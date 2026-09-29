---
name: product-discovery
description: "Use when starting a new product or epic, or when docs/product/ is still empty or placeholder: '요구사항 정리해줘', '유스케이스 뽑아줘', 'RFP 분석해서 백로그 만들어줘', '액터 정의', '초기 ERD'. Builds the skeleton of actors, requirements backlog, use-case list, screen list and initial ERD. Do NOT use for a single feature change (story-new) or for detailing one use case/screen (story-design)."
argument-hint: "[RFP·과업지시서·회의록 경로 또는 설명]"
---

# 제품 분석 뼈대 만들기 (인셉션)

`docs/product/`의 **뼈대**를 만든다. 전부 상세화하지 않는다 — 유스케이스·화면은 제목과 한 줄 설명만.
상세화는 각 스토리의 `story-design`에서 한다. 이 원칙이 애자일을 지키는 핵심이다.

문서 지도와 ID 체계는 [docs/product/README.md](../../../docs/product/README.md)를 먼저 읽는다.

## 입력

| 항목 | 규칙 |
|---|---|
| 원천 자료 | RFP·과업지시서·회의록·기존 시스템. 없으면 사용자와 대화로 모은다 |
| 기존 문서 | `docs/product/`에 실제 내용이 있으면 **덮어쓰지 않고** 추가·수정만 한다 |
| 기존 DDL | `*/docs/database/`에 있으면 ERD는 DDL에서 역으로 그린다 |

## 절차

1. **액터** — 사람·시스템·시간 액터를 찾아 `actors.md`에 쓴다.
2. **요구사항** — 원천 자료를 한 행 한 요구로 쪼개 `requirements.md`에 쓴다.
   - 기능 `REQ-F`, 비기능 `REQ-N`. 모든 행에 **출처**(RFP 항목 번호 등)를 적는다.
   - 비기능은 **측정 기준**을 반드시 적는다. 모호하면 질문 목록에 넣는다.
   - 우선순위는 사용자에게 확인받기 전까지 제안값이고, 상태는 `proposed`.
3. **유스케이스 목록** — `use-cases/README.md` 표와 Mermaid 개요도. 명세 파일은 만들지 않는다.
4. **화면 목록** — 웹 화면 기준으로 `screens/README.md` 표와 화면 흐름도. URL은 제안값.
5. **ERD** — 핵심 엔티티와 관계만 `erd.md`에. DDL이 없으면 "초안"이라고 표시한다.
6. **아키텍처** — `architecture.md`의 시스템 구성도를 실제 모듈에 맞춘다.
7. **추적표** — `traceability.md`에 REQ별 행을 만들고 UC·SCR을 연결한다.

## 멈추고 확인받기

다음을 보여주고 **승인을 기다린다**:
- 요구사항 표 (우선순위 제안 포함)와 출처가 불분명한 항목
- 질문 목록 (모호한 요구, 빠진 비기능 요구, 액터 권한)
- 첫 스토리로 가져갈 후보 REQ 3개 (Must 중 의존성이 적은 것)

승인되면 합의된 REQ의 상태를 `accepted`로 바꾼다.

## 하지 않는 것

- 유스케이스 명세·화면 정의 파일을 미리 만들지 않는다.
- 코드를 만들지 않는다.
- 출처 없는 요구사항을 지어내지 않는다. 필요해 보이면 "제안"으로 표시하고 질문한다.
