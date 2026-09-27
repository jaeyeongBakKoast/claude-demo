# edge/api 개발 가이드

코드 컨벤션은 [../../docs/conventions/java.md](../../docs/conventions/java.md)가 기준이다.
이 문서는 edge/api 고유의 명령·구조·주의점만 다룬다.

## 명령

**항상 저장소 루트에서 실행한다.**

```bash
./gradlew :edge:api:bootRun --args='--spring.profiles.active=local'
./gradlew :edge:api:test          # DB·외부 서비스 불필요
./gradlew :edge:api:bootWar       # edge/ui 빌드 결과를 static/app 에 포함한 WAR
```

## 구조 (`<base.package>.edge`)

- `controller/api/` — REST 컨트롤러
- `domain/<기능>/` — 엔티티·DTO·enum만
- `repository/` — MyBatis 매퍼 인터페이스. XML은 `resources/mybatis/`
- `service/`, `service/impl/` — 비즈니스 로직
- `sync/` — central 전송. 실패 시 로컬 큐에 쌓고 스케줄러가 재전송한다

## 주의점

- `<모듈 디렉터리에서 gradlew를 돌리면 루트 프로젝트가 달라져 UI가 빠진 WAR가 나온다 — 예시>`
- `src/main/resources/static/app/`은 빌드가 채우는 산출물이다. 손으로 고치지 않는다.
- edge/api 테스트는 DB나 외부 서비스가 필요하지 않다. 필요하게 만들지 않는다.
