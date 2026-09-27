# edge/worker 개발 가이드

코드 컨벤션은 [../../docs/conventions/python.md](../../docs/conventions/python.md)가 기준이다.
이 문서는 edge/worker 고유의 명령·구조·주의점만 다룬다.

## 명령

`edge/worker/`에서 실행한다. 패키지 관리는 `uv`다.

```bash
uv sync                    # 의존성 설치 (.venv)
uv run python -m worker    # 로컬 실행 (config.example.yaml 복사 후)
uv run pytest -q
uv run ruff check .
```

## 구조

- `worker/` — 패키지 본체. `collector/`(입력 수집), `processor/`(가공), `sender/`(edge/api 전송)
- `tests/` — pytest. 하드웨어가 필요한 테스트는 `@pytest.mark.hardware`로 표시하고 기본 실행에서 제외한다
- `config.example.yaml` — 설정 예시. 실제 `config.yaml`은 커밋하지 않는다

## 주의점

- 장비에서 systemd 서비스로 돈다. 서비스 파일·설치 절차는 `edge/docs/ops/`에 있다 (사람이 관리).
- 장시간 실행된다. 루프 안에서 메모리가 쌓이지 않게 하고, 예외는 잡아 로그로 남긴 뒤 계속 돈다.
