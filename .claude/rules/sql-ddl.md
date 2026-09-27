---
paths:
  - "*/docs/database/**/*.sql"
  - "*/api/src/main/resources/mybatis/**/*.xml"
---

# DDL·DML과 MyBatis 매퍼

전체 규칙은 `docs/conventions/sql.md`다. 아래는 초기화를 깨뜨리거나 자주 틀리는 것만.

- DDL 파일 맨 위에 `drop table if exists <테이블> cascade;`. 초기화 스크립트가 재실행 가능해야 한다.
- 모든 테이블과 모든 컬럼에 `comment on`을 단다. 이 주석이 스키마 문서다.
- edge DB와 central DB는 **서로 다른 데이터베이스다.** 한쪽 DDL을 다른 쪽에 복사하지 않는다.
- 매퍼 XML의 `namespace`는 매퍼 인터페이스 FQCN과 1:1. 값은 `#{}`만 쓴다. `${}`는 정렬 컬럼처럼
  화이트리스트로 검증한 값에만 쓴다.
