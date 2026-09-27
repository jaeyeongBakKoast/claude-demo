#!/bin/bash
# PostToolUse(Edit|Write) 훅. 방금 바뀐 파일 하나만 lint 한다.
#   .ts/.tsx → 해당 UI 모듈의 eslint
#   .py      → 해당 Python 모듈의 ruff
# 대상 밖이거나 도구가 설치되지 않았으면 조용히 통과한다(exit 0).
# 위반이 있으면 결과를 stderr 로 내고 exit 2 → Claude 가 그 내용을 보고 고친다.
#
# 새 모듈을 추가하면 아래 UI_MODULES / PY_MODULES 에 경로를 더한다.
set -u

UI_MODULES="edge/ui central/ui"
PY_MODULES="edge/worker"

file=$(python3 -c 'import sys, json
d = json.load(sys.stdin)
print(d.get("tool_input", {}).get("file_path") or d.get("tool_response", {}).get("filePath") or "")' 2>/dev/null)
[ -n "$file" ] || exit 0

root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$root" ] || exit 0

case "$file" in
    *.ts|*.tsx)
        for module in $UI_MODULES; do
            case "$file" in
                "$root/$module/"*)
                    eslint="$root/$module/node_modules/.bin/eslint"
                    [ -x "$eslint" ] || exit 0
                    out=$(cd "$root/$module" && "$eslint" --no-warn-ignored "$file" 2>&1)
                    if [ $? -ne 0 ]; then
                        printf '[eslint %s] 위반이 있습니다. 고친 뒤 다시 확인하세요.\n%s\n' "$module" "$out" >&2
                        exit 2
                    fi
                    exit 0
                    ;;
            esac
        done
        ;;
    *.py)
        for module in $PY_MODULES; do
            case "$file" in
                "$root/$module/"*)
                    dir="$root/$module"
                    if [ -x "$dir/.venv/bin/ruff" ]; then
                        ruff="$dir/.venv/bin/ruff"
                    elif command -v ruff >/dev/null 2>&1; then
                        ruff=ruff
                    else
                        exit 0
                    fi
                    out=$(cd "$dir" && "$ruff" check "$file" 2>&1)
                    if [ $? -ne 0 ]; then
                        printf '[ruff %s] 위반이 있습니다. 고친 뒤 다시 확인하세요.\n%s\n' "$module" "$out" >&2
                        exit 2
                    fi
                    exit 0
                    ;;
            esac
        done
        ;;
esac
exit 0
