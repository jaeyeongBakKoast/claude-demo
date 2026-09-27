@AGENTS.md

# CLAUDE.md

이 파일은 Claude Code가 이 저장소에서 작업할 때 항상 로드된다. **짧게 유지한다(200줄 이하).**
프로젝트 개요와 구조는 위에서 import한 `AGENTS.md`에 있다. 여기에는 Claude Code 전용 규칙만 둔다.

## 세부 규칙 — 작업 전에 읽는다

| 이런 작업을 한다면                                   | 먼저 읽을 것                                             |
| ---------------------------------------------------- | -------------------------------------------------------- |
| `edge/api/`, `central/api/`의 `.java` 생성·수정      | [docs/conventions/java.md](docs/conventions/java.md)     |
| `edge/ui/`, `central/ui/`의 `.ts`/`.tsx` 생성·수정   | [docs/conventions/react.md](docs/conventions/react.md)   |
| `edge/worker/`의 `.py` 생성·수정                     | [docs/conventions/python.md](docs/conventions/python.md) |
| DDL/DML 작성, MyBatis 매퍼 XML 수정                  | [docs/conventions/sql.md](docs/conventions/sql.md)       |
| 커밋 메시지, 브랜치, PR 본문 작성                    | [docs/conventions/commit.md](docs/conventions/commit.md) |
| `.claude/` 아래 에이전트·스킬·룰·훅 추가·수정         | [.claude/README.md](.claude/README.md)                   |

파일 하나만 고치는 작은 변경이어도 해당 문서를 먼저 읽는다.
경로별 세부 규칙은 [.claude/rules/](.claude/rules/)에 있고, 해당 경로의 파일을 읽을 때 자동으로 로드된다.
모듈 고유의 명령·구조·주의점은 각 모듈의 `CLAUDE.md`에 있고, 그 모듈 파일을 읽을 때 로드된다.

## 에이전트 위임 — 이런 작업은 서브에이전트에 맡긴다

한 파일만 읽거나 고치는 작업은 위임하지 않고 직접 한다.

| 이런 작업을 한다면                                          | 위임할 에이전트     |
| ----------------------------------------------------------- | ------------------- |
| 여러 모듈에 걸친 파일·호출 관계 찾기 (3개 파일 이상)        | `explore`           |
| 스택 트레이스, 빌드 실패, 테스트 실패의 원인 찾기           | `debugger`          |
| 구조 판단, 변경이 edge/central 경계에 맞는지 진단           | `architect`         |
| 테스트 추가·수정, 불안정한 테스트 진단                      | `test-engineer`     |
| 인증·인가·외부 노출 API 변경 후 보안 검토                   | `security-reviewer` |
| 여러 관심사가 섞인 변경을 원자 커밋으로 나누기              | `git-master`        |
| `docs/`, 모듈 README, `CLAUDE.md`/`AGENTS.md` 작성          | `writer`            |

## 항상 지키는 것

**언어** — 커밋 메시지, 주석, 문서는 한국어. 식별자와 로그 메시지는 영어.

**문서 위치** — 공용 문서는 `docs/`, 모듈 종속 문서는 `<그룹>/docs/`에 둔다.
코드 컨벤션을 `.claude/` 아래에 만들지 않는다. 사람과 다른 AI 도구도 읽어야 하므로 `docs/conventions/`에 쓴다.

**커밋** — `type(scope): 한국어 요약`. **`Co-Authored-By` 라인을 넣지 않는다.**
커밋·푸시 전에 사람에게 확인받는다. 자동 승인 모드여도 마찬가지다.
`git add .`를 쓰지 않고 변경한 파일을 명시적으로 지정한다.

**검증** — "완료"라고 말하기 전에 해당 모듈의 테스트·빌드를 돌리고 결과 건수로 보고한다.

## 하지 않는 것

- 요청하지 않은 리팩토링을 하지 않는다. 인접 코드의 스타일·주석·포맷을 "개선"하지 않는다.
  기존 코드에서 문제를 발견하면 고치지 말고 알린다.
- `.env`, `**/secrets/**`를 읽거나 고치지 않는다 (`.claude/settings.json`의 deny와 훅이 강제한다).
- `<그룹>/docs/ops/`의 운영 절차 문서를 임의로 고치지 않는다 (훅이 차단한다. 사람이 관리한다).
