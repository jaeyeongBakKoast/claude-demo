---
paths:
  - "docs/product/**"
  - "docs/quality/**"
  - "docs/manuals/**"
  - "docs/deliverables/**"
---

# 제품 문서·산출물

체계와 ID 규칙은 `docs/product/README.md`, 산출물 대응은 `docs/deliverables/README.md`다.

- **ID는 재사용하지 않는다.** 폐기한 항목은 지우지 않고 상태를 `dropped`로 둔다.
- 문서 사이는 ID로 연결한다. 새 UC·SCR·API를 만들면 목록 문서와 `traceability.md`에 행을 추가한다.
- `generated/` 아래 파일은 **손으로 고치지 않는다.** `tools/deliverables/*.py`로 다시 만든다.
- 다이어그램은 Mermaid로 쓴다. 이미지 파일로 넣지 않는다.
- 요구사항에는 출처를 적는다. 출처 없는 요구사항을 지어내지 않는다.
- 스토리 없이 제품 문서를 크게 바꾸지 않는다. 오타·서식 수정은 예외.
- 발주기관 기준·법령 항목(보안약점, 접근성 검사 항목)을 기억에 의존해 채우지 않는다. 원문에서 옮긴다.
