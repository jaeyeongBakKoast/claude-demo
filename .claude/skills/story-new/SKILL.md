---
name: story-new
description: "Use when the user asks to add or change a feature, screen or API in this repo ('~ 기능 추가해줘', '~ 화면 만들어줘', '~ 되게 해줘', '새 스토리'), or picks a requirement from the backlog, and no story exists yet on the current branch. Writes docs/stories/S-###/story.md with acceptance criteria and stops for approval. Do NOT use for questions, typo/doc-only edits, config tweaks, or when a story for this work already exists."
argument-hint: "[REQ-F-### 또는 기능 설명]"
---

# 스토리 시작

스토리와 **수용 기준**을 쓰고 승인받는다. 코드는 쓰지 않는다. 프로세스 전체는 [docs/stories/README.md](../../../docs/stories/README.md).

## 입력

| 항목 | 규칙 |
|---|---|
| 요구사항 | `docs/product/requirements.md`의 REQ. 해당 REQ가 없으면 새 행을 `proposed`로 추가하고 출처를 "사용자 요청 <날짜>"로 적는다 |
| 크기 | 한 스토리는 며칠 안에 끝나는 크기. 크면 쪼개자고 제안한다 (화면 단위, CRUD 동작 단위) |

## 절차

1. 번호: `ls docs/stories`에서 가장 큰 `S-###` + 1.
2. 폴더 `docs/stories/S-###-<kebab-slug>/`를 만들고 `docs/stories/_template/story.md`를 복사해 채운다.
3. frontmatter의 `requirements`, `use_cases`, `screens`를 제품 문서의 ID로 채운다. 해당 UC·SCR이 목록에 없으면 목록에 행을 추가한다 (명세·정의 파일은 아직 만들지 않는다).
4. **수용 기준**은 Given/When/Then, 각각 테스트나 실행으로 확인 가능하게. 오류·권한·빈 결과 같은 경계 조건을 최소 하나 넣는다.
5. 범위 밖과 미해결 질문을 적는다.
6. 브랜치를 제안한다: `feat/S-###-<slug>` (`docs/conventions/commit.md`). 브랜치 생성은 사용자가 동의하면 한다.

## 멈추고 확인받기 (승인 ①)

수용 기준과 미해결 질문을 보여주고 기다린다. 승인되면:
- `status: ready`, "승인" 절에 날짜와 승인자
- 관련 REQ 상태를 `in-progress`로
- 다음 단계로 `story-design`을 안내한다

## 하지 않는 것

- 설계·코드를 먼저 쓰지 않는다.
- 사용자 승인 없이 `ready`로 바꾸지 않는다.
