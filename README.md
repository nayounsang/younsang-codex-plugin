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
