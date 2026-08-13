from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from service_ops.config import REPOSITORY_ROOT, Settings


@dataclass(frozen=True)
class CheckResult:
    level: str
    label: str
    detail: str


def _command_check(command: str, label: str) -> CheckResult:
    executable = shutil.which(command)
    if executable:
        return CheckResult("READY", label, executable)
    return CheckResult("ERROR", label, f"{command} is not installed")


def _module_check(module: str) -> CheckResult:
    try:
        available = importlib.util.find_spec(module) is not None
    except ModuleNotFoundError:
        available = False
    if available:
        return CheckResult("READY", f"Python import: {module}", "available")
    return CheckResult("ERROR", f"Python import: {module}", "missing from .venv")


def _mcp_compatibility_check() -> CheckResult:
    try:
        from mcp.server.fastmcp import FastMCP
        from mcp.types import InitializeResult

        installed_version = version("mcp")
    except (ImportError, PackageNotFoundError) as exc:
        return CheckResult("ERROR", "MCP compatibility", f"MCP v1 API unavailable: {exc}")

    compatible = (
        installed_version == "1.29.0"
        and "protocolVersion" in InitializeResult.model_fields
        and callable(FastMCP)
    )
    if compatible:
        return CheckResult("READY", "MCP compatibility", "mcp 1.29.0 with v1 schema")
    return CheckResult(
        "ERROR",
        "MCP compatibility",
        f"expected mcp 1.29.0 with protocolVersion; found {installed_version}",
    )


def _azure_sign_in_check() -> CheckResult:
    if not shutil.which("az"):
        return CheckResult("ERROR", "Azure sign-in", "Azure CLI is not installed")
    completed = subprocess.run(
        ["az", "account", "show", "--query", "name", "--output", "tsv"],
        capture_output=True,
        check=False,
        text=True,
        timeout=15,
    )
    if completed.returncode == 0:
        return CheckResult("READY", "Azure sign-in", "signed in; account details are hidden")
    return CheckResult("ACTION", "Azure sign-in", "run: az login --use-device-code")


def collect_checks(*, bootstrap: bool = False) -> list[CheckResult]:
    python_minor = f"{sys.version_info.major}.{sys.version_info.minor}"
    python_result = (
        CheckResult("READY", "Python", f"{python_minor} at {sys.executable}")
        if python_minor == "3.12"
        else CheckResult("ERROR", "Python", f"3.12 required; found {python_minor}")
    )
    venv_result = (
        CheckResult("READY", "Repository virtual environment", str(Path(sys.prefix)))
        if Path(sys.prefix).resolve() == (REPOSITORY_ROOT / ".venv").resolve()
        else CheckResult("ERROR", "Repository virtual environment", "expected .venv interpreter")
    )
    results = [
        python_result,
        venv_result,
        _command_check("git", "Git"),
        _command_check("az", "Azure CLI"),
        _module_check("agent_framework"),
        _module_check("agent_framework.foundry"),
        _module_check("agent_framework.orchestrations"),
        _module_check("azure.identity"),
        _module_check("dotenv"),
        _mcp_compatibility_check(),
    ]
    if bootstrap:
        return results

    results.append(_azure_sign_in_check())
    settings = Settings.from_environment()
    missing = settings.missing_for_chat_agent()
    if missing:
        results.append(CheckResult("ACTION", ".env configuration", f"set {', '.join(missing)}"))
    else:
        results.append(
            CheckResult("READY", ".env configuration", "project endpoint and model are set")
        )
    return results


def print_checks(*, bootstrap: bool = False, strict: bool = False) -> int:
    results = collect_checks(bootstrap=bootstrap)
    for result in results:
        print(f"{result.level:<6} {result.label}: {result.detail}")
    has_error = any(result.level == "ERROR" for result in results)
    has_action = any(result.level == "ACTION" for result in results)
    if has_error or (strict and has_action):
        return 1
    return 0
