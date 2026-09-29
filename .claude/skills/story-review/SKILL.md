---
name: story-review
description: "Use when the current story's status is review, or all design.md tasks are checked and the user asks to wrap up ('리뷰해줘', '검증해줘', '스토리 마무리', '완료 처리'). Verifies each acceptance criterion with evidence, checks product docs against code, updates traceability and integration test records, writes review.md and stops for acceptance. Do NOT use for code-quality review of an arbitrary diff (code-review) or before implementation is done."
argument-hint: "[S-###]"
---

# 스토리 리뷰

수용 기준을 **증거로** 확인하고, 제품 문서가 코드와 일치하는지 확인한 뒤 추적표를 갱신한다.
문서가 코드보다 늦으면 이 스토리는 끝나지 않은 것이다.

## 절차

1. **전체 테스트** — 영향 받은 모듈의 테스트를 모두 돌리고 건수를 기록한다.
2. **수용 기준** — `docs/stories/_template/review.md`로 `review.md`를 만들고, AC마다 증거를 적는다.
   증거는 테스트 이름과 결과, 또는 실행 절차와 관찰 결과. "구현했음"은 증거가 아니다.
3. **자동 생성 문서 재생성·대조**
   ```bash
   python3 tools/deliverables/gen_table_spec.py      # DDL이 바뀌었으면
   python3 tools/deliverables/gen_program_list.py    # 문서 등록 N 인 엔드포인트가 있으면 api.md/interfaces.md 에 추가
   ```
4. **문서-코드 일치** — `review.md`의 체크리스트를 하나씩 확인하고, 어긋나면 **문서 쪽을 코드에 맞게** 고친다
   (코드가 틀렸으면 `story-build`로 돌아간다).
5. **보안·접근성** — 인증·인가·외부 노출 API를 바꿨으면 `security-reviewer`. 화면을 바꿨으면 `docs/quality/web-accessibility.md`의 스토리 단위 체크.
6. **기록 갱신**
   - `docs/product/traceability.md`: 이 스토리의 REQ 행에 UC·SCR·API/IF·테이블·스토리·시험
   - `docs/quality/integration-tests.md`: AC마다 `IT-<번호>-<AC>` 행
   - 매뉴얼에 영향이 있으면 `docs/manuals/user-manual.md` 해당 절

## 멈추고 확인받기 (승인 ③)

AC별 결과와 남은 일을 보여주고 기다린다. 수락되면:
- `story.md`의 `status: done`, `review.md` "수락" 절에 날짜와 수락자
- `requirements.md`의 REQ 상태: 이 스토리로 요구사항이 모두 충족되면 `done`, 아니면 `in-progress` 유지
- 남은 일은 새 REQ 또는 다음 스토리 후보로 등록

AC가 하나라도 실패면 `status: in-progress`로 되돌리고 `design.md`에 보완 작업을 추가한다.

## 하지 않는 것

- 사용자 수락 없이 `done`으로 바꾸지 않는다.
- 증거 없이 AC를 통과로 적지 않는다.
