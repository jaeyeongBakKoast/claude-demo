---
name: story-build
description: "Use when the current story's status is designed or in-progress and the user wants to implement it ('구현해줘', '작업 진행해줘', '이어서 해줘'). Works through design.md's task checklist one task at a time, runs tests after each, and records progress in design.md. Do NOT use before the design is approved (story-design) or for final acceptance checks (story-review)."
argument-hint: "[S-### 또는 작업 번호 T#]"
---

# 스토리 구현

`design.md`의 작업 목록을 **하나씩** 진행하고, 매 작업의 결과를 `design.md`에 기록한다.
이 기록이 중간 산출물이다. 세션이 끊겨도 다음 세션이 `design.md`만 읽고 이어갈 수 있어야 한다.

## 입력

- 현재 스토리: 브랜치의 `S-###` 또는 인자. `status`가 `designed`·`in-progress`가 아니면 멈추고 알린다.
- 처음 시작이면 `status: in-progress`로 바꾼다.

## 작업마다

1. 체크되지 않은 첫 작업을 고른다 (인자로 `T#`를 받으면 그것).
2. 관련 컨벤션(`docs/conventions/<스택>.md`)과 모듈 `CLAUDE.md`를 읽는다.
3. 테스트 계획에 해당 테스트가 있으면 **테스트를 먼저** 쓰고 실패를 확인한다.
4. 구현한다. 설계와 다르게 가야 하면 **멈추고** 이유와 변경안을 사용자에게 묻는다. 합의되면 `design.md`와 제품 문서를 먼저 고친다.
5. 모듈 테스트를 돌린다. 실패하면 원인을 찾는다 (막히면 `debugger` 에이전트).
6. `design.md`를 갱신한다:
   - 작업 체크 `[x]`
   - 검증 로그에 한 행: 일시, 작업, 한 일, 검증 명령, 결과 **건수**
7. 사용자에게 한 줄로 알리고 다음 작업으로. 커밋은 사용자가 요청할 때 `/commit`으로 (본문에 `Story: S-###`).

## 모든 작업이 끝나면

- `status: review`로 바꾸고 `story-review`를 안내한다.

## 하지 않는 것

- 작업 목록에 없는 기능을 추가하지 않는다. 필요해 보이면 "남은 일" 후보로 알린다.
- 테스트 실패를 건너뛰고 체크하지 않는다.
