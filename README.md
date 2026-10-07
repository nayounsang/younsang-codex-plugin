# Younsang Codex Plugin

> 주의: MacOS M1 + Codex CLI에서 동작하는 것이 전제합니다. 다른 환경은 동작 여부를 모르며, 호환할 계획도 없습니다.(제가 디바이스를 바꾸는게 아니면)

nayounsang이 Codex CLI와 개발할 때 사용하는 유틸리티 모음입니다.

스킬별 설명과 사용 방법은 [docs](docs/)를 참조하세요.
개발 및 추가 작업 절차는 [개발 워크플로우](docs/development-workflow.md)를
참조하세요.

## 전역 설치

먼저 GitHub 저장소의 marketplace를 Codex CLI에 등록하고, 목록에서 플러그인을 설치합니다.

```bash
# 최초 1회: marketplace 등록
codex plugin marketplace add nayounsang/younsang-codex-plugin --ref main

# 플러그인 설치
codex plugin add younsang-codex-plugin@younsang-codex-plugins
```

설치 후 새 Codex thread를 시작하면 플러그인의 스킬을 사용할 수 있습니다.

이후 업데이트시 다음 명령어를 실행해주세요.

```bash
codex plugin marketplace upgrade younsang-codex-plugins
```

## 프로젝트 범위로 설치

특정 프로젝트에서만 플러그인을 사용하려면 대상 프로젝트에 로컬 marketplace 항목을 추가합니다.

1. 프로젝트에서 `.agents/plugins/marketplace.json`을 만듭니다. 기존 파일이 있으면 `plugins` 배열에 다음 항목을 추가합니다.

   ```json
   {
     "name": "marketplace-name",
     "plugins": [
       {
         "name": "younsang-codex-plugin",
         "source": {
           "source": "url",
           "url": "https://github.com/nayounsang/younsang-codex-plugin"
         },
         "policy": {
           "installation": "AVAILABLE",
           "authentication": "ON_INSTALL"
         },
         "category": "Productivity"
       }
     ]
   }
   ```

   이미 marketplace 파일이 있다면 최상위 `name`을 유지하고, 기존 `plugins` 배열에 플러그인 객체만 추가하세요. 파일이 없다면 `name`은 자유롭게 설정할 수 있습니다.

2. 프로젝트의 `.codex/config.toml`에 다음을 추가합니다.

   ```toml
   [plugins."younsang-codex-plugin@marketplace-name"]
   enabled = true
   ```

3. Codex에서 대상 프로젝트를 신뢰된 프로젝트로 열고 새 스레드를 시작하면 설정이 적용됩니다.

## Features

### `api-scenario-forge`

AI가 CLI로 API 응답 시나리오를 원하는 대로 설정해 애플리케이션에서 확인하세요.

- 응답 본문을 자유롭게 설정하고 loading 상태, error, HTTP 상태코드를 지정해 애플리케이션에서 다양한 상황을 확인하도록 합니다.
- MSW와 [`@msw-dev-tool`](https://msw-dev-tool-docs.vercel.app/)을 기반으로 하며 Node와 Browser 환경을 지원합니다.
- 자세한 것은 [`docs/api-scenario-forge.md`](docs/api-scenario-forge.md)를 참고하세요.

### `strict-review`

Codex의 기존 빌트인 리뷰 스킬을 확장해 깊고 다양한 관점에서 리뷰받으세요.

- 정확성, 보안, 성능, 아키텍처, 네이밍, 테스트 품질, 의존성 도입 가능성, 생태계 활용을 체계적으로 검토하고 출력합니다. 따라서 기능이 잘 동작하는지 여부 뿐만 아니라 코드 품질(리팩토링), 성능 문제까지 파악 가능합니다.
- 리뷰 범위와 변경 형태에 따라 핵심 reviewer와 선택적 reviewer를 구성합니다.
- 자세한 것은 [`docs/strict-review.md`](docs/strict-review.md)를 참고하세요.

### `dev-docs-review`

작성한 개발 문서의 컨텐츠가 올바른지, 읽기 어려운 부분은 없는지 점검받으세요.

- 문서의 API, 명령, 설정, 사용자 여정, 링크와 생태계, 난잡한 표현을 점검합니다.
- 실행 가능한 수정 방향을 출력합니다.
- 자세한 것은 [`docs/dev-docs-review.md`](docs/dev-docs-review.md)를 참고하세요.

### `write-pr-content`

좋은 PR의 사례가 될 수 있는 Markdown fragment를 제공합니다.

- 기능 변경 명세, 외부 동작 다이어그램, 참고 링크, benchmark, UI 캡처,
  버그 재현 절차 중 필요한 것을 얻기 위한 독립적인 하위 스킬로 제공합니다.
- UI 캡처는 GitHub 업로드와 hosted URL 확인을 마친 뒤 임시 worktree 및
  캡처 파일을 함께 정리합니다.
- 자세한 것은 [`docs/write-pr-content.md`](docs/write-pr-content.md)를 참고하세요.

### [codex-complex-prompt](https://github.com/nayounsang/codex-complex-prompt)

문서 작업, 리서치 뿐만 아니라 프롬프트까지 직접 작성하고 AI와 함께 검토 가능한 에디터를 제공합니다. 그림, 다이어그래까지 제공하는 마크다운 에디터로 피드백 루프가 긴 채팅 대신 Codex에서 복잡한 작업을 해보세요.

- 자세한 내용은 [`docs/complex-prompt.md`](docs/complex-prompt.md)를 참고하세요.

#### 설치

다음 명령을 실행하거나 Codex CLI에서 `$install-complex-prompt` 스킬을 요청하세요.

```bash
npx @codex-complex-prompt/cli-bridge hook install
```

### `angry-insight`

> 왜 Codex는 `/insight`가 없을까.

Codex가 더 이상 바보같은 행동을 하지 말도록 유효한 잡도리를 하세요.
빡침을 표현하고 멋진 Agent로 직접 만들어보세요. ~~AI Agent 교육들을 필요가 없어질수도~~ 

- Codex에 보낸 프롬프트를 로컬에 수집합니다. 이 프롬프트들을 분석해 불만 사례 데이터를 얻습니다.
- 분석은 사용자가 `$angry-insight`를 명시적으로 실행할 때 시작됩니다.
- 사례에 맞는 자료(Codex·Anthropic 공식 자료, Hacker News, GitHub, npm 등)를 조사해 해결책과 실행 가이드를 제안합니다. 적용 가능한 기존 해결책이 없으면 AI 생성 아이디어로 표시합니다.
- 자세한 것은 [`docs/angry-insight.md`](docs/angry-insight.md)를 참고하세요.

## 추천 외부 도구

> nayounsang이 제작하지 않았으나, 외부에서 괜찮은 도구도 함께 제공합니다.

### [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)

UI UX Pro Max는 UI/UX 디자인 인텔리전스 스킬입니다.

- 웹·모바일·데스크톱 UI의 구조와 시각적 방향 설계
- 79개 UI 스타일, 192개 제품별 색상 팔레트, 74개 폰트 조합 검색
- 접근성, 반응형 레이아웃, 인터랙션, 애니메이션, 차트 UX 검토
- React, Flutter, SwiftUI, Tailwind, shadcn/ui 등 스택별 가이드
- 프로젝트 요구사항을 바탕으로 한 디자인 시스템 생성

#### 설치

```bash
# marketplace가 등록된 상태여야 합니다.
codex plugin add ui-ux-pro-max@younsang-codex-plugins
```

### [Plannotator](https://plannotator.ai/)

`install-plannotator` 스킬로 Plannotator를 설치하고 Codex 연동을 설정합니다.

- `$install-plannotator`를 요청하면 공식 설치 스크립트를 실행합니다.
- 설치 프로그램이 Codex 연동도 설정하므로 별도 설정은 필요 없습니다.
- 공식 설치 문서를 따라 직접 설치하는 방법도 권장합니다. ~~소개의 목적으로 플러그인에 포함한거지, 그냥 문서보고 직접 설치해주세요...ㅋㅋ~~
