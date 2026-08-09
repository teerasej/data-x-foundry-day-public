from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\]\((?!https?://|mailto:|#)([^)#?]+)")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Azure-style connection string": re.compile(r"AccountKey=[A-Za-z0-9+/=]{20,}"),
    "common API token": re.compile(r"(?:sk-|AIza)[A-Za-z0-9_-]{20,}"),
}


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


def main() -> int:
    errors = check_local_links() + check_required_extensions() + check_for_secrets()
    if errors:
        print("\n".join(errors))
        return 1
    print("Local links, required extension declarations, and secret patterns passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
