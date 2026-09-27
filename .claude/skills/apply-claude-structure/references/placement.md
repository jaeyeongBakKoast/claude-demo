# 배치 원칙 요약

## 로드 시점이 곧 비용이다

| 위치 | 언제 컨텍스트에 들어오는가 | 그래서 여기 둘 것 |
|---|---|---|
| 루트 `CLAUDE.md` (+ `@import` 한 파일) | 세션 시작 시 항상. `/compact` 뒤에도 다시 읽힌다 | 모든 작업에 필요한 사실만 |
| `<하위폴더>/CLAUDE.md` | 그 폴더의 파일을 처음 읽을 때 | 그 모듈의 명령·구조·함정 |
| `.claude/rules/*.md` + `paths:` | 매칭되는 파일을 읽을 때 | 파일 유형·경로별 규칙 |
| `.claude/rules/*.md` (paths 없음) | 항상 | 쓰지 않는다 — 루트 CLAUDE.md와 같다 |
| `skills/<이름>/SKILL.md` | description만 항상, 본문은 쓸 때 | 가끔 필요한 절차·참고 자료 |
| `<하위폴더>/.claude/skills/` | 그 폴더의 파일을 처음 읽을 때 발견됨 | 한 모듈 그룹 전용 절차 |
| `agents/*.md` | 위임할 때, 별도 컨텍스트에서 | 결과 요약만 필요한 부수 작업 |
| 훅 | 도구 호출 전후, 모델 판단과 무관하게 | 반드시 지켜져야 하는 것 |

`@import`는 컨텍스트를 줄이지 않는다. import한 파일도 시작 시 전부 로드된다. 정리 수단일 뿐이다.

## 자주 하는 실수

- **컨벤션을 `.claude/`에 쓴다** → 사람과 다른 도구가 못 본다. `docs/conventions/`에 쓰고 가리킨다.
- **rule에 `paths`를 빼먹는다** → 항상 로드된다. YAML 오류도 같은 결과다.
- **모듈 그룹마다 `.claude/settings.json`을 둔다** → 상위에서 상속되지 않고, 그 폴더에서 Claude를 시작할 때만 읽힌다.
  훅·권한은 루트 한 곳에.
- **description에 워크플로를 요약한다** → 모델이 본문을 읽지 않고 요약대로 행동한다. "언제 쓰는가"만.
- **"절대 ~하지 마라"를 CLAUDE.md에만 쓴다** → 요청일 뿐 보장이 아니다. 훅이나 `permissions.deny`로.
- **AGENTS.md와 CLAUDE.md에 같은 내용을 쓴다** → CLAUDE.md 첫 줄에 `@AGENTS.md`로 import 한다.
  CLAUDE.md가 있으면 Claude Code는 AGENTS.md를 자동으로 읽지 않는다. 심링크는 Windows에서 깨지고 Edit가 막힌다.
- **`.claude/commands/`에 새 명령을 만든다** → 예전 형식. skill로 만든다.
- **에이전트·스킬을 미리 잔뜩 만든다** → 쓰이지 않는 자산의 description이 매 세션 공간을 차지한다.

## 크기 기준

- 루트 `CLAUDE.md` 200줄 이하, `SKILL.md` 500줄 이하
- skill description은 짧게, 요청에 나올 단어로 시작한다 (많아지면 잘린다)
