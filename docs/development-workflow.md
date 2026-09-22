# 개발 워크플로우

1. 작업을 시작하기 전에 현재 브랜치와 worktree 상태를 확인한다.

2. 원격 `main`을 최신 상태로 동기화한 뒤, 작업 목적을 설명하는 전용
   브랜치를 만든다.

3. 새로운 스킬은 `skills/<skill-name>/` 아래에 추가한다. 스킬 이름은
   소문자 하이픈 형식을 사용하고, 최소한 루트에 `SKILL.md`를 둔다.

4. 스킬별 설명과 사용 방법, 사람이 읽는 개발 문서는 `docs/`에 둔다.
   새로운 스킬을 추가할 때는 `SKILL.md`, 관련
   `docs/<skill-name>.md`, README의 `Features` 항목을 같은 작업에서
   함께 작성한다.

   기존 스킬의 목적, 사용법, 동작 정책, 출력 형식 또는 참조 절차를
   변경할 때도 관련 docs와 README 요약을 같은 작업에서 갱신한다.

5. 플러그인 manifest는 `.codex-plugin/plugin.json`에 유지한다. 스킬을
   추가할 때는 특별한 manifest 변경이 필요하지 않으며, `skills` 경로가
   전체 스킬 디렉터리를 가리키는지 확인한다.

6. 변경 후 Codex의 내장 `validate_plugin` 검증을 실행하고, 변경된 스킬의
   내부 링크, 참조 파일, 에이전트 metadata가 실제 파일과 일치하는지
   확인한 뒤 필요한 테스트나 수동 검증을 수행한다. 문서 검증에서는
   README 링크, docs 파일 경로, 스킬 내부 reference 링크도 확인한다.

   기능 변경 시 docs의 내용이 실제 `SKILL.md`와 reference 파일의
   동작·정책과 일치하는지 확인한다.

7. diff를 검토해 다른 스킬의 동작 정책이나 파일을 의도치 않게 바꾸지
   않았는지 확인한 뒤 커밋한다.

   기존 `validate_plugin` 실행과 최종 diff 검토 절차는 문서 변경만
   포함된 작업에서도 유지한다.

8. marketplace를 사용하는 경우 marketplace 파일을 직접 편집하지 않고,
   `plugin-creator`가 제공하는 scaffold/update 흐름을 사용한다. 플러그인
   manifest나 스킬 구조가 바뀌면 새 Codex thread에서 동작을 확인한다.
