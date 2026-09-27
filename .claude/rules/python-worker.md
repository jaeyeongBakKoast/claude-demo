---
paths:
  - "edge/worker/**/*.py"
  - "edge/worker/pyproject.toml"
---

# Python 워커

전체 규칙은 `docs/conventions/python.md`다. 아래는 자주 틀리는 것만.

- 의존성은 `uv add`로 추가한다. `pip install`로 넣지 않는다. `uv.lock`을 같이 커밋한다.
- lint·format은 `pyproject.toml`의 ruff 설정이 기준이다. 저장하면 훅이 바뀐 파일만 검사한다.
- 로그는 `logging` 모듈로 영어로 남긴다. `print`를 쓰지 않는다.
- 테스트는 `uv run pytest`로 돌리고 통과 건수로 보고한다.
