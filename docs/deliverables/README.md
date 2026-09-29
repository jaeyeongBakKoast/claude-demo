# 산출물 목록표

제출해야 하는 산출물과 **레포 안의 원본**을 연결한다. 제출본(HWPX·DOCX)은 원본에서 만든다. 원본을 고치고 다시 만든다 — 제출본을 직접 고치지 않는다.

> 사업마다 과업지시서·제안요청서(RFP)의 산출물 목록과 명칭이 다르다. **사업 시작 때 이 표를 RFP 기준으로 고친다.**
> `구분`의 `용역`은 공공 SW 용역, `R&D`는 국가연구개발과제에서 주로 요구되는 것이다.

## 목록

| 단계 | 산출물 | 구분 | 원본 | 만드는 법 | 갱신 시점 |
|---|---|---|---|---|---|
| 착수 | 사업수행계획서 / 연구개발계획서 | 용역·R&D | 레포 밖 | PM 작성 | 착수 |
| 착수 | 방법론 테일러링 결과서 | 용역 | 이 표 + `docs/stories/README.md` | 수동 | 착수 |
| 분석 | 요구사항 정의서 | 용역·R&D | `docs/product/requirements.md` | 스킬 갱신 | 스토리마다 |
| 분석 | 유스케이스 명세서 (액터 포함) | 용역 | `docs/product/actors.md`, `use-cases/` | 스킬 갱신 | 스토리마다 |
| 분석 | 요구사항 추적표 | 용역 | `docs/product/traceability.md` | `story-review` | 스토리마다 |
| 설계 | 아키텍처 설계서 | 용역·R&D | `docs/product/architecture.md` | 수동 | 구조 변경, 단계 말 |
| 설계 | 화면 설계서 (UI 설계서) | 용역 | `docs/product/screens/` | `story-design` | 스토리마다 |
| 설계 | 인터페이스 정의서 | 용역 | `docs/product/interfaces.md` | `story-design` | 스토리마다 |
| 설계 | 엔티티 관계 모형 기술서 (ERD) | 용역 | `docs/product/erd.md` | `story-design` | DDL 변경 스토리 |
| 설계 | 테이블 정의서 (DB 설계서) | 용역 | DDL → `docs/product/generated/table-spec.md` | `gen_table_spec.py` | DDL 변경 시 |
| 설계 | 코드 정의서 | 용역 | `docs/product/code-definitions.md` | 수동 (DML과 일치) | 코드 추가 시 |
| 설계 | 프로그램 목록 | 용역 | 컨트롤러 → `docs/product/generated/program-list.md` | `gen_program_list.py` | 단계 말 |
| 구현 | 소스 코드 | 용역·R&D | 레포 | — | — |
| 시험 | 시험 계획서 | 용역 | `docs/quality/test-plan.md` | 수동 | 단계 초 |
| 시험 | 단위 시험 결과서 | 용역 | 테스트 XML → `docs/quality/generated/unit-test-report.md` | `gen_test_report.py` | 단계 말 |
| 시험 | 통합 시험 결과서 | 용역 | `docs/quality/integration-tests.md` | `story-review` | 스토리마다 |
| 시험 | 성능 시험 결과서 / 성능지표 시험 결과 | 용역·R&D | `docs/quality/performance.md` | 수동 + 시험 스크립트 | 단계 말 |
| 시험 | 시큐어코딩·웹 취약점 점검 결과 | 용역 | `docs/quality/security-checklist.md` | 도구 + 수동 | 단계 말 |
| 시험 | 웹 접근성·호환성 점검 결과 | 용역 | `docs/quality/web-accessibility.md` | 도구 + 수동 | 단계 말 |
| 시험 | 인수 시험 결과서 | 용역 | 레포 밖 (발주기관 양식) | — | 종료 |
| 이행 | 사용자 매뉴얼 | 용역·R&D | `docs/manuals/user-manual.md` | 화면 정의에서 초안 | 단계 말 |
| 이행 | 운영자 매뉴얼 (설치 포함) | 용역·R&D | `docs/manuals/operator-manual.md` + `<그룹>/docs/ops/` | 수동 | 단계 말 |
| R&D | 연구노트 | R&D | 스토리 `design.md` 검증 로그 (기초 자료) | 기관 연구노트 시스템에 기록 | 상시 |
| R&D | 연차·단계·최종 보고서 | R&D | 레포 밖 (위 산출물을 인용) | PM 작성 | 연차 말 |
| R&D | 프로그램 저작권 등록 자료 | R&D | 소스 + 프로그램 목록 + 매뉴얼 | 수동 | 성과 등록 시 |
| 종료 | 완료 보고서, 하자보수 계획서 | 용역 | 레포 밖 | PM 작성 | 종료 |

## 제출본 만들기

`deliverables-export` 스킬을 쓴다 ("산출물 제출본 만들어줘", "단계 말 산출물 정리").

1. 자동 생성 문서를 다시 만든다 (`tools/deliverables/*.py`). 테스트 결과서는 모듈 테스트를 먼저 돌린다.
2. 제출 대상 원본의 `<...>` 자리와 빈 칸을 점검한다.
3. HWPX 제출은 `.claude/skills/hwpxskill`(submodule), DOCX 제출은 docx 스킬로 변환한다.
   Mermaid 도식은 이미지로 렌더링해 넣는다.
4. 결과는 `docs/deliverables/out/<YYYY-MM-DD>/`에 두고 커밋하지 않는다 (`.gitignore`). 제출 이력은 아래 표에 남긴다.

## 제출 이력

| 제출일 | 단계 | 산출물 | 원본 커밋 | 제출처 |
|---|---|---|---|---|
| <YYYY-MM-DD> | 분석 | 요구사항 정의서 외 | `<hash>` | <발주기관> |
