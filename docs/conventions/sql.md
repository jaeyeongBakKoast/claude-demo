# SQL — DDL·DML, MyBatis 매퍼 XML

> 견본의 골격이다. 실제 프로젝트의 규칙으로 채운다.

## DB 구분

| | 데이터베이스 | DDL 위치 |
|---|---|---|
| edge | `<edge DB 이름>` | `edge/docs/database/` |
| central | `<central DB 이름>` | `central/docs/database/` |

두 DB는 서로 다르다. 한쪽 DDL을 다른 쪽에 복사하지 않는다.

## DDL

- 파일 맨 위에 `drop table if exists <테이블> cascade;` — 초기화 스크립트를 재실행할 수 있어야 한다.
- 모든 테이블·컬럼에 `comment on`. 이 주석이 스키마 문서다.
- 이름은 snake_case. PK는 `<테이블>_id`.
- 시각은 `<타입과 타임존 규칙>`.

## MyBatis 매퍼 XML

- `namespace`는 매퍼 인터페이스 FQCN과 1:1.
- 값은 `#{}`만 쓴다. `${}`는 화이트리스트로 검증한 정렬 컬럼 등에만.
- 부분 수정은 `<set><if test="x != null">`.

## 정리 대상

| 어긋난 것 | 현황 | 고치는 비용 |
|---|---|---|
| <예: comment on 누락 컬럼> | <n개> | <추정> |
