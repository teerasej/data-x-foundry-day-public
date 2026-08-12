from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\]\((?!https?://|mailto:|#)([^)#?]+)")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Azure-style connection string": re.compile(r"AccountKey=[A-Za-z0-9+/=]{20,}"),
    "common API token": re.compile(r"(?:sk-|AIza)[A-Za-z0-9_-]{20,}"),
}
PLACEHOLDER_STATUS = "จะเพิ่มใน Review Gate ถัดไป"
PRIVATE_PATH_PATTERNS = ("/Users/", "/private/var/", "Trainocate x DataX")


def check_local_links() -> list[str]:
    errors: list[str] = []
    for document in ROOT.rglob("*.md"):
        if any(part.startswith(".") for part in document.relative_to(ROOT).parts):
            continue
        text = document.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            raw_target = match.group(1).strip().strip("<>")
            target = raw_target.split("#", maxsplit=1)[0]
            if target and not (document.parent / target).exists():
                errors.append(f"Broken local link: {document.relative_to(ROOT)} -> {raw_target}")
    return errors


def check_required_extensions() -> list[str]:
    config = json.loads((ROOT / ".devcontainer/devcontainer.json").read_text(encoding="utf-8"))
    installed = set(config["customizations"]["vscode"]["extensions"])
    required = {
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-windows-ai-studio.windows-ai-studio",
    }
    missing = sorted(required - installed)
    return [f"Missing required extension in devcontainer.json: {item}" for item in missing]


def check_for_secrets() -> list[str]:
    errors: list[str] = []
    excluded = {".git", ".venv", ".pytest_cache", ".ruff_cache"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or excluded.intersection(path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"Potential {label}: {path.relative_to(ROOT)}")
    return errors


def check_exercise_structure() -> list[str]:
    errors: list[str] = []
    for document in sorted((ROOT / "exercises").glob("*/README.md")):
        text = document.read_text(encoding="utf-8")
        relative = document.relative_to(ROOT)
        if "> **License" not in text:
            errors.append(f"Missing exercise license statement: {relative}")
        if PLACEHOLDER_STATUS in text:
            errors.append(f"Unfinished review-gate placeholder: {relative}")

        matches = list(re.finditer(r"^## Practice \d+:.*$", text, re.MULTILINE))
        if not matches:
            errors.append(f"No Practice headings: {relative}")
            continue
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            section = text[match.start() : end]
            practice_name = match.group(0)
            if section.count("**Primary target:**") != 1:
                errors.append(
                    f"Practice must have one Primary target: {relative} -> {practice_name}"
                )
            if len(re.findall(r"^### Checkpoint$", section, re.MULTILINE)) != 1:
                errors.append(f"Practice must have one Checkpoint: {relative} -> {practice_name}")

        files_directory = document.parent / "files"
        if not files_directory.is_dir() or not any(files_directory.iterdir()):
            errors.append(f"Exercise files directory is missing or empty: {relative}")
    return errors


def check_dependency_lock() -> list[str]:
    errors: list[str] = []
    requirement_lines = [
        line.strip()
        for line in (ROOT / "requirements.in").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    locked = {
        line.split("==", maxsplit=1)[0].casefold()
        for line in (ROOT / "requirements.lock").read_text(encoding="utf-8").splitlines()
        if "==" in line
    }
    for requirement in requirement_lines:
        if "==" not in requirement:
            errors.append(f"Direct dependency is not exactly pinned: {requirement}")
            continue
        name = requirement.split("==", maxsplit=1)[0].casefold()
        if name not in locked:
            errors.append(f"Direct dependency missing from requirements.lock: {requirement}")

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    runtime_dependencies = project["project"]["dependencies"]
    direct_set = set(requirement_lines)
    for dependency in runtime_dependencies:
        if dependency not in direct_set:
            errors.append(f"Runtime dependency missing from requirements.in: {dependency}")
    return errors


def check_public_safety() -> list[str]:
    errors: list[str] = []
    excluded = {".git", ".venv", ".pytest_cache", ".ruff_cache"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or excluded.intersection(path.relative_to(ROOT).parts):
            continue
        if path == Path(__file__).resolve():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in PRIVATE_PATH_PATTERNS:
            if pattern in text:
                errors.append(f"Private workspace marker {pattern!r}: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = (
        check_local_links()
        + check_required_extensions()
        + check_for_secrets()
        + check_exercise_structure()
        + check_dependency_lock()
        + check_public_safety()
    )
    if errors:
        print("\n".join(errors))
        return 1
    print(
        "Links, assets, exercise structure, dependencies, extensions, public safety, "
        "and secret patterns passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
