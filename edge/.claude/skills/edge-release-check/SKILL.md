---
name: edge-release-check
description: "Use before building or shipping an edge release: 'edge 배포 전 점검', '엣지 릴리스 체크', 'edge WAR 만들기 전에 확인'. Checks edge/api, edge/ui, edge/worker build/test and profile settings. Do NOT use for central releases or for field installation (see edge/docs/ops/)."
---

# edge 배포 전 점검

> 모듈 그룹 전용 스킬의 예시다. `edge/.claude/skills/`에 있으므로 Claude가 `edge/` 아래 파일을
> 처음 읽을 때 발견된다. 루트에서 `/edge-release-check`로 바로 부르려면 먼저 edge 파일을 하나 읽게 한다.

## 절차

각 항목을 실제로 돌리고 결과를 표로 보고한다. 하나라도 실패하면 멈추고 알린다.

| # | 확인 | 명령 | 통과 기준 |
|---|---|---|---|
| 1 | 작업 트리가 깨끗한가 | `git status --short edge/` | 빈 출력 |
| 2 | API 테스트 | `./gradlew :edge:api:test` | 실패 0건 (건수 보고) |
| 3 | UI 빌드 | `(cd edge/ui && npm run build)` | exit 0, 타입 오류 없음 |
| 4 | 워커 테스트 | `(cd edge/worker && uv run pytest -q)` | 실패 0건 (건수 보고) |
| 5 | 운영 프로파일 | `<프로파일 설정 파일>`의 활성 프로파일 값 | `product` |
| 6 | DB 스키마 변경 | `git diff <이전 태그> -- edge/docs/database/` | 변경이 있으면 마이그레이션 파일 존재 |

## 하지 않는 것

- 프로파일 값을 대신 바꾸지 않는다. 다르면 알리기만 한다.
- 현장 설치 절차(`edge/docs/ops/`)를 실행하지 않는다.
