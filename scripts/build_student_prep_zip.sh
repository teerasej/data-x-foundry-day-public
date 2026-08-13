#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

output_zip="exercises/student-prep-files.zip"
tmp_file_list="$(mktemp "${TMPDIR:-/tmp}/student-prep-files.XXXXXX")"
trap 'rm -f "$tmp_file_list"' EXIT

exercise_files_dirs=()
while IFS= read -r dir_path; do
  exercise_files_dirs+=("$dir_path")
done < <(find exercises -type d -name files | sort)

if [[ ${#exercise_files_dirs[@]} -eq 0 ]]; then
  echo "ERROR: No exercise files directories found under exercises/" >&2
  exit 1
fi

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
