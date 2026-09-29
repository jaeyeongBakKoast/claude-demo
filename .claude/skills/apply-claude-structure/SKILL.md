---
name: apply-claude-structure
description: "Use when asked to apply, set up or migrate a repository to this Claude Code layout: 'Claude 구조 적용해줘', '이 레포에 CLAUDE.md·rules·skills 세팅해줘', 'set up Claude Code for this repo', or when auditing an existing CLAUDE.md/.claude setup against it. Works on new or existing multi-module repos. Do NOT use for editing a single rule/skill/agent (edit it directly) or for general code changes."
argument-hint: "[대상 저장소 경로 (기본: 현재 디렉터리)]"
---

# 저장소에 Claude Code 구조 적용

대상 저장소를 조사해 **계획을 먼저 보여주고, 승인받은 뒤에만** 파일을 만든다.
기존 파일을 덮어쓰지 않는다. 이 스킬의 가치는 "무엇을 어디에 둘지"를 매번 다시 고민하지 않게 하는 데 있다.

배치 원칙의 근거는 [references/placement.md](references/placement.md), 파일 틀은 [references/templates/](references/templates/)에 있다.

## 1단계 — 조사 (파일을 만들지 않는다)

다음을 확인하고 표로 정리한다.

| 항목 | 확인 방법 |
|---|---|
| 모듈 목록과 스택 | 빌드 파일(`build.gradle*`, `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml` …)의 위치 |
| 모듈 그룹 | 모듈이 2단계(`<그룹>/<모듈>`)로 묶여 있는지 |
| 모듈별 명령 | 빌드·테스트·lint·실행 명령. `package.json` scripts, Gradle 태스크, Makefile |
| 기존 AI 지침 | `CLAUDE.md`(모든 위치), `AGENTS.md`, `.cursor/rules/`, `.cursorrules`, `.github/copilot-instructions.md`, `.claude/` |
| 기존 컨벤션 문서 | `CONTRIBUTING.md`, `docs/` 아래 스타일 가이드, lint 설정 |
| 보호할 파일 | `.env*`, 비밀값 폴더, 사람이 관리하는 운영 문서, 생성 코드·산출물 폴더 |
| git 상태 | 커밋되지 않은 변경이 있으면 알리고 계속할지 묻는다 |

기존 지침이 있으면 **내용을 버리지 않는다.** 아래 매핑으로 옮길 위치만 정한다.

| 기존 내용 | 옮길 위치 |
|---|---|
| 프로젝트 개요, 구조, 빌드 명령 (도구 중립) | `AGENTS.md` |
| Claude 전용 규칙, 문서 인덱스, 위임 표, 금지사항 | 루트 `CLAUDE.md` |
| 스택별 코드 스타일 | `docs/conventions/<스택>.md` |
| 특정 경로에만 해당하는 규칙 (`.cursor/rules`의 globs 규칙 등) | `.claude/rules/<주제>.md` (`paths:`) |
| 한 모듈의 명령·구조·함정 | `<모듈>/CLAUDE.md` |
| 반복 절차 ("~할 때는 이 순서로") | `.claude/skills/<이름>/` |
| "절대 ~하지 마라" 중 기계로 검사 가능한 것 | 훅 또는 `permissions.deny` |

## 2단계 — 계획 제시 후 멈춤

아래 형식으로 보여주고 **사용자 승인을 기다린다.** 승인 없이 3단계로 가지 않는다.

```text
[생성] 경로 — 한 줄 이유
[수정] 경로 — 무엇을 바꾸는지 (기존 내용은 어디로 옮기는지)
[유지] 경로 — 손대지 않는 이유
[질문] 결정이 필요한 것 (예: 커밋 컨벤션, 문서 언어, 보호할 폴더,
       스토리 흐름·산출물 체계(docs/product, docs/stories, story-* 스킬) 도입 여부)
```

## 3단계 — 적용 (승인 후)

순서대로 만든다. 각 파일은 `references/templates/`의 틀에서 시작하고, `<...>` 자리는 1단계 조사 결과로 채운다.
**조사로 확인하지 못한 명령은 지어내지 않는다.** `<확인 필요>`로 남기고 마지막에 목록으로 보고한다.

1. `AGENTS.md` ← `templates/AGENTS.md`
2. 루트 `CLAUDE.md` ← `templates/CLAUDE.root.md` (첫 줄 `@AGENTS.md`, 200줄 이하)
3. 모듈마다 `<모듈>/CLAUDE.md` ← `templates/CLAUDE.module.md`
4. `docs/conventions/README.md`와 스택별 문서. 기존 스타일 문서가 있으면 옮기고, 없으면 틀만 만든다
5. `.claude/rules/` ← `templates/rule.md`. 주제당 한 파일, `paths` 필수. 처음엔 3–5개로 시작한다
6. `.claude/settings.json` ← `templates/settings.json`. 보호할 파일을 `deny`에, 명령을 `allow`에
7. `.claude/hooks/` ← `templates/hooks/`. 보호 경로 차단(PreToolUse), 바뀐 파일 lint(PostToolUse).
   `guard`의 `case` 패턴과 `lint`의 `UI_MODULES`·`PY_MODULES`를 조사 결과로 채우고 `chmod +x` 한다.
   스토리 흐름을 도입하기로 했으면 `story-context.sh`(UserPromptSubmit)도 넣는다. 도입하지 않으면 `settings.json`에서 그 항목을 뺀다
8. `.claude/agents/` — 처음엔 `explore`, `debugger`만. 나머지는 필요가 보일 때 추가한다
9. `.gitignore`에 `templates/gitignore.snippet` 추가
10. 기존 `.cursor/rules` 등은 지우지 않는다. 옮긴 뒤 원본을 어떻게 할지 사용자에게 묻는다

에이전트·스킬을 한꺼번에 많이 만들지 않는다. 쓰이지 않는 자산은 description 공간만 차지한다.

## 4단계 — 검증

- 루트 `CLAUDE.md` 줄 수 (`wc -l`) — 200 이하
- 모든 `.claude/rules/*.md`에 `paths:`가 있는지 (`grep -L '^paths:' .claude/rules/*.md`는 빈 출력이어야 한다)
- `settings.json`이 올바른 JSON인지 (`python3 -m json.tool .claude/settings.json`)
- 훅 스크립트에 가짜 입력을 넣어 동작 확인:
  `echo '{"tool_input":{"file_path":"'$PWD'/.env"}}' | CLAUDE_PROJECT_DIR=$PWD bash .claude/hooks/guard-protected-paths.sh; echo $?` → `2`
- `git status`로 커밋될 파일 확인 — `settings.local.json`, `CLAUDE.local.md`가 목록에 없어야 한다

## 보고

만든 파일 / 고친 파일 / `<확인 필요>`로 남긴 항목 / 사용자가 다음에 할 일(명령 검증, 커밋).
커밋은 하지 않는다. 사용자가 요청하면 `docs/conventions/commit.md`를 따른다.
