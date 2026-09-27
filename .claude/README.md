# .claude/ — Claude Code 전용 자산

이 폴더에는 **Claude Code만 쓰는 자산**을 둔다. 사람이나 다른 AI 도구도 읽어야 하는 내용(코드 컨벤션,
설치 절차)은 `docs/`에 쓰고, 여기서는 그 문서를 가리키기만 한다. 두 곳에 쓰면 반드시 어긋난다.

전체 배경과 출처는 [../docs/guides/claude-structure.md](../docs/guides/claude-structure.md)를 본다.

## 무엇을 어디에 두는가

| 성격 | 위치 | 로드 시점 |
|---|---|---|
| 모든 작업에 필요한 사실 (명령, 금지사항, 문서 인덱스) | 루트 `CLAUDE.md` | 세션 시작 시 항상 |
| 한 모듈에만 해당하는 명령·구조·함정 | `<모듈>/CLAUDE.md` | 그 모듈 파일을 처음 읽을 때 |
| 특정 파일 유형·경로에만 해당하는 규칙 | `rules/*.md` (`paths:` 필수) | 매칭되는 파일을 읽을 때 |
| 가끔 필요한 절차·참고 자료 | `skills/<이름>/SKILL.md` | description만 항상, 본문은 쓸 때 |
| 한 모듈 그룹에서만 쓰는 절차 | `<그룹>/.claude/skills/` | 그 그룹 파일을 처음 읽을 때 |
| 결과 요약만 돌려받으면 되는 부수 작업 | `agents/*.md` | 위임할 때 (별도 컨텍스트) |
| **반드시** 지켜져야 하는 것 | `hooks/*.sh` + `settings.json` | 도구 호출 전후 (결정적) |
| 권한 허용·차단 | `settings.json`의 `permissions` | 항상 |
| 개인 설정 | `settings.local.json`, `CLAUDE.local.md` | 커밋하지 않는다 |

판단 기준: CLAUDE.md의 한 줄마다 "이 줄을 지우면 Claude가 실수하는가?"를 묻는다. 아니면 지운다.
"하지 마라"가 정말 중요하면 CLAUDE.md에 쓰는 것으로 끝내지 않고 훅이나 `permissions.deny`로 강제한다.

## 주의할 동작

- **`settings.json`은 상위 폴더에서 상속되지 않는다.** 훅·권한은 루트 `.claude/settings.json` 한 곳에 둔다.
  모듈 그룹의 `.claude/`에는 `skills/`만 둔다.
- **`rules/`에서 frontmatter 필드는 `paths`만 읽는다.** `paths`가 없으면 항상 로드되므로 반드시 붙인다.
  YAML이 깨지면 `paths`가 없는 것으로 취급되어 항상 로드된다.
- **`/compact` 뒤에는 루트 CLAUDE.md만 다시 읽힌다.** 모듈 CLAUDE.md와 rules는 해당 파일을 다시 읽을 때 로드된다.
- **`.claude/commands/`는 쓰지 않는다.** 예전 형식이다. 새 슬래시 명령은 skill로 만든다.

## 작성 규칙

에이전트·스킬·룰을 추가하거나 고칠 때의 규칙은 [rules/claude-assets.md](rules/claude-assets.md)에 있다
(이 폴더의 `.md`를 읽으면 자동 로드된다).

## 현재 자산

| 종류 | 이름 | 용도 |
|---|---|---|
| hook | `hooks/guard-protected-paths.sh` | PreToolUse — `.env`·비밀·운영 문서 수정 차단 |
| hook | `hooks/lint-changed-file.sh` | PostToolUse — 바뀐 파일만 eslint/ruff |
| rule | `rules/*.md` | Java 테스트, React, Python, SQL, 운영 문서, Claude 자산 |
| agent | `explore`, `debugger`, `architect`, `test-engineer`, `security-reviewer`, `git-master`, `writer` | 루트 CLAUDE.md의 위임 표 참고 |
| skill | `apply-claude-structure` | 기존 저장소에 이 구조를 적용 |
| skill | `scaffolding-crud-api` | 테이블 기반 CRUD API 골격 생성 (도메인 워크플로 예시) |
| skill | `commit` | 컨벤션에 맞는 커밋 (부수효과 스킬 예시, 사용자 호출 전용) |
| skill | `edge/.claude/skills/edge-release-check` | edge 배포 전 점검 (그룹 전용 스킬 예시) |
