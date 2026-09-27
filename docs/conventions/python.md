# Python — `edge/worker/`

> 견본의 골격이다. 실제 프로젝트의 규칙으로 채운다.
> lint·format 규칙은 `pyproject.toml`의 ruff 설정이 기준이다.

## 환경

- 패키지 관리는 `uv`. 의존성은 `uv add`로 추가하고 `uv.lock`을 함께 커밋한다.
- Python 버전은 `pyproject.toml`의 `requires-python`이 기준이다.

## 규칙

- 타입 힌트를 공개 함수에 모두 단다.
- 로그는 `logging` 모듈, 메시지는 영어. `print`를 쓰지 않는다.
- 설정은 `config.yaml`에서 읽는다. 코드에 경로·주소를 하드코딩하지 않는다.
- 장시간 루프는 예외를 잡아 로그를 남기고 계속 돈다. 조용히 삼키지 않는다.

## 테스트

- pytest. 하드웨어가 필요한 테스트는 `@pytest.mark.hardware`로 표시하고 기본 실행에서 제외한다.

## 정리 대상

| 어긋난 것 | 현황 | 고치는 비용 |
|---|---|---|
| <예: print 사용> | <n곳> | <추정> |
