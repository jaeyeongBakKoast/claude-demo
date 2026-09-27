# central — 중앙 시스템

`central/` 아래 파일을 처음 읽을 때 로드된다. central 모듈 전체에 공통인 사실만 둔다.
모듈별 명령·구조는 `api/`, `ui/`의 `CLAUDE.md`에 있다.

## 동작 환경

- 여러 edge 장비의 데이터를 받는다. **edge가 보낸 데이터를 신뢰하지 않는다** — 장비 인증과 입력 검증을 서버에서 한다.
- 같은 데이터가 재전송될 수 있다. 수신 API는 멱등하게 만든다 (edge 쪽 식별자로 중복 제거).

## 모듈 간 계약

| 호출 | 방향 | 문서 |
|---|---|---|
| 수집 데이터 수신 | `edge/api` → `api` | `central/docs/api-contract.md` |
| 조회·관리 | `ui` → `api` | 코드의 컨트롤러가 기준 |

## 데이터베이스

central DB는 edge DB와 **다른 데이터베이스다.** DDL은 `central/docs/database/`에 있다.

## 보안

인증·인가, 수신 API를 바꾸면 머지 전에 `security-reviewer` 에이전트로 검토한다.
