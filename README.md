# Claude Code 멀티 프로젝트 저장소 견본

여러 모듈로 구성된 저장소에서 Claude Code를 쓰기 위한 **CLAUDE.md · rules · skills · agents · hooks 배치 견본**이다.
실제 운영 중인 멀티 모듈 프로젝트(Spring Boot + React + Python)의 구조를 일반화하고,
공식 문서와 공개 저장소의 모범 사례로 보강했다.

코드는 들어 있지 않다. Claude 자산과 문서만 있어 새 프로젝트의 출발점으로도, 기존 프로젝트에 덮어쓸 참고로도 쓸 수 있다.

## 구조

```text
.
├── AGENTS.md                      도구 중립 개요 (Cursor·Codex·Claude 공용)
├── CLAUDE.md                      @AGENTS.md + Claude 전용 규칙 (항상 로드, 200줄 이하)
├── .claude/
│   ├── README.md                  무엇을 어디에 두는가
│   ├── settings.json              권한(allow/ask/deny) + 훅 등록
│   ├── hooks/                     보호 경로 차단(PreToolUse), 바뀐 파일 lint(PostToolUse)
│   ├── rules/                     paths 스코프 규칙 — 매칭 파일을 읽을 때만 로드
│   ├── agents/                    explore, debugger, architect, test-engineer, security-reviewer, git-master, writer
│   └── skills/
│       ├── apply-claude-structure/  ★ 기존 저장소에 이 구조를 적용하는 스킬 (+ 템플릿)
│       ├── product-discovery/       ★ 요구사항·액터·유스케이스·화면·ERD 뼈대
│       ├── story-new/ story-design/ story-build/ story-review/  ★ 스토리 단위 애자일 흐름
│       ├── deliverables-export/     제출본(HWPX·DOCX) 생성
│       ├── hwpxskill/               한글 HWPX (git submodule)
│       ├── scaffolding-crud-api/    도메인 워크플로 스킬 예시
│       └── commit/                  부수효과 스킬 예시 (사용자 호출 전용)
├── tools/deliverables/            테이블 정의서·프로그램 목록·단위 시험 결과서 생성 (Python 표준 라이브러리)
├── docs/
│   ├── product/                   ★ 요구사항·액터·UC·화면·API·IF·ERD·아키텍처·추적표
│   ├── stories/                   ★ 스토리별 story · design · review
│   ├── quality/                   시험 계획·결과, 성능, 보안·접근성
│   ├── manuals/                   사용자·운영자 매뉴얼
│   ├── deliverables/              ★ 공공 용역·R&D 산출물 목록표 ↔ 원본
│   ├── conventions/               코드 컨벤션 SSOT (사람·모든 AI 공용)
│   └── guides/
│       ├── claude-structure.md    ★ 베스트 프랙티스와 근거·출처
│       ├── development-process.md ★ 애자일 + 산출물 개발 프로세스
│       └── adopting-existing-repo.md  ★ 새/기존 프로젝트 적용 절차
├── edge/                          모듈 그룹 예시 1
│   ├── CLAUDE.md                  그룹 공통 (동작 환경, 모듈 간 계약)
│   ├── .claude/skills/            그룹 전용 스킬 (edge 파일을 읽을 때 발견)
│   ├── api/  ui/  worker/         각자 CLAUDE.md (명령·구조·함정)
│   └── docs/ops/                  사람만 수정하는 운영 문서 (훅이 보호)
└── central/                       모듈 그룹 예시 2
    ├── CLAUDE.md
    └── api/  ui/
```

## 로드 흐름

```text
세션 시작 ─ CLAUDE.md (+ AGENTS.md) ─ skill·agent description
   │
   ├─ edge/api/Foo.java 를 읽음 ─→ edge/CLAUDE.md, edge/api/CLAUDE.md, edge/.claude/skills 발견
   ├─ **/src/test/java/** 를 읽음 ─→ .claude/rules/java-tests.md
   ├─ 파일 수정 시도 ─→ PreToolUse 훅 (.env, docs/ops 차단) → PostToolUse 훅 (eslint/ruff)
   └─ "CRUD 만들어줘" ─→ scaffolding-crud-api 본문 로드
```

## 개발 흐름 (애자일 + 산출물)

```text
product-discovery ─→ 백로그(requirements.md)
      │
      ▼  스토리마다 (브랜치 feat/S-###-…)
story-new ─승인①→ story-design ─승인②→ story-build ─→ story-review ─수락③→ done
story.md          UC·화면·API·ERD 갱신    코드·테스트        review.md
                  design.md(작업 목록)     design.md 로그     추적표·통합시험
      │
      ▼  단계 말
/deliverables-export ─→ 요구사항 정의서, 화면 설계서, 테이블 정의서 … (HWPX·DOCX)
```

각 단계에서 Claude에게 뭐라고 말하고, 무엇이 생기고, 사람이 무엇을 승인하는지는
**[docs/guides/development-process.md](docs/guides/development-process.md)**에 있다 (공공 용역 단계·감리, R&D 대응 포함).

clone할 때 submodule(hwpxskill)도 받는다: `git clone --recurse-submodules <URL>`
(이미 받았으면 `git submodule update --init`).

## 쓰는 법

- **처음 읽을 문서**: [docs/guides/claude-structure.md](docs/guides/claude-structure.md) (구조), [docs/guides/development-process.md](docs/guides/development-process.md) (개발 프로세스·산출물)
- **적용하기**: [docs/guides/adopting-existing-repo.md](docs/guides/adopting-existing-repo.md)
  — 새 프로젝트는 복사 후 `<...>` 채우기, 기존 프로젝트는 `apply-claude-structure` 스킬 사용
- **팀 스터디(60분 실습)**: [docs/study/study.html](docs/study/study.html) (참가자용), [docs/study/facilitator-script.md](docs/study/facilitator-script.md) (진행자 대본)

`<...>` 표시는 실제 프로젝트 값으로 바꿀 자리다.
