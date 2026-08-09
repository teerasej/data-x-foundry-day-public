#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv_dir="$repo_root/.venv"
python_bin="${PYTHON_BIN:-python3}"

cd "$repo_root"

python_version="$("$python_bin" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$python_version" != "3.12" ]]; then
  echo "ERROR: Python 3.12 is required; found $python_version." >&2
  exit 1
fi

if [[ ! -x "$venv_dir/bin/python" ]]; then
  "$python_bin" -m venv "$venv_dir"
fi

venv_version="$("$venv_dir/bin/python" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$venv_version" != "3.12" ]]; then
  echo "ERROR: Existing .venv uses Python $venv_version. Rebuild the container." >&2
  exit 1
fi

"$venv_dir/bin/python" -m pip install --no-input "pip==26.2.1"
"$venv_dir/bin/python" -m pip install --no-input --requirement requirements.lock
"$venv_dir/bin/python" -m pip check

"$venv_dir/bin/python" -m service_ops check --bootstrap

echo "Bootstrap complete. The repository-local .venv is ready."
