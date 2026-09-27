# 코드 컨벤션

사람과 AI 에이전트(Claude Code, Cursor, Codex)가 **같은 문서를 읽는다.** 이 폴더가 유일한 기준(SSOT)이다.
`.claude/rules/`는 여기를 가리키며 자주 틀리는 것만 요약한다. 규칙 본문을 거기에 복사하지 않는다.

## 문서 목록

| 문서 | 대상 |
|---|---|
| [commit.md](commit.md) | 커밋 메시지, 브랜치, PR |
| [java.md](java.md) | `edge/api/`, `central/api/` — Spring Boot |
| [react.md](react.md) | `edge/ui/`, `central/ui/` — React + TypeScript |
| [python.md](python.md) | `edge/worker/` |
| [sql.md](sql.md) | `*/docs/database/` DDL·DML, MyBatis 매퍼 XML |

## 이 문서들의 성격

- 여기 적힌 것은 **"코드가 도달해야 할 상태"**다. 새 코드는 예외 없이 따른다.
- 어긋난 기존 코드는 각 문서의 **"정리 대상"** 절에 적는다. 면제 목록이 아니라 할 일 목록이다.
  무엇이 어긋났는지와 고치는 비용을 함께 남긴다.
- 기계가 강제할 수 있는 것(eslint, ruff, formatter)은 문서에 나열하지 않고 설정 파일을 가리킨다.

## 문서를 고칠 때

- 규칙을 추가하면 기존 코드가 얼마나 어기는지 세어 "정리 대상"에 적는다.
- 이 폴더의 문서가 바뀌면 루트 `CLAUDE.md`의 인덱스 표와 `.claude/rules/`의 요약도 확인한다.
- 기존 코드를 고칠 때 규칙에 맞추겠다고 주변 코드까지 옮기지 않는다.
