# 새 프로젝트·기존 프로젝트에 적용하기

두 가지 방법이 있다. **B(스킬로 적용)를 권한다.** 조사·계획·검증을 스킬이 대신 해 준다.

## A. 새 프로젝트 — 견본을 복사해서 시작

```bash
git clone <이 견본 저장소 URL> my-project
cd my-project && rm -rf .git && git init
```

1. `edge/`, `central/`을 실제 모듈 그룹 이름으로 바꾸고, 필요 없는 모듈 폴더를 지운다.
2. 저장소 전체에서 `<...>` 자리를 찾아 채운다: `grep -rn '<[^>]*>' --include='*.md' .`
3. 모듈 경로가 들어간 곳을 새 경로로 바꾼다:
   `CLAUDE.md` 인덱스·위임 표, `.claude/rules/*.md`의 `paths`,
   `.claude/hooks/lint-changed-file.sh`의 `UI_MODULES`·`PY_MODULES`, `.gitignore`의 그룹 `.claude` 줄,
   에이전트 description의 경로.
4. 아래 "검증"을 돌린다.

## B. 기존 프로젝트 — `apply-claude-structure` 스킬로 적용

스킬을 사용자 레벨에 한 번 설치하면 어떤 저장소에서든 쓸 수 있다.

```bash
cp -r <견본>/.claude/skills/apply-claude-structure ~/.claude/skills/
```

대상 저장소에서 Claude Code를 열고 요청한다.

```text
이 레포에 Claude 구조 적용해줘
```

스킬은 다음 순서로 진행한다.

1. **조사** — 모듈·스택·명령, 기존 `CLAUDE.md`/`AGENTS.md`/`.cursor/rules`/스타일 문서, 보호할 파일
2. **계획 제시 후 멈춤** — `[생성]`/`[수정]`/`[유지]`/`[질문]` 목록. 승인해야 다음으로 간다
3. **적용** — 템플릿으로 파일 생성. 기존 내용은 버리지 않고 알맞은 위치로 옮긴다. 확인 못 한 명령은 `<확인 필요>`로 남긴다
4. **검증** — 아래 항목을 자동으로 돌리고 결과 보고

커밋은 하지 않는다. 결과를 검토한 뒤 직접 또는 `/commit`으로 커밋한다.

### 기존 지침이 있을 때 옮기는 기준

| 기존 내용 | 옮길 위치 |
|---|---|
| 프로젝트 개요, 구조, 빌드 명령 | `AGENTS.md` |
| Claude 전용 규칙, 금지사항 | 루트 `CLAUDE.md` |
| 스택별 코드 스타일 | `docs/conventions/<스택>.md` |
| `.cursor/rules`의 globs 규칙 | `.claude/rules/<주제>.md`의 `paths` |
| 한 모듈의 명령·함정 | `<모듈>/CLAUDE.md` |
| 반복 절차 | `.claude/skills/<이름>/` |
| 기계로 검사 가능한 금지사항 | 훅 또는 `permissions.deny` |

## 단계적으로 도입하기

한 번에 모두 만들 필요 없다. 효과가 큰 순서:

1. **루트 `CLAUDE.md` + `AGENTS.md`** — 인덱스 표, 항상/금지. 이것만으로도 효과가 가장 크다
2. **모듈 `CLAUDE.md`** — Claude가 실제로 틀린 명령·함정부터 적는다
3. **`docs/conventions/`** — 기존 스타일 문서를 옮기거나 틀만 만든다
4. **훅 2개** — 보호 경로 차단, 바뀐 파일 lint
5. **rules 3–5개** — Claude가 반복해서 틀리는 것만
6. **agents** — `explore`, `debugger`부터. 위임할 일이 실제로 생기면 추가
7. **도메인 skill** — 같은 절차를 세 번 설명했으면 skill로
8. **스토리 흐름·산출물 체계** (선택) — `docs/product/`, `docs/stories/`, `story-*` 스킬, `story-context.sh` 훅.
   산출물 제출이 있는 공공 용역·R&D라면 권한다. 도입 절차는 [development-process.md 9절](development-process.md#9-기존-프로젝트에-도입하기)

## 검증

```bash
wc -l CLAUDE.md                                   # 200 이하
grep -L '^paths:' .claude/rules/*.md              # 빈 출력이어야 함
python3 -m json.tool .claude/settings.json >/dev/null && echo ok
chmod +x .claude/hooks/*.sh
echo "{\"tool_input\":{\"file_path\":\"$PWD/.env\"}}" \
  | CLAUDE_PROJECT_DIR=$PWD bash .claude/hooks/guard-protected-paths.sh; echo "exit=$?"   # exit=2
git status --short --ignored .claude              # settings.local.json 은 ignored 쪽에
```

Claude Code 안에서는 `/context`로 어떤 CLAUDE.md·rule이 로드됐는지, `/doctor`로 설정 오류를 확인한다.

## 운영하면서

- Claude가 같은 실수를 두 번 하면: 모듈 전용이면 모듈 CLAUDE.md, 경로 패턴이면 rule, 절대 안 되면 훅.
- 루트 CLAUDE.md가 200줄을 넘기면: 모듈 전용 내용을 모듈 CLAUDE.md로, 절차를 skill로 옮긴다.
- 분기마다 쓰이지 않는 skill·agent를 지운다.
