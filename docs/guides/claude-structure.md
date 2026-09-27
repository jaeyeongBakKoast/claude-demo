# Claude Code 저장소 구조 가이드

이 견본이 **왜 이렇게 생겼는지**를 설명한다. 공식 문서와 공개 저장소를 조사한 결과(2026-09 기준)와
실제 멀티 모듈 프로젝트에서 운영한 경험을 합쳤다. 출처는 문서 끝에 있다.

## 1. 핵심 원칙

1. **로드 시점이 곧 비용이다.** 항상 로드되는 곳(루트 CLAUDE.md)에는 모든 작업에 필요한 것만 둔다.
   나머지는 필요할 때 로드되는 곳(모듈 CLAUDE.md, 경로 스코프 rule, skill, agent)으로 보낸다.
2. **한 사실은 한 곳에만.** 코드 컨벤션은 `docs/conventions/`에만 쓴다. `.claude/`에서는 가리키기만 한다.
   두 곳에 쓰면 반드시 어긋난다.
3. **요청과 보장을 구분한다.** CLAUDE.md의 "하지 마라"는 요청이다. 반드시 지켜야 하면 훅·`permissions.deny`로 강제한다.
4. **도구 중립 정보는 AGENTS.md에.** Cursor·Codex 등도 읽는다. CLAUDE.md는 첫 줄에 `@AGENTS.md`로 가져온다.
5. **적게 시작해서 필요할 때 늘린다.** 쓰이지 않는 skill·agent도 description이 매 세션 공간을 차지한다.

## 2. 무엇을 어디에 두는가

| 성격 | 위치 | 로드 시점 |
|---|---|---|
| 도구 중립 개요·구조·빌드 | `AGENTS.md` | CLAUDE.md의 `@AGENTS.md`로 항상 |
| 모든 작업에 필요한 규칙·문서 인덱스·위임 표 | 루트 `CLAUDE.md` | 항상 (`/compact` 뒤에도) |
| 모듈 그룹 공통 (동작 환경, 모듈 간 계약) | `<그룹>/CLAUDE.md` | 그 그룹 파일을 처음 읽을 때 |
| 한 모듈의 명령·구조·함정 | `<그룹>/<모듈>/CLAUDE.md` | 그 모듈 파일을 처음 읽을 때 |
| 파일 유형·경로별 규칙 | `.claude/rules/*.md` + `paths:` | 매칭 파일을 읽을 때 |
| 가끔 필요한 절차 | `.claude/skills/<이름>/SKILL.md` | description 항상, 본문은 쓸 때 |
| 한 그룹 전용 절차 | `<그룹>/.claude/skills/` | 그 그룹 파일을 처음 읽을 때 발견 |
| 결과 요약만 필요한 부수 작업 | `.claude/agents/*.md` | 위임 시 별도 컨텍스트 |
| 반드시 지켜야 하는 것 | `.claude/hooks/` + `settings.json` | 도구 호출 전후 |
| 사람과 공유할 코드 컨벤션 | `docs/conventions/` | 인덱스 표를 보고 읽을 때 |
| 개인 설정 | `CLAUDE.local.md`, `.claude/settings.local.json` | 커밋하지 않음 |

### 모듈 CLAUDE.md와 경로 스코프 rule 중 무엇을 쓰나

- **모듈 CLAUDE.md**: 그 폴더 소유자가 관리하는 모듈 고유 정보 (명령, 구조, 함정).
- **rule**: 여러 모듈에 흩어진 같은 종류의 파일에 적용되는 규칙 (예: 모든 `src/test/java/**`, 모든 매퍼 XML).

## 3. 로딩 동작에서 주의할 것

- **하위 폴더 CLAUDE.md는 지연 로드된다.** 시작 디렉터리와 그 상위는 시작 시, 하위는 그 폴더 파일을 읽을 때.
- **`/compact` 뒤에는 루트 CLAUDE.md만 다시 읽힌다.** 모듈 CLAUDE.md와 rule은 해당 파일을 다시 읽을 때 복구된다.
- **`@import`는 컨텍스트를 줄이지 않는다.** import한 파일도 시작 시 전부 로드된다(최대 4단계).
- **`rules/`의 frontmatter는 `paths`만 읽는다.** 없거나 YAML이 깨지면 항상 로드된다.
- **`.claude/settings.json`은 상위 폴더에서 상속되지 않는다.** 훅·권한은 루트 한 곳에 둔다.
  그룹 `.claude/`에는 `skills/`만 둔다.
- **CLAUDE.md가 있으면 AGENTS.md는 자동 로드되지 않는다.** 그래서 `@AGENTS.md` import를 쓴다.
  `ln -s AGENTS.md CLAUDE.md` 심링크는 Windows 클론에서 깨지고 Edit·Write가 막혀 권하지 않는다.
- **`.claude/commands/`는 예전 형식이다.** 새 슬래시 명령은 skill로 만든다 (`name`, `paths`, 부속 파일 지원).

## 4. 작성 기준

### CLAUDE.md
- 루트 200줄 이하. 한 줄마다 "이 줄을 지우면 Claude가 실수하는가?"
- 넣을 것: 추측할 수 없는 명령, 기본값과 다른 스타일, 테스트 방법, 저장소 관례, 함정.
- 뺄 것: 코드를 읽으면 알 수 있는 것, 표준 관례, 파일별 설명, 자주 바뀌는 정보.
- "IMPORTANT", 굵은 글씨는 아껴 쓴다. 모든 게 중요하면 아무것도 중요하지 않다.

### description (skill · agent)
- **"언제 쓰는가"만.** `Use when …` + `Do NOT use for …`. 저장소 경로를 넣어 내장 도구와 구분한다.
- **워크플로를 요약하지 않는다.** 요약이 있으면 모델이 본문을 읽지 않고 요약대로 행동한다.
- 요청에 나올 단어로 시작한다. 스킬이 많아지면 description이 잘린다.

### skill
- `name`은 디렉터리명과 같게 (Agent Skills 표준). `SKILL.md` 500줄 이하, 넘으면 `references/`로.
- 부수효과(커밋·배포)가 있으면 `disable-model-invocation: true`.
- 좋은 skill은 **결정을 대신 내려 준다** — "정해진 것" 절에 매번 다시 고민하지 않을 선택을 적는다.

### agent
- 읽기 전용 에이전트는 `disallowedTools: [Write, Edit]`.
- 모델은 역할에 맞게: 탐색·문서 `haiku`, 구현·디버깅 `sonnet`, 설계·보안 `opus`.
- 커밋·푸시하는 에이전트는 "사용자 확인이 명시되지 않으면 실행하지 않는다"를 본문에 둔다.

### hook
- 입력은 stdin JSON (`tool_input.file_path` 등). `exit 2`는 차단하고 stderr가 Claude에게 전달된다.
- 스크립트 경로는 `"$CLAUDE_PROJECT_DIR/.claude/hooks/x.sh"`로 참조한다.
- 도구가 설치되지 않은 환경에서는 조용히 통과(`exit 0`)하게 만든다. 훅이 개발을 막으면 사람들이 끈다.

## 5. 확장 단계

| 상황 | 다음 단계 |
|---|---|
| 같은 skill·agent를 두 번째 저장소에서도 쓰고 싶다 | 공용 자산을 플러그인으로 묶어 marketplace로 배포 (`.claude-plugin/plugin.json`) |
| 외부 시스템(이슈 트래커, DB)을 Claude가 조회해야 한다 | 저장소 루트 `.mcp.json`. 비밀값은 `${VAR}`로 |
| 워크트리에서 `.env` 같은 무시 파일이 필요하다 | `.worktreeinclude` (gitignore 문법) |
| 어떤 rule·CLAUDE.md가 실제로 로드됐는지 확인하고 싶다 | `/context`, 또는 `InstructionsLoaded` 훅 |

## 6. 공개 저장소에서 참고한 패턴

| 저장소 | 가져온 것 |
|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | skill 폴더 구조, `references/` 분리, 표준 frontmatter |
| [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) | `.claude/` 전체 구성 예, PostToolUse lint 훅, PreToolUse 보호 훅 |
| [obra/superpowers](https://github.com/obra/superpowers) | "설계 → 계획 → 구현" 프로세스 skill, description 작성법 |
| [wshobson/agents](https://github.com/wshobson/agents) | 역할별 소형 에이전트, 작업 난이도별 모델 배정 |
| [centminmod/my-claude-code-setup](https://github.com/centminmod/my-claude-code-setup) | `.worktreeinclude` 사용 예 (메모리 뱅크 다중 import 패턴은 200줄 기준과 충돌해 채택하지 않음) |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 커뮤니티 자산 색인 |

## 출처

- 메모리·CLAUDE.md·rules: https://code.claude.com/docs/en/memory
- 대규모 코드베이스·모노레포: https://code.claude.com/docs/en/large-codebases
- 베스트 프랙티스: https://code.claude.com/docs/en/best-practices
- Skills: https://code.claude.com/docs/en/skills , 표준 https://agentskills.io/specification
- Subagents: https://code.claude.com/docs/en/sub-agents
- Hooks: https://code.claude.com/docs/en/hooks , https://code.claude.com/docs/en/hooks-guide
- 권한·설정: https://code.claude.com/docs/en/permissions , https://code.claude.com/docs/en/settings
- 기능별 선택 기준: https://code.claude.com/docs/en/features-overview
- 플러그인: https://code.claude.com/docs/en/plugins
- AGENTS.md 표준: https://agents.md/
- Agent Skills 소개: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
