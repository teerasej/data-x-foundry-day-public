#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

bootstrap_mode="false"
if [[ "${1:-}" == "--bootstrap" ]]; then
  bootstrap_mode="true"
fi

if [[ ! -x .venv/bin/python ]]; then
  echo "ERROR: .venv is missing. Run bash .devcontainer/bootstrap.sh." >&2
  exit 1
fi

.venv/bin/python -m service_ops check --bootstrap

if command -v code >/dev/null 2>&1; then
  installed_extensions="$(code --list-extensions 2>/dev/null | tr '[:upper:]' '[:lower:]' || true)"
  extension_status=0
  for extension in ms-python.python ms-python.vscode-pylance ms-windows-ai-studio.windows-ai-studio charliermarsh.ruff; do
    if grep -qx "$extension" <<<"$installed_extensions"; then
      echo "READY  VS Code extension: $extension"
    else
      echo "ACTION VS Code extension is still installing or unavailable: $extension"
      extension_status=1
    fi
  done

  if [[ "$bootstrap_mode" == "false" && "$extension_status" -ne 0 ]]; then
    echo "Open Extensions in VS Code and confirm the required extensions before Exercise 1." >&2
  fi
else
  echo "INFO   VS Code CLI is not available during this lifecycle step; extension IDs are validated from devcontainer.json."
fi

echo "Health check complete."
