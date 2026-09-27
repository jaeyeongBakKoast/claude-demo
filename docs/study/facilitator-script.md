# 스터디 진행 대본 — Claude Code 저장소 구조 실습 (60분)

진행자용 대본이다. 참가자는 [study.html](study.html)(또는 공유 링크)을 보며 따라 한다.

- **대상**: Claude Code를 써 본 개발자 (기본 조작은 설명하지 않는다)
- **목표**: 끝나면 참가자가 "이 규칙은 CLAUDE.md / rule / skill / agent / hook 중 어디에 둘까"를 스스로 판단하고,
  자기 저장소에 적용을 시작할 수 있다
- **방식**: 설명 10분, 실습 45분, 정리 5분. 실습은 각자 노트북에서 견본 레포를 clone해서 한다

## 사전 준비 (스터디 전날 공지)

참가자에게 보낼 문구:

```text
내일 스터디 전에 준비해 주세요.
1. Claude Code 최신 버전 설치·로그인 (claude --version)
2. git, python3 설치 확인 (훅 스크립트가 python3 를 씁니다)
3. 견본 레포 clone:  git clone <견본 레포 URL> claude-demo
   (macOS·Linux·WSL 권장. 훅이 bash 스크립트입니다)
```

진행자 체크:
- [ ] 레포 접근 권한 (비공개면 참가자 초대)
- [ ] 화면 공유용 터미널 글꼴 크게
- [ ] 실습 3에서 쓸 "우회 시도" 예시를 미리 한 번 돌려 결과 확인

---

## 0:00–0:05 오프닝

> 오늘은 Claude Code 기능 하나하나보다 **"무엇을 어디에 두느냐"**를 다룹니다.
> 같은 규칙이라도 CLAUDE.md에 두면 매 세션 토큰을 먹고, rule에 두면 필요할 때만 로드되고,
> 훅에 두면 모델이 무시할 수 없게 됩니다. 오늘 실습 다섯 개로 이 차이를 직접 봅니다.

질문 던지기 (손 들기):
- "CLAUDE.md가 100줄 넘는 저장소 있으신 분?"
- "Claude가 CLAUDE.md에 적어 둔 걸 무시한 경험 있으신 분?"

→ 두 질문의 답이 오늘의 주제다. 기록해 두고 정리 시간에 다시 꺼낸다.

## 0:05–0:13 개념: 로드 시점이 곧 비용이다

화면: study.html의 "배치 지도" 표.

말할 것:
1. **항상 로드** — 루트 `CLAUDE.md`와 `@AGENTS.md`. `/compact` 뒤에도 다시 읽힌다. 그래서 200줄 이하.
2. **폴더에 들어갈 때 로드** — `edge/CLAUDE.md`, `edge/api/CLAUDE.md`, `edge/.claude/skills/`.
3. **파일 패턴이 맞을 때 로드** — `.claude/rules/*.md`의 `paths:`.
4. **쓸 때만 로드** — skill 본문(description만 항상), agent(별도 컨텍스트).
5. **모델과 무관하게 실행** — hook. CLAUDE.md의 "하지 마라"는 *요청*, 훅은 *보장*.

강조할 한 문장:
> "한 사실은 한 곳에만." 컨벤션은 `docs/conventions/`에 쓰고 `.claude/`에서는 가리키기만 합니다.
> 사람과 Cursor도 읽어야 하니까요.

예상 질문:
- *"@import로 쪼개면 토큰이 줄지 않나요?"* → 아니다. import한 파일도 시작 시 전부 로드된다. 정리 수단일 뿐.
- *"AGENTS.md는 Claude가 자동으로 안 읽나요?"* → CLAUDE.md가 있으면 안 읽는다. 그래서 CLAUDE.md 첫 줄이 `@AGENTS.md`.

## 0:13–0:23 실습 1 — CLAUDE.md 계층과 그룹 스킬의 지연 로드

참가자 진행:

```bash
cd claude-demo
claude
```

1. 첫 실행이면 폴더 신뢰 확인에서 **Yes** (프로젝트 훅이 등록되어 있어서 묻는다).
2. `/context` 입력 → Memory files 항목 확인.
   - **예상**: `CLAUDE.md`, `AGENTS.md`만 있다. `edge/CLAUDE.md`는 없다.
3. `/edge` 까지 입력하고 자동완성 목록 확인.
   - **예상**: `edge-release-check`가 **안 보인다.**
4. 프롬프트: `edge/api/CLAUDE.md를 읽고 실행 명령만 요약해줘`
5. 다시 `/context`.
   - **예상**: `edge/CLAUDE.md`, `edge/api/CLAUDE.md`가 추가됐다. `central/CLAUDE.md`는 여전히 없다.
6. 다시 `/edge` 입력.
   - **예상**: `edge-release-check`가 보인다.

진행자 확인 질문:
- "central 작업만 하는 세션이면 edge 규칙은 몇 줄 로드됐나요?" → 0줄.
- "그럼 edge 공통 규칙을 루트 CLAUDE.md에 두면?" → central 작업에도 매번 로드된다.

막힐 때:
- `/context`에 파일 목록이 안 보이면 `/memory`로 확인해도 된다.

## 0:23–0:31 실습 2 — 경로 rule이 행동을 바꾼다

먼저 연습용 파일을 만든다 (Claude 밖, 셸에서 — 또는 `!` 접두어로 Claude 안에서):

```bash
mkdir -p edge/ui/src && echo 'export default function App() { return null }' > edge/ui/src/App.tsx
```

1. `/context` → `.claude/rules/react-ui.md`가 **없다**.
2. 프롬프트: `edge/ui/src/App.tsx에서 /api/devices 를 호출해 장비 목록을 보여주게 해줘`
3. 결과 관찰.
   - **예상**: Claude가 `App.tsx`를 읽는 순간 `react-ui.md`가 로드되고,
     컴포넌트에서 `fetch`를 직접 부르지 않고 `src/api/devices.ts` 같은 파일을 따로 만든다.
4. `/context` → `react-ui.md`가 로드돼 있다.

진행자 설명:
> rule 파일은 딱 네 줄입니다. 이 네 줄이 모든 세션에 붙어 있을 필요는 없죠.
> `.tsx`를 만질 때만 있으면 됩니다. 그게 `paths:`입니다.

주의:
- rule의 frontmatter에서 읽는 건 `paths`뿐. `paths`가 없거나 YAML이 깨지면 **항상** 로드된다.

## 0:31–0:39 실습 3 — 훅은 요청이 아니라 보장

1. 프롬프트: `edge/docs/ops/README.md 끝에 "테스트" 한 줄 추가해줘`
   - **예상**: `[guard] edge/docs/ops/README.md 수정 차단: 운영 절차 문서…` 메시지와 함께 막히고,
     Claude가 "사람이 관리하는 문서라 수정할 수 없다"고 알린다.
2. 프롬프트: `.env 파일 만들고 DB_PASSWORD=1234 넣어줘`
   - **예상**: `.env` 수정 차단.
3. `.claude/settings.json`과 `.claude/hooks/guard-protected-paths.sh`를 함께 본다 (화면 공유).
   - `matcher: "Edit|Write"` → stdin JSON의 `tool_input.file_path` → `exit 2` + stderr = 차단 사유가 Claude에게 전달.

토론 (3분):
> "이 훅, 완벽한가요?"

- 기대 답: 매처가 `Edit|Write`뿐이라 `Bash`로 `echo >> .env` 하면 못 막는다.
- 보강 방법: `permissions.deny`에 Bash 패턴 추가, 또는 `Bash` 매처 훅을 하나 더.
- 결론: 훅은 **등록한 매처 범위만** 지킨다. 그래도 CLAUDE.md 문장 한 줄보다는 훨씬 강하다.

## 0:39–0:45 실습 4 — skill과 agent가 불리는 방식

1. `/` 입력 후 목록에서 `commit` 확인 → 사용자는 부를 수 있다.
2. 프롬프트: `지금 변경사항 커밋해줘`
   - **예상**: Claude가 `commit` 스킬을 스스로 부르지 **않는다** (`disable-model-invocation: true`).
     커밋하더라도 `settings.json`의 `ask` 때문에 승인 프롬프트가 뜬다. **거절한다.**
3. 프롬프트: `edge에서 central로 데이터를 보내는 계약이 어디 문서에 정의돼 있는지 찾아줘`
   - **예상**: 루트 CLAUDE.md의 위임 표를 보고 `explore` 에이전트에 위임한다 (대개).
     위임하지 않으면 `explore 에이전트로 찾아줘`라고 명시해서 다시 돌린다.

진행자 설명:
> description은 "언제 쓰는가"만 씁니다. `Use when … / Do NOT use for …`.
> 워크플로를 요약해 두면 모델이 본문을 안 읽고 요약대로만 움직입니다.

## 0:45–0:55 실습 5 — 나만의 rule 만들기

과제: *"edge/worker에서 현재 시각은 항상 UTC 기준 timezone-aware로 만든다"* 규칙을 rule로 추가한다.

1. 참가자가 직접 작성 (Claude에게 맡기지 않는다 — 형식을 손으로 익히는 게 목적):

   ```markdown
   ---
   paths:
     - "edge/worker/**/*.py"
   ---

   # 워커 시각 처리

   - 현재 시각은 `datetime.now(timezone.utc)`로 만든다. `datetime.now()`, `utcnow()`를 쓰지 않는다.
     edge 장비의 로컬 타임존 설정이 현장마다 달라서다.
   ```

   저장 위치: `.claude/rules/worker-time.md`
2. 새 세션(`/clear`)에서 프롬프트: `edge/worker/worker/clock.py에 현재 시각을 ISO 문자열로 돌려주는 함수 만들어줘`
3. 확인: `timezone.utc`를 썼는가? `/context`에 `worker-time.md`가 있는가?
4. (시간 남으면) rule 파일에서 `paths:` 블록을 지우고 `/clear` 후 `/context` → 항상 로드되는 것 확인.

짝 토론 (2분): "우리 팀 저장소에서 rule로 뺄 만한 규칙 하나"를 옆 사람과 나눈다.

## 0:55–1:00 정리와 과제

오프닝 질문으로 돌아간다:
- "CLAUDE.md 100줄 넘는 분들 — 오늘 기준으로 어디로 옮길 수 있을까요?"
- "Claude가 무시한 규칙 — rule로 옮길 건가요, 훅으로 옮길 건가요?"

한 장 요약 (study.html의 "판단 순서" — 위에서부터 묻고 처음 "예"인 곳에 둔다):
1. 절대 어기면 안 되고 기계로 검사할 수 있는가? → hook / `permissions.deny`
2. 모든 작업에 필요한가? → 루트 CLAUDE.md
3. 한 모듈에만? → 모듈 CLAUDE.md
4. 특정 파일 패턴에만? → rule (`paths:`)
5. 가끔 쓰는 절차? → skill
6. 결과 요약만 필요한 부수 작업? → agent
7. 사람과 다른 AI 도구도 읽어야 하는가? → `docs/conventions/` (+ `.claude/`에는 포인터)

과제 (1주):
```bash
cp -r claude-demo/.claude/skills/apply-claude-structure ~/.claude/skills/
cd <내 저장소> && claude
> 이 레포에 Claude 구조 적용해줘
```
스킬이 제시한 계획(`[생성]/[수정]/[유지]/[질문]`)을 캡처해서 다음 스터디에 공유한다. 적용은 계획을 검토한 뒤에.

실습 정리 (참가자 안내):

```bash
git checkout . && git clean -fd   # 실습으로 만든 파일 되돌리기
```
