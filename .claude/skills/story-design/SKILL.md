---
name: story-design
description: "Use when the current story's status is ready and the user wants to design it ('설계해줘', '다음 단계', '어떻게 만들지 정리해줘'). Details only the use cases, screens, APIs, interfaces and ERD/DDL this story touches, then writes design.md with a task checklist and stops for approval. Do NOT use before acceptance criteria are approved (story-new) or to write production code (story-build)."
argument-hint: "[S-###]"
---

# 스토리 설계

이 스토리가 **건드리는 제품 문서만** 상세화하고, 작업 목록을 만든다. 코드는 쓰지 않는다.

## 입력

- 현재 스토리: 브랜치 이름의 `S-###` 또는 인자. `story.md`의 `status`가 `ready`가 아니면 멈추고 알린다.
- 관련 코드: 영향 범위를 모르면 `explore` 에이전트에 맡긴다. 구조 판단이 필요하면 `architect`.

## 절차

1. `story.md`의 수용 기준과 연결된 REQ·UC·SCR을 읽는다.
2. **제품 문서를 먼저 고친다** (이 스토리에 해당하는 것만):
   - 유스케이스 명세 `docs/product/use-cases/UC-###-slug.md` — 없으면 `_templates/use-case.md`로 만든다. 기본·대안·예외 흐름이 수용 기준과 맞아야 한다
   - 화면 정의 `docs/product/screens/SCR-###-slug.md` — 없으면 `_templates/screen.md`로. 와이어프레임, 요소, 동작, 호출 API, 메시지
   - `api.md`(화면↔서버), `interfaces.md`(시스템 간) — 경로·메서드·권한·필드
   - DB가 바뀌면 DDL(`<그룹>/docs/database/`)과 `erd.md`를 함께 고친다. 공통 코드면 `code-definitions.md`
   - 목록 문서(`use-cases/README.md`, `screens/README.md`)의 "명세/정의" 칸에 링크
3. `docs/stories/_template/design.md`로 `design.md`를 쓴다.
   - 영향 범위 표는 2번에서 고친 문서와 고칠 코드 경로
   - 테스트 계획: 수용 기준마다 시험 방법과 위치
   - **작업 목록**: 한 작업 = 한 번에 검증할 수 있는 단위. 각 작업에 완료 기준
4. 레이어·명명은 `docs/conventions/`를 따른다. 테이블 기반 CRUD면 `scaffolding-crud-api` 스킬 사용을 작업에 적는다.

## 멈추고 확인받기 (승인 ②)

접근 방식, 바뀐 제품 문서 목록, 작업 목록을 보여주고 기다린다. 승인되면:
- `story.md`의 `status: designed`, `design.md` "승인" 절에 날짜와 승인자
- 다음 단계로 `story-build`를 안내한다

## 하지 않는 것

- 이 스토리와 관계없는 유스케이스·화면을 상세화하지 않는다.
- 프로덕션 코드를 쓰지 않는다.
