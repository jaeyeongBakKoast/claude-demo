# edge — 현장 장비 시스템

`edge/` 아래 파일을 처음 읽을 때 로드된다. edge 모듈 전체에 공통인 사실만 둔다.
모듈별 명령·구조는 `api/`, `ui/`, `worker/`의 `CLAUDE.md`에 있다.

## 동작 환경

- 현장 장비(<OS, 하드웨어>)에서 돈다. **네트워크가 끊겨도 동작해야 한다.**
  central 호출은 실패를 전제로 짜고, 보내지 못한 데이터는 로컬에 쌓았다가 재전송한다.
- 디스크가 작다. 로그·임시 파일은 보존 기간과 삭제 정책을 함께 만든다.

## 모듈 간 계약

| 호출 | 방향 | 문서 |
|---|---|---|
| 수집 결과 저장 | `worker` → `api` | `edge/docs/api-contract.md` |
| central 전송 | `api` → `central/api` | `central/docs/api-contract.md` |

계약(경로, DTO 필드)을 바꾸면 **호출하는 쪽과 받는 쪽 코드, 두 문서를 같은 작업에서 함께 바꾼다.**

## 데이터베이스

edge DB는 central DB와 **다른 데이터베이스다.** DDL은 `edge/docs/database/`에 있다.

## 그룹 전용 자산

- `edge/.claude/skills/edge-release-check/` — 배포 전 점검
- `edge/docs/ops/` — 현장 설치·운영 절차. 사람이 관리한다 (Claude는 수정 불가, 훅이 차단)
