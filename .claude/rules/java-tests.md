---
paths:
  - "**/src/test/java/**/*.java"
  - "*/api/build.gradle.kts"
---

# api 모듈 테스트

전체 규칙은 `docs/conventions/java.md`의 "테스트" 절이다. 아래는 자주 틀리는 것만.

- 테스트가 실패하면 Gradle 빌드도 실패한다. `ignoreFailures`를 넣지 않는다.
- 통과 여부는 콘솔 요약이나 `build/reports/tests/test/index.html`의 **건수**로 보고한다. "exit 0"만으로 통과라고 하지 않는다.
- DB가 필요한 테스트(`@SpringBootTest`로 컨텍스트를 띄우는 것)는 `@Tag("db")`를 붙인다.
  기본 `test`에서 제외되고 `integrationTest`로 돈다.
- 서비스 단위 테스트는 리포지토리를 `mock()`하고 `new XxxServiceImpl(...)`로 만든다.
- 새 테스트에서는 deprecated된 `@MockBean` 대신 `@MockitoBean`을 쓴다.
- 테스트 클래스는 대상과 같은 패키지에 `XxxTest`로 둔다.
