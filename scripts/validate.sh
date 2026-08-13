#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python_bin="${PYTHON_BIN:-$repo_root/.venv/bin/python}"
if [[ ! -x "$python_bin" ]]; then
  echo "ERROR: Python environment not found. Run bash .devcontainer/bootstrap.sh." >&2
  exit 1
fi

"$python_bin" -m json.tool .devcontainer/devcontainer.json >/dev/null
"$python_bin" -m compileall -q service_ops tests
"$python_bin" -m ruff check .
"$python_bin" -m pytest
"$python_bin" -m pip check
"$python_bin" scripts/validate_repository.py

git diff --check

echo "Repository validation passed."
