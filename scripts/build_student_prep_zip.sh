#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

output_zip="exercises/student-prep-files.zip"
tmp_file_list="$(mktemp "${TMPDIR:-/tmp}/student-prep-files.XXXXXX")"
trap 'rm -f "$tmp_file_list"' EXIT

exercise_files_dirs=(
  "exercises/01-prepare-foundry-project/files"
  "exercises/02-build-service-operations-agent/files"
  "exercises/03-extend-agent-with-mcp/files"
  "exercises/04-add-foundry-iq/files"
  "exercises/05-build-foundry-workflow/files"
  "exercises/06-build-agent-framework-agent/files"
  "exercises/07-build-multi-agent-solution/files"
)

for dir_path in "${exercise_files_dirs[@]}"; do
  if [[ ! -d "$dir_path" ]]; then
    echo "ERROR: Required directory not found: $dir_path" >&2
    exit 1
  fi
done

for dir_path in "${exercise_files_dirs[@]}"; do
  find "$dir_path" -type f | sort >> "$tmp_file_list"
done

if [[ ! -s "$tmp_file_list" ]]; then
  echo "ERROR: No input files found to package." >&2
  exit 1
fi

rm -f "$output_zip"
zip -q "$output_zip" -@ < "$tmp_file_list"

file_count="$(wc -l < "$tmp_file_list" | tr -d ' ')"
echo "Created $output_zip with $file_count files."
