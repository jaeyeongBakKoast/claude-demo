---
paths:
  - ".claude/**/*.md"
  - "*/.claude/**/*.md"
  - "**/CLAUDE.md"
  - "AGENTS.md"
---

# Claude Code 자산 (CLAUDE.md · agents · skills · rules)

## description
- **"언제 쓰는가"만 쓴다.** `Use when …`으로 시작하고 `Do NOT use for …`로 경계를 긋는다.
  이 저장소의 경로·상황(`edge/api`, `central/ui` …)을 넣어 내장 에이전트·스킬과 구분되게 한다.
- **워크플로를 요약하지 않는다.** 요약이 있으면 모델이 본문을 읽지 않고 요약대로만 행동한다.
- 트리거 정확도를 위해 description은 영어로, 본문은 한국어로 쓴다. 식별자·명령·코드는 그대로 둔다.

## CLAUDE.md
- 루트는 200줄 이하. 한 줄마다 "지우면 Claude가 실수하는가?"를 묻는다.
- 모듈 `CLAUDE.md`는 그 모듈의 명령·구조·함정만. 컨벤션 본문은 `docs/conventions/`를 가리킨다.
- 자주 바뀌는 정보(진행 상황, 담당자)와 코드를 읽으면 알 수 있는 것은 쓰지 않는다.

## rules
- 한 파일에 한 주제. frontmatter는 `paths`만 읽힌다. **`paths`가 없으면 항상 로드되므로 반드시 붙인다.**
- `paths`는 저장소 루트 기준 글로브. 규칙 본문은 짧게, 세부는 `docs/conventions/`를 가리킨다.

## skills
- `.claude/skills/<name>/SKILL.md`. `name`은 디렉터리명과 같게, 소문자·숫자·하이픈만.
- 본문은 500줄 이하. 길어지면 `references/`로 나누고 SKILL.md에서 한 단계로만 참조한다.
- 커밋·배포처럼 부수효과가 있는 스킬은 `disable-model-invocation: true`로 사용자만 호출하게 한다.
- 한 모듈 그룹에서만 쓰는 스킬은 `<그룹>/.claude/skills/`에 둔다.

## agents
- `name`, `description` 필수. 읽기 전용 에이전트는 `disallowedTools`에 `Write`, `Edit`를 둔다.
- `model`은 역할에 맞춰 고른다: 탐색·문서 `haiku`, 구현·디버깅 `sonnet`, 설계·보안 `opus`.
- 커밋·푸시하는 에이전트는 "호출자가 사용자 확인을 명시하지 않으면 실행하지 않는다"를 본문에 둔다.

## 검증
- 스킬·에이전트를 새로 만들거나 고치면, 그것 없이 한 번 / 있을 때 한 번 같은 요청을 돌려 차이를 확인한다.
