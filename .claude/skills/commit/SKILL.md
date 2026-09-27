---
name: commit
description: "Use when the user runs /commit or asks '커밋해줘' in this repo. Groups staged/unstaged changes per docs/conventions/commit.md and commits only after the user confirms the plan."
disable-model-invocation: true
argument-hint: "[추가 지시, 예: edge/api만]"
---

# 컨벤션에 맞는 커밋

부수효과가 있는 스킬이라 `disable-model-invocation: true`로 사용자만 호출한다.

## 절차

1. `docs/conventions/commit.md`를 읽는다.
2. `git status`, `git diff`, `git diff --staged`로 변경을 확인한다.
3. 변경을 이유별로 묶어 커밋 계획을 보여준다. 여러 관심사가 섞였으면 `git-master` 에이전트에 나누기를 맡긴다.

   ```text
   1. feat(api): 장비 상태 조회 API 추가
      - edge/api/src/main/java/.../DeviceController.java
      - edge/api/src/test/java/.../DeviceServiceImplTest.java
   ```

4. **사용자가 확인하면** 파일을 명시해 `git add <파일>` 후 커밋한다. `git add .`를 쓰지 않는다.
5. `git log --oneline -n <커밋 수>`로 결과를 보여준다.

## 하지 않는 것

- `Co-Authored-By` 등 트레일러를 넣지 않는다.
- 푸시하지 않는다. 사용자가 따로 요청할 때만 한다.
- 훅 실패를 `--no-verify`로 건너뛰지 않는다. 원인을 고친다.
