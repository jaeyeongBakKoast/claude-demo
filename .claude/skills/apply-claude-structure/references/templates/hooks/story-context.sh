#!/bin/bash
# UserPromptSubmit 훅. 요청마다 현재 스토리와 다음 단계를 대화에 넣는다 (stdout → 컨텍스트).
# 막지 않는다. 브랜치 이름의 S-### 로 docs/stories/S-###-*/ 를 찾는다.
set -u

root="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -n "$root" ] && [ -d "$root/docs/stories" ] || exit 0
cd "$root" || exit 0

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || exit 0
id=$(printf '%s' "$branch" | grep -oE 'S-[0-9]{3,}' | head -1)

if [ -z "$id" ]; then
    echo "[스토리] 현재 브랜치($branch)에 스토리 없음. 기능 추가·변경 요청이면 story-new 로 시작한다 (질문·조사, 문서·오타, 설정값, 긴급 대응은 예외)."
    if grep -q '<예:' docs/product/requirements.md 2>/dev/null; then
        echo "[스토리] docs/product/ 가 아직 견본 상태다. 제품 초기 분석이 필요하면 product-discovery 를 먼저 쓴다."
    fi
    exit 0
fi

dir=$(ls -d docs/stories/"$id"-*/ 2>/dev/null | head -1)
if [ -z "$dir" ]; then
    echo "[스토리] 브랜치는 $id 인데 docs/stories/$id-*/ 가 없다. story-new 로 story.md 를 먼저 만든다."
    exit 0
fi

status=$(sed -n '/^---$/,/^---$/{s/^status:[[:space:]]*//p}' "$dir/story.md" 2>/dev/null | head -1)
done_n=$(grep -cE '^- \[x\] T[0-9]+' "$dir/design.md" 2>/dev/null)
todo_n=$(grep -cE '^- \[ \] T[0-9]+' "$dir/design.md" 2>/dev/null)
next_task=$(grep -m1 -oE '^- \[ \] T[0-9]+' "$dir/design.md" 2>/dev/null | grep -oE 'T[0-9]+')

case "$status" in
    draft)       next="수용 기준 승인을 받는다 (story-new 승인①). 승인 전에는 설계·코드를 쓰지 않는다." ;;
    ready)       next="story-design — 이 스토리가 건드리는 UC·화면·API·ERD만 상세화하고 design.md 작성 후 승인②." ;;
    designed)    next="story-build — design.md 작업 목록 순서대로 구현한다." ;;
    in-progress) next="story-build — ${next_task:-남은 작업 확인}. 작업마다 테스트 후 design.md 체크와 검증 로그를 갱신한다." ;;
    review)      next="story-review — 수용 기준 증거, 문서-코드 일치, 추적표 갱신 후 수락③." ;;
    done)        next="완료된 스토리다. 새 작업이면 새 브랜치에서 story-new." ;;
    *)           next="story.md 의 status 를 확인한다." ;;
esac

tasks=""
[ -f "$dir/design.md" ] && tasks=" · 작업 ${done_n:-0}/$(( ${done_n:-0} + ${todo_n:-0} ))"
echo "[스토리] $id (${dir%/}) · status: ${status:-?}$tasks"
echo "[스토리] 다음: $next"
exit 0
