---
name: scaffolding-crud-api
description: "Use when asked to create a basic CRUD REST API, 'CRUD 만들어줘', '테이블 기반 API', or '기본 API 구조' for a table in edge/api or central/api, given a table name or a DDL. Covers entity, DTO, MyBatis mapper XML, repository, service, controller, tests. Do NOT use for changing an existing API or for non-table endpoints."
argument-hint: "<모듈> <테이블명 또는 DDL 경로>"
---

# 테이블 기반 CRUD API 골격 생성

DDL 하나를 받아 `docs/conventions/java.md`·`sql.md`가 정한 레이어 구조로
목록(페이징)·단건·생성·부분 수정·삭제 API를 만든다. **이 스킬의 가치는 결정을 대신 내려 주는 데 있다.**
아래 "정해진 것"을 다시 고민하지 않는다.

> 도메인 워크플로 스킬의 예시다. 실제 프로젝트의 레이어·예외·페이징 방식으로 바꿔 쓴다.

## 입력

| 항목 | 규칙 |
|---|---|
| 모듈 | `edge/api`, `central/api` 중 하나. 없으면 묻는다 |
| 테이블 | DDL은 `<그룹>/docs/database/ddl/`에서 찾는다. 없으면 DDL 본문을 요청한다 |

이름 파생: 테이블 `device_status` → 패키지 `devicestatus`, 클래스 접두 `DeviceStatus`,
경로 `/api/device-statuses`(복수형 kebab-case), 매퍼 XML `DeviceStatusMapper.xml`.

## 정해진 것

- **엔드포인트 5종 고정**: `GET /api/<리소스>`(페이징), `GET /{id}`, `POST`, `PATCH /{id}`, `DELETE /{id}`
- **수정은 PATCH 부분 수정.** `*UpdateRequest`는 모든 필드 nullable, XML은 `<set><if>`로 보낸 필드만 갱신한다
- **SELECT는 `*Response`를 `resultType`으로 직접 받는다.** 엔티티는 INSERT·UPDATE 파라미터에만 쓴다
- **없는 id는 `BusinessException(errorCode="NOT_FOUND")`.** 수정·삭제는 반영 건수 0이면 던진다
- **목록 검색 조건은 최소.** 필터 없이 페이징만. 기본 20, 상한 200
- **테스트는 `*ServiceImplTest` 하나**: 리포지토리 mock, 생성·조회·NOT_FOUND

## 파일 체크리스트

- [ ] `domain/<기능>/<Name>.java` — 엔티티
- [ ] `domain/<기능>/dto/<Name>CreateRequest`, `UpdateRequest`, `Response`, `PageRequest`
- [ ] `repository/<Name>Repository.java` + `resources/mybatis/<Name>Mapper.xml`
- [ ] `service/<Name>Service.java` + `service/impl/<Name>ServiceImpl.java`
- [ ] `controller/api/<Name>Controller.java`
- [ ] `src/test/.../<Name>ServiceImplTest.java`

각 파일은 같은 모듈에 이미 있는 CRUD 기능 하나를 골라 그 형태를 그대로 따른다.
기존 기능이 없으면 `docs/conventions/java.md`의 레이어 절을 기준으로 만든다.

## 검증

`./gradlew :<그룹>:api:test` — 새 테스트 포함 통과 건수로 보고한다.
