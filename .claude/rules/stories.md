---
paths:
  - "docs/stories/**"
---

# 스토리 기록

프로세스는 `docs/stories/README.md`다.

- 상태는 `draft → ready → designed → in-progress → review → done` 순서로만 바꾼다.
- **`ready`, `designed`, `done`은 사용자 승인·수락을 받은 뒤에만 쓴다.** 승인 절에 날짜와 승인자를 남긴다.
- `design.md`의 작업을 끝낼 때마다 체크하고 검증 로그에 한 행을 남긴다 (일시, 작업, 검증 명령, 결과 건수).
- 설계와 다르게 구현해야 하면 코드보다 `design.md`와 제품 문서를 먼저 고치고 사용자에게 알린다.
- 수용 기준은 증거로만 통과 처리한다. 증거는 테스트 이름과 결과, 또는 실행 절차와 관찰 결과.
- 스토리 번호는 재사용하지 않는다. `_template/`은 고치지 않고 복사해서 쓴다.
