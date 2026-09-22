# Younsang Codex Plugin

nayounsang이 Codex와 개발할 때 사용하는 유틸리티 모음입니다.

스킬별 설명과 사용 방법은 [docs](docs/)를 참조하세요.
개발 및 추가 작업 절차는 [개발 워크플로우](docs/development-workflow.md)를
참조하세요.

## 설치

로컬 marketplace를 등록한 뒤 플러그인을 설치합니다.

```bash
# 최초 1회: 플러그인을 포함한 로컬 marketplace 등록
codex plugin marketplace add /path/to/marketplace-root

# 플러그인 설치
codex plugin add younsang-codex-plugin@<marketplace-name>
```

Personal marketplace를 이미 사용 중이라면 다음 명령으로 설치할 수 있습니다.

```bash
codex plugin add younsang-codex-plugin@personal
```

설치 후 새 Codex thread를 시작하면 플러그인의 스킬을 사용할 수 있습니다.

## Features

### `api-scenario-forge`

AI가 CLI로 API 응답 시나리오를 원하는 대로 설정해 애플리케이션에서 확인하세요.

- 응답 본문을 자유롭게 설정하고 loading 상태, error, HTTP 상태코드를 지정해 애플리케이션에서 다양한 상황을 확인하도록 합니다.
- MSW와 [`@msw-dev-tool`](https://msw-dev-tool-docs.vercel.app/)을 기반으로 하며 Node와 Browser 환경을 지원합니다.
- 자세한 것은 [`docs/api-scenario-forge.md`](docs/api-scenario-forge.md)를 참고하세요.

### `strict-review`

Codex의 기존 빌트인 리뷰 스킬을 확장합니다.

- 정확성, 보안, 성능, 아키텍처, 네이밍, 테스트 품질, 의존성 도입 가능성, 생태계 활용을 체계적으로 검토하고 출력합니다.
- 리뷰 범위와 변경 형태에 따라 핵심 reviewer와 선택적 reviewer를 구성합니다.
- 자세한 것은 [`docs/strict-review.md`](docs/strict-review.md)를 참고하세요.
