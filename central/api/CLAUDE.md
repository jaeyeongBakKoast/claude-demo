# central/api 개발 가이드

코드 컨벤션은 [../../docs/conventions/java.md](../../docs/conventions/java.md)가 기준이다.
이 문서는 central/api 고유의 명령·구조·주의점만 다룬다.

## 명령

**항상 저장소 루트에서 실행한다.**

```bash
(cd central && docker compose up -d)                  # central DB
./gradlew :central:api:bootRun --args='--spring.profiles.active=local'
./gradlew :central:api:test                           # DB 불필요한 테스트만
./gradlew :central:api:integrationTest                # @Tag("db") 테스트. DB가 떠 있어야 한다
```

## 구조 (`<base.package>.central`)

- `controller/api/` — REST 컨트롤러. `receive/`는 edge 수신 전용
- `config/SecurityConfig` — 인증·인가 규칙. 새 엔드포인트는 여기에 규칙을 추가해야 접근된다
- `domain/`, `repository/`, `service/` — edge/api와 같은 레이어 구조

## 주의점

- DB가 필요한 테스트는 `@Tag("db")`를 붙인다. 붙이지 않으면 기본 `test`가 DB 없이 실패한다.
- `SecurityConfig`의 규칙은 순서대로 매칭된다. 새 규칙은 `.anyRequest()` **위**에 넣는다.
