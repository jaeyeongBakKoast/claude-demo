# 내부 API 목록 (화면 ↔ 서버)

시스템 간·외부 연계는 [interfaces.md](interfaces.md)에 둔다. 코드와의 일치는 `story-review`가 확인한다
(컨트롤러의 경로·메서드와 이 표가 같아야 한다). 전체 엔드포인트 목록은 `generated/program-list.md`에서 자동 생성된다.

| ID | 메서드 | 경로 | 모듈 | 권한 | 설명 | 사용 화면 | 테이블 |
|---|---|---|---|---|---|---|---|
| API-001 | GET | `/api/devices` | central/api | ACT-01 | <장비 상태 목록(페이징)> | SCR-001 | `device`, `device_status` |

## API-001 장비 상태 목록

<필요할 때만 상세를 쓴다. 요청 파라미터·응답 필드·오류 코드가 표로 설명되지 않을 때.>

| 구분 | 이름 | 타입 | 필수 | 설명 |
|---|---|---|---|---|
| 요청 | `page` | int | N | 기본 1 |
| 응답 | `items[].deviceId` | long | Y | |
| 오류 | `NOT_FOUND` | | | |
