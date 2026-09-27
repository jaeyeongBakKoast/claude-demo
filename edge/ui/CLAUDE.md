# edge/ui 개발 가이드

코드 컨벤션은 [../../docs/conventions/react.md](../../docs/conventions/react.md)가 기준이다.
이 문서는 edge/ui 고유의 명령·구조·주의점만 다룬다.

## 명령

`edge/ui/`에서 실행한다.

```bash
npm run dev      # Vite 개발 서버. /api 는 edge/api(localhost:8080)로 프록시
npm run build    # tsc -b 타입 검사 후 빌드. 결과는 edge/api WAR에 포함된다
npm run lint
npm test         # vitest
```

## 구조

- `src/api/` — 서버 호출 함수. 컴포넌트는 여기만 쓴다
- `src/store/` — Redux Toolkit. typed hook(`useAppSelector`, `useAppDispatch`)만 쓴다
- `src/pages/`, `src/components/` — 화면과 재사용 컴포넌트

## 주의점

- 현장 장비의 브라우저(키오스크)에서 돈다. `<해상도, 터치 여부 등 제약>`
- 빌드 결과는 `edge/api`의 `static/app/`으로 복사된다. `base` 경로를 바꾸면 API 쪽 서빙 경로도 바꿔야 한다.
