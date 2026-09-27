#!/bin/bash
# PreToolUse(Edit|Write) 훅. 사람이 관리하는 파일의 수정을 결정적으로 막는다.
# CLAUDE.md 에 "고치지 마라"라고 쓰는 것은 요청일 뿐이라 여기서 강제한다.
# 막을 때는 이유를 stderr 로 내고 exit 2 → Claude 가 이유를 보고 사용자에게 알린다.
set -u

# jq 설치를 전제할 수 없어 python3 로 읽는다.
file=$(python3 -c 'import sys, json
d = json.load(sys.stdin)
print(d.get("tool_input", {}).get("file_path", ""))' 2>/dev/null)
[ -n "$file" ] || exit 0

root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}"
rel="${file#"$root"/}"

case "$rel" in
    *.env.example)
        exit 0 ;;
    .env|*/.env|.env.*|*/.env.*)
        reason="비밀값 파일(.env)은 수정하지 않는다. 필요한 값은 사용자에게 요청한다." ;;
    secrets/*|*/secrets/*)
        reason="secrets/ 아래 파일은 수정하지 않는다." ;;
    */docs/ops/*)
        reason="운영 절차 문서(docs/ops/)는 현장 검증된 자산이라 사람이 관리한다. 수정이 필요하면 변경안을 제시만 한다." ;;
    *)
        exit 0 ;;
esac

printf '[guard] %s 수정 차단: %s\n' "$rel" "$reason" >&2
exit 2
