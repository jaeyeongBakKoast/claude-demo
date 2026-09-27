# AI 에이전트 가이드

Claude Code, Cursor, Codex 등 모든 AI 에이전트와 새로 합류한 사람이 이 저장소를 이해하는 데 필요한 정보를 담는다.
**도구 중립적으로 쓴다.** Claude Code 전용 규칙은 [CLAUDE.md](CLAUDE.md)에 둔다.

> 이 저장소는 **Claude Code 개발용 저장소 견본**이다. `<...>` 표시는 실제 프로젝트에 맞게 바꾼다.
> 적용 방법은 [docs/guides/adopting-existing-repo.md](docs/guides/adopting-existing-repo.md)를 본다.

## 프로젝트 개요

`<한두 문장으로 무엇을 만드는 시스템인지 쓴다.>`
예: 현장 장비(edge)에서 데이터를 수집·가공하고, 중앙 시스템(central)이 이를 받아 저장·조회·관리한다.

## 구조

```text
프로젝트 루트
├── docs/
│   ├── conventions/        스택별 코드 컨벤션 (모든 모듈·모든 도구 공용 SSOT)
│   └── guides/             Claude Code 구조 가이드, 기존 저장소 적용 절차
├── edge/                   현장 장비 시스템
│   ├── api/                Spring Boot — 수집 데이터 API, 중앙 전송
│   ├── ui/                 React — 현장 대시보드
│   ├── worker/             Python — 수집·가공 워커
│   └── docs/               edge 전용 문서
└── central/                중앙 시스템
    ├── api/                Spring Boot — 수신·저장·조회
    ├── ui/                 React — 운영 웹
    └── docs/               central 전용 문서
```

데이터 흐름:

```text
장비/센서 -> edge/worker -> edge/api (+ edge/ui) -> central/api -> central/ui
```

## 빌드·실행

`<실제 명령으로 바꾼다. 저장소 루트 기준으로 쓴다.>`

```bash
./gradlew :edge:api:test          # edge API 테스트
./gradlew :central:api:test       # central API 테스트
(cd edge/ui && npm run build)     # UI 빌드
(cd edge/worker && uv run pytest) # 워커 테스트
```

모듈별 명령·구조·주의점은 각 모듈의 `CLAUDE.md`에 있다. 사람도 읽을 수 있게 쓴다.

## 작업 규칙 (요약)

- 문서·주석·커밋 메시지는 한국어, 식별자와 로그 메시지는 영어
- 코드 컨벤션은 [docs/conventions/](docs/conventions/)가 기준이다. 작업 전에 해당 문서를 읽는다
- 커밋은 `type(scope): 한국어 요약` ([docs/conventions/commit.md](docs/conventions/commit.md))
- 요청하지 않은 리팩토링을 하지 않는다
