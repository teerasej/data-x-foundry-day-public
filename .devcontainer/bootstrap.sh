#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv_dir="${VENV_DIR:-$repo_root/.venv}"
python_bin="${PYTHON_BIN:-python3}"
lock_fingerprint_file="$venv_dir/.requirements-lock.sha256"

cd "$repo_root"

python_version="$("$python_bin" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$python_version" != "3.12" ]]; then
  echo "ERROR: Python 3.12 is required; found $python_version." >&2
  exit 1
fi

lock_fingerprint="$("$python_bin" -c 'import hashlib, pathlib; print(hashlib.sha256(pathlib.Path("requirements.lock").read_bytes()).hexdigest())')"
installed_fingerprint=""
if [[ -f "$lock_fingerprint_file" ]]; then
  installed_fingerprint="$(<"$lock_fingerprint_file")"
fi

if [[ -d "$venv_dir" && "$installed_fingerprint" != "$lock_fingerprint" ]]; then
  echo "Dependency lock changed; recreating $venv_dir."
  rm -rf "$venv_dir"
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
printf '%s\n' "$lock_fingerprint" >"$lock_fingerprint_file"

"$venv_dir/bin/python" -m service_ops check --bootstrap

echo "Bootstrap complete. The repository-local .venv is ready."
