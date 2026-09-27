# central/ui 개발 가이드

코드 컨벤션은 [../../docs/conventions/react.md](../../docs/conventions/react.md)가 기준이다.
이 문서는 central/ui 고유의 명령·구조·주의점만 다룬다.

## 명령

`central/ui/`에서 실행한다.

```bash
npm run dev      # /api 는 central/api(localhost:8090)로 프록시
npm run build
npm run lint
npm test
```

## 구조

- `src/api/`, `src/store/`, `src/pages/`, `src/components/` — edge/ui와 같은 구조
- `src/auth/` — 로그인 상태와 권한별 메뉴 노출

## 주의점

- 메뉴 노출은 편의일 뿐 보안이 아니다. 권한 검사는 central/api가 한다.
- `<공용 UI 라이브러리를 쓰면 그 스킬·문서 위치를 여기에 적는다>`
