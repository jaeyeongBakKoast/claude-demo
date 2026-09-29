# 제품 문서 (살아 있는 분석·설계 산출물)

제품 전체에 대한 분석·설계 산출물이다. **처음에 뼈대만 만들고, 스토리마다 필요한 만큼 갱신한다.**
스토리 진행 기록은 [../stories/](../stories/), 제출용 산출물과의 대응은 [../deliverables/](../deliverables/README.md)를 본다.
어느 단계에서 어떤 문서가 채워지는지는 [개발 프로세스 가이드 4절](../guides/development-process.md#4-산출물이-채워지는-시점)에 있다.

## 문서 지도

| 문서 | 내용 | 제출 산출물 명칭 | 누가·언제 갱신 |
|---|---|---|---|
| [requirements.md](requirements.md) | 기능·비기능 요구사항. 우선순위·상태 → **제품 백로그** | 요구사항 정의서 | `product-discovery`, `story-new`, `story-review` |
| [actors.md](actors.md) | 액터와 권한 | 유스케이스 명세서(액터 정의) | `product-discovery`, `story-design` |
| [use-cases/](use-cases/README.md) | 유스케이스 목록·개요도, UC별 명세 | 유스케이스 명세서 | 목록은 discovery, 명세는 `story-design` |
| [screens/](screens/README.md) | 화면 목록·흐름도, 화면별 정의 | 화면 설계서(UI 설계서) | 목록은 discovery, 정의는 `story-design` |
| [api.md](api.md) | 내부 API (화면 ↔ 서버) | 프로그램 사양서 일부 | `story-design`, `story-review` |
| [interfaces.md](interfaces.md) | 시스템 간·외부 연계 (edge ↔ central, 외부 기관) | 인터페이스 정의서 | `story-design` |
| [erd.md](erd.md) | Mermaid ERD (edge DB, central DB) | 엔티티 관계 모형 기술서 | DDL을 바꾸는 스토리의 `story-design` |
| [architecture.md](architecture.md) | 시스템·배포 구성 | 아키텍처 설계서 | 구조가 바뀔 때, 단계 말 |
| [code-definitions.md](code-definitions.md) | 공통 코드 | 코드 정의서 | 코드를 추가하는 스토리 |
| [traceability.md](traceability.md) | REQ → UC → SCR → API/IF → TBL → Story → Test | 요구사항 추적표 | `story-review` |
| `generated/` | 테이블 정의서, 프로그램 목록 (**자동 생성, 손으로 고치지 않음**) | 테이블 정의서, 프로그램 목록 | `tools/deliverables/` 스크립트 |

## ID 체계

| 대상 | 형식 | 예 |
|---|---|---|
| 기능 요구사항 | `REQ-F-###` | `REQ-F-012` |
| 비기능 요구사항 | `REQ-N-###` | `REQ-N-003` (성능·보안·접근성 등) |
| 액터 | `ACT-##` | `ACT-01` |
| 유스케이스 | `UC-###` | `UC-004` |
| 화면 | `SCR-###` | `SCR-010` |
| 내부 API | `API-###` | `API-021` |
| 시스템 간 인터페이스 | `IF-###` | `IF-002` |
| 테이블 | 실제 테이블명 | `device_status` |
| 스토리 | `S-###` | `S-007` |

- **번호는 재사용하지 않는다.** 폐기한 항목은 지우지 않고 상태를 `dropped`로 둔다. 감리·추적표에서 번호가 사라지면 설명해야 한다.
- 문서 사이는 ID로 연결한다. 링크를 걸 수 있으면 상대 경로 링크로.
- 다이어그램은 Mermaid로 문서 안에 쓴다. GitHub·VS Code에서 바로 렌더링되고 diff로 변경을 볼 수 있다.

## 애자일로 유지하는 법

- **discovery 때 전부 채우지 않는다.** 유스케이스·화면은 제목과 한 줄 설명만 둔다.
- 스토리를 설계할 때 **그 스토리가 건드리는 것만** 상세화한다.
- 스토리 리뷰 때 문서와 코드가 일치하는지 확인하고 추적표를 갱신한다. 문서가 코드보다 늦으면 그 스토리는 끝나지 않은 것이다.
