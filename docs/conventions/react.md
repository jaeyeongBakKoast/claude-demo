# React + TypeScript — `edge/ui/`, `central/ui/`

> 견본의 골격이다. 실제 프로젝트의 규칙으로 채운다.
> lint로 강제되는 규칙은 여기 나열하지 않는다. 각 모듈의 `eslint.config.js`가 기준이다.

## 구조

```text
src/
├── api/          서버 호출 함수 (도메인별 파일). 컴포넌트는 여기만 쓴다
├── store/        Redux Toolkit. store.ts, hooks.ts, slices/
├── pages/        라우트 단위 화면
├── components/   재사용 컴포넌트
└── types/        공용 타입
```

## 규칙

- 서버 호출은 `src/api/`의 함수로만 한다. 컴포넌트에서 `fetch`/`axios`를 직접 부르지 않는다.
  <이유: 인증 헤더·오류 처리를 한 곳에서>
- 전역 상태는 typed hook(`useAppSelector`, `useAppDispatch`)만 쓴다.
- 컴포넌트 파일명은 PascalCase, 훅은 `useXxx`.
- 색상·간격은 Tailwind 설정의 토큰을 쓴다. 임의 hex 값을 넣지 않는다.
- `any`를 쓰지 않는다. 외부 응답은 `types/`에 타입을 정의한다.

## 테스트

- vitest + Testing Library. 사용자 관점(보이는 텍스트, 역할)으로 찾는다.

## 정리 대상

| 어긋난 것 | 현황 | 고치는 비용 |
|---|---|---|
| <예: 컴포넌트에서 직접 fetch> | <n개> | <추정> |
