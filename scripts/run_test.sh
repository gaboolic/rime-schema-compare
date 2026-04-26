#!/usr/bin/env bash
set -euo pipefail

artifacts_dir="artifacts"
report_dir="report"
rime_dll_path=""
date_format="%Y-%m-%d"
progress_every=0

usage() {
    cat <<'EOF'
Usage: scripts/run_test.sh [options]

Options:
  --artifacts-dir DIR    Directory for benchmark artifacts (default: artifacts)
  --report-dir DIR       Directory for markdown reports (default: report)
  --rime-dll PATH        Path to librime dynamic library (default: auto-detect)
  --date-format FORMAT   date(1) format for dated report name (default: %Y-%m-%d)
  --progress-every N     Progress interval passed to benchmark_sentences.py (default: 0)
  -h, --help             Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --artifacts-dir)
            artifacts_dir="${2:?missing value for --artifacts-dir}"
            shift 2
            ;;
        --report-dir)
            report_dir="${2:?missing value for --report-dir}"
            shift 2
            ;;
        --rime-dll)
            rime_dll_path="${2:?missing value for --rime-dll}"
            shift 2
            ;;
        --date-format)
            date_format="${2:?missing value for --date-format}"
            shift 2
            ;;
        --progress-every)
            progress_every="${2:?missing value for --progress-every}"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd -- "$script_dir/.." && pwd)"
artifacts_path="$repo_root/$artifacts_dir"
report_path="$repo_root/$report_dir"

resolve_rime_library() {
    local candidate
    local candidates=(
        "$repo_root/lib/rime.dll"
        "$repo_root/lib/librime.dylib"
        "$repo_root/lib/librime.1.dylib"
        "$repo_root/lib/librime.so"
        "$repo_root/lib/librime.so.1"
        "/opt/homebrew/lib/librime.dylib"
        "/opt/homebrew/lib/librime.1.dylib"
        "/usr/local/lib/librime.dylib"
        "/usr/local/lib/librime.1.dylib"
        "/usr/local/lib/librime.so"
        "/usr/local/lib/librime.so.1"
        "/usr/lib/librime.so"
        "/usr/lib/librime.so.1"
        "/usr/lib/x86_64-linux-gnu/librime.so"
        "/usr/lib/x86_64-linux-gnu/librime.so.1"
        "/usr/lib/aarch64-linux-gnu/librime.so"
        "/usr/lib/aarch64-linux-gnu/librime.so.1"
    )

    if [[ -n "$rime_dll_path" ]]; then
        if [[ "$rime_dll_path" = /* ]]; then
            printf '%s\n' "$rime_dll_path"
        else
            printf '%s\n' "$repo_root/$rime_dll_path"
        fi
        return 0
    fi

    for candidate in "${candidates[@]}"; do
        if [[ -e "$candidate" ]]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    return 1
}

if ! resolved_rime_dll_path="$(resolve_rime_library)"; then
    echo "librime dynamic library not found. Pass it explicitly with --rime-dll /path/to/librime.dylib or --rime-dll /path/to/librime.so" >&2
    exit 1
fi

mkdir -p "$artifacts_path" "$report_path"

if [[ ! -e "$resolved_rime_dll_path" ]]; then
    echo "librime dynamic library not found: $resolved_rime_dll_path" >&2
    exit 1
fi

export PYTHONPATH="$repo_root/src"
export RIME_DLL="$resolved_rime_dll_path"

get_submodule_snapshots() {
    local gitmodules_path="$repo_root/.gitmodules"
    local entry key path name full_path commit_id branch

    [[ -f "$gitmodules_path" ]] || return 0

    git config --file "$gitmodules_path" --get-regexp '^submodule\..*\.path$' 2>/dev/null |
        while IFS= read -r entry; do
            key="${entry%%[[:space:]]*}"
            path="${entry#*[[:space:]]}"
            name="${key#submodule.}"
            name="${name%.path}"
            full_path="$repo_root/$path"

            [[ -d "$full_path" ]] || continue

            commit_id="$(git -C "$full_path" rev-parse HEAD 2>/dev/null || true)"
            [[ -n "$commit_id" ]] || continue

            branch="$(git config --file "$gitmodules_path" --get "submodule.$name.branch" 2>/dev/null || true)"
            if [[ -n "$branch" ]]; then
                printf -- '- `%s` (`%s`): `%s`\n' "$path" "$branch" "$commit_id"
            else
                printf -- '- `%s`: `%s`\n' "$path" "$commit_id"
            fi
        done
}

cd "$repo_root"
python "scripts/benchmark_sentences.py" \
    --progress-every "$progress_every" \
    --out-dir "$artifacts_path" \
    --rime-dll "$resolved_rime_dll_path"

latest_report="$(
    python - "$artifacts_path" <<'PY'
import pathlib
import sys

artifacts_path = pathlib.Path(sys.argv[1])
reports = sorted(
    artifacts_path.glob("*_report.txt"),
    key=lambda path: path.stat().st_mtime,
    reverse=True,
)
if reports:
    print(reports[0])
PY
)"

if [[ -z "$latest_report" ]]; then
    echo "No *_report.txt file was generated under '$artifacts_path'." >&2
    exit 1
fi

generated_at="$(date '+%Y-%m-%d %H:%M:%S %z')"
dated_report_name="$(date +"$date_format").md"
latest_report_name="$(basename -- "$latest_report")"
submodule_snapshots="$(get_submodule_snapshots)"

{
    echo '# Rime 评测结果'
    echo
    echo "- 生成时间: $generated_at"
    echo "- 来源文件: \`$latest_report_name\`"
    echo
    echo '## Vendor 子模块版本'
    echo
    if [[ -n "$submodule_snapshots" ]]; then
        printf '%s\n' "$submodule_snapshots"
    else
        echo '- 未检测到子模块信息'
    fi
    echo
    echo '## 评测摘要'
    echo
    echo '```text'
    python - "$latest_report" <<'PY'
import pathlib
import sys

print(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"), end="")
PY
    echo '```'
    echo
} > "$report_path/latest.md"

cp "$report_path/latest.md" "$report_path/$dated_report_name"
