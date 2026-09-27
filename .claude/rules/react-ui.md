---
paths:
  - "*/ui/src/**/*.ts"
  - "*/ui/src/**/*.tsx"
---

# React UI

전체 규칙은 `docs/conventions/react.md`다. 아래는 자주 틀리는 것만.

- lint 규칙은 각 모듈의 `eslint.config.js`가 기준이다. 저장하면 훅이 바뀐 파일만 eslint로 검사한다.
- 서버 호출은 `src/api/`의 함수를 통해서만 한다. 컴포넌트에서 `fetch`/`axios`를 직접 부르지 않는다.
- 전역 상태는 `src/store/`의 typed hook(`useAppSelector`, `useAppDispatch`)만 쓴다.
- 색상·간격은 디자인 토큰(Tailwind 설정)을 쓴다. 임의 hex 값을 넣지 않는다.
