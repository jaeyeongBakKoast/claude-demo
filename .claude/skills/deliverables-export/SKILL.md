---
name: deliverables-export
description: "Use when preparing submission documents for a phase end, audit or report: '산출물 제출본 만들어줘', '단계 말 산출물 정리', '감리 대비 산출물 점검', 'HWP로 요구사항 정의서 뽑아줘'. Regenerates generated docs, checks gaps against docs/deliverables/README.md, and converts sources to HWPX/DOCX. Do NOT use for day-to-day story work or for editing the source documents' content."
disable-model-invocation: true
argument-hint: "[단계 또는 산출물 이름] [hwpx|docx]"
---

# 산출물 제출본 만들기

원본은 레포의 Markdown이다. 제출본은 매번 원본에서 새로 만든다. 제출본을 직접 고치지 않는다.

## 절차

1. **대상 확정** — `docs/deliverables/README.md` 목록에서 이번에 낼 산출물과 형식(HWPX/DOCX)을 사용자와 확정한다.
2. **자동 생성 문서 재생성**
   ```bash
   python3 tools/deliverables/gen_table_spec.py
   python3 tools/deliverables/gen_program_list.py
   # 단위 시험 결과서: 모듈 테스트를 먼저 실행한 뒤
   python3 tools/deliverables/gen_test_report.py
   ```
3. **빈 곳 점검** — 대상 원본마다 보고한다. 제출본을 만들기 전에 사용자에게 보여주고 진행 여부를 묻는다.
   - `<...>` 자리표시가 남은 곳: `grep -n '<[^>]*>' <파일>`
   - 추적표의 빈 칸, `proposed` 상태로 남은 Must 요구사항
   - 프로그램 목록의 "문서 등록 N" 엔드포인트, 테이블 정의서의 주석 누락
4. **변환**
   - HWPX: `.claude/skills/hwpxskill` 스킬 (submodule. 비어 있으면 `git submodule update --init`)
   - DOCX: docx 스킬
   - Mermaid 도식은 이미지로 렌더링해서 넣는다 (예: `npx -y @mermaid-js/mermaid-cli -i in.md -o out.md`). 렌더링 도구가 없으면 사용자에게 알리고 도식 자리에 원본 경로를 적는다
   - 출력 위치: `docs/deliverables/out/<YYYY-MM-DD>/<산출물명>.<hwpx|docx>` (커밋하지 않는다)
5. **이력** — `docs/deliverables/README.md`의 "제출 이력"에 제출일·단계·산출물·원본 커밋 해시를 추가한다.

## 하지 않는 것

- 원본에 없는 내용을 제출본에서 지어 넣지 않는다. 빈 곳은 3단계에서 사용자에게 돌려준다.
- 레포 밖 산출물(사업수행계획서, 완료 보고서 등)은 만들지 않는다. 요청이 있으면 레포 원본을 인용한 초안까지만.
