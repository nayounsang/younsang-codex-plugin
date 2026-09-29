# Codex Complex Prompt

[Codex Complex Prompt](https://github.com/nayounsang/codex-complex-prompt)는 복잡한 작업 요청을 브라우저의 마크다운 에디터에서 정리하고, Codex의 피드백을 반영해 다듬은 뒤 실행할 수 있게 해줍니다.

## 1. 해결하는 문제

> (수많은 채팅 기록...) 야 잠깐만 너 뭐해, 30분이나 걸려서 이렇게 하면 넘 불만족스러운데. 작업한거 날리고 내가 조건 더 줄테니 다시 해봐. 근데, 처음에 하자고 한게 뭐였지? 아 내가 이렇게 하라고 했다고? 무슨 소리야

복잡한 작업을 채팅으로 주고받으며 수정하면 목표와 세부 조건이 대화에 흩어지고, Codex가 반영한 내용을 한눈에 확인하기 어렵습니다. 요청을 한 문서로 작성하고 직접 고친 뒤, Codex에게 선택한 부분의 피드백을 받아 전체 요청을 검토할 수 있습니다.

## 2. 설치

설치 방법은 두 가지입니다. 아래 중 하나만 선택하세요.

### 이 marketplace의 스킬로 설치

Codex CLI에서 `$install-complex-prompt` 스킬을 요청합니다. 스킬이 macOS M1, Codex CLI, Node.js 24 이상, `npx` 사용 가능 여부를 확인한 뒤 설치 명령을 실행합니다.

### 설치 명령으로 직접 설치

[Codex Complex Prompt 저장소](https://github.com/nayounsang/codex-complex-prompt)에서 안내하는 설치 명령을 터미널에서 직접 실행합니다.

```bash
npx @codex-complex-prompt/cli-bridge hook install
```

설치가 끝나면 Codex CLI를 재시작합니다. 새 hook을 검토하라는 안내가 나오면 `/hooks`에서 내용을 확인하고 신뢰 여부를 선택한 뒤 새 대화에서 사용합니다.

## 3. 사용

Codex CLI에서 `$complex-prompt`를 호출해 요청 문서를 엽니다.

```text
$complex-prompt 결제 기능을 조사하고 구현 요청 문서를 작성해줘
```

- 요청 없이 호출하면 빈 문서로 시작합니다.
- 일반 텍스트를 입력하면 그 내용을 초안으로 사용합니다.
- `.md` 또는 `.txt` 파일 경로를 입력하면 파일 내용을 초안으로 불러옵니다. 원본 파일은 수정하지 않습니다.

브라우저 편집기에서 요청을 직접 수정하고, 템플릿으로 초안을 시작하거나 그림과 이미지를 첨부할 수 있습니다.

## 4. Codex 피드백을 반영하고 실행하기

기능 구현 전 사용자 흐름과 예외 조건을 정리하거나, 리서치 범위와 결과 형식 또는 문서 작성 조건을 모으는 데 사용할 수 있습니다.

1. 문서를 직접 작성하거나 수정합니다.
2. 검토가 필요한 부분을 선택해 `Send Feedback`으로 Codex에게 피드백을 요청합니다. 반영된 문서가 편집기에서 다시 열립니다.
3. 결과를 확인하고 필요하면 더 수정하거나 피드백을 반복합니다.
4. 요청이 준비되면 `Submit`을 눌러 문서 내용을 Codex CLI에 전달하고 실행합니다.

자세한 사용 안내는 [원본 저장소의 README](https://github.com/nayounsang/codex-complex-prompt#readme)를 참고하세요.
