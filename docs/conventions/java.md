# Java (Spring Boot) — `edge/api/`, `central/api/`

> 견본의 골격이다. 실제 프로젝트의 규칙으로 채운다. 항목마다 "왜"를 한 줄 붙이면 AI가 예외 상황에서도 옳게 판단한다.

## 레이어

```text
controller/api → service (interface) → service/impl → repository (MyBatis mapper)
                                           ↘ domain (entity, dto, enum)
```

- 컨트롤러는 요청 검증과 응답 변환만 한다. 비즈니스 로직을 두지 않는다.
- 서비스는 인터페이스와 `impl`로 나눈다. <이유: 테스트에서 mock 교체, 프로젝트 관례>
- 리포지토리는 MyBatis 매퍼 인터페이스다. SQL 규칙은 [sql.md](sql.md).

## 이름

| 대상 | 규칙 | 예 |
|---|---|---|
| 요청 DTO | `<Name>CreateRequest`, `<Name>UpdateRequest` | `DeviceCreateRequest` |
| 응답 DTO | `<Name>Response` | `DeviceResponse` |
| REST 경로 | `/api/<복수형-kebab-case>` | `/api/device-statuses` |

## 예외

- 업무 오류는 `BusinessException(errorCode, message)`로 던지고 전역 핸들러가 응답으로 바꾼다.
- 없는 리소스는 `errorCode="NOT_FOUND"`.

## 로그

- 로그 메시지는 영어. 파라미터는 `{}` 플레이스홀더로.
- 비밀값·개인정보를 로그에 남기지 않는다.

## 테스트

- 서비스 단위 테스트: 리포지토리를 `mock()`하고 `new XxxServiceImpl(...)`로 만든다.
- DB가 필요한 테스트는 `@Tag("db")` — 기본 `test`에서 제외, `integrationTest`로 실행.
- 새 테스트에서는 `@MockitoBean`을 쓴다 (`@MockBean`은 deprecated).
- 결과는 건수로 보고한다.

## 정리 대상

| 어긋난 것 | 현황 | 고치는 비용 |
|---|---|---|
| <예: 컨트롤러에 로직이 있는 클래스> | <n개> | <추정> |
