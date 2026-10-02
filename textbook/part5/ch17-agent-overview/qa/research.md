# Ch 17 공식 자료 조사

- 조사일: 2026-09-10
- 범위: 워크플로우와 에이전트의 경계, 정지 조건, 추적 구조, 실제 제품의 공개 추적 단서
- 사용 원칙: 공식 제작사·공식 SDK 문서만 본문 근거로 사용했습니다. 특정 제품을 이 컴퓨터에서 실행한 것처럼 설명하지 않습니다.

## 확인한 내용

### 워크플로우와 에이전트

Anthropic의 공식 글은 워크플로우를 미리 정의한 코드 경로로 모델과 도구를 조정하는 시스템, 에이전트를 모델이 과정과 도구 사용을 동적으로 지휘하는 시스템으로 구분합니다. 고정 하위 작업으로 나눌 수 있는 문제에는 프롬프트 체이닝이 맞으며, 필요한 하위 작업을 미리 예측하기 어려운 코딩·검색 문제에는 동적 오케스트레이션이나 에이전트가 맞을 수 있다고 설명합니다. 에이전트는 환경 결과를 다시 받아 판단하는 루프와 최대 반복 같은 정지 조건이 필요하고, 비용과 오류 누적 가능성이 증가한다고 밝힙니다.

출처: https://www.anthropic.com/engineering/building-effective-agents

### OpenAI Codex 공개 추적 단서

OpenAI의 Codex 공식 소개는 사용자가 결과를 검증할 수 있도록 파일 인용, 터미널 로그, 테스트 결과를 제공한다고 설명합니다. 실패와 불확실성도 사용자에게 알리며, 소개 당시 클라우드 실행은 격리된 컨테이너 경계를 사용했습니다. 이 자료는 추적에서 관찰할 증거 유형을 확인해 주지만, 하나의 요청에 대한 전체 원시 사건 목록을 공개하지는 않습니다. 따라서 실습 JSON에는 세 증거 유형과 제한만 넣고 실제 실행 순서나 내부 추론은 추가하지 않았습니다.

출처: https://openai.com/index/introducing-codex/

### Anthropic Claude Code 공개 추적 인터페이스

Claude Code CLI 공식 문서는 `stream-json` 출력, `--verbose` 턴별 출력, `--max-turns` 최대 턴, `--max-budget-usd` 예산 상한, 도구 허용·거부 옵션을 공개합니다. 이는 모델이 수행한 턴을 관찰하는 인터페이스와 코드가 강제하는 정지·권한 경계를 구분할 수 있는 근거입니다. 실습에서는 실제 Claude Code 세션을 실행하지 않았으며 옵션과 사건 유형만 추출했습니다.

출처: https://code.claude.com/docs/en/cli-usage

### OpenAI Deep Research 공개 행동 경로

OpenAI의 Deep Research 공식 소개는 모델이 필요한 자료를 찾기 위해 다단계 경로를 계획하고 실행하며, 실시간 정보에 반응해 되돌아가기도 한다고 설명합니다. 업로드 파일 탐색, 웹 탐색, Python을 이용한 그래프 분석, 출처 인용이 공개된 행동 유형입니다. 이는 관찰 결과에 따라 다음 행동이 달라지는 제품 사례이지만 원시 내부 추론이나 특정 사용자 요청의 전체 로그는 아닙니다.

출처: https://openai.com/index/introducing-deep-research/

### 트레이스와 스팬

OpenAI Agents SDK 공식 문서는 트레이스를 한 워크플로우의 종단 간 기록, 스팬을 시작·종료 시각과 부모 관계를 가진 작업 단위로 설명합니다. 생성 스팬과 함수 스팬에는 입력·출력이 포함될 수 있어 민감 정보 수집을 끄는 설정도 제공합니다. Ch 17은 SDK를 설치하거나 에이전트를 만들지 않고 이 개념만 사용합니다.

출처: https://openai.github.io/openai-agents-python/tracing/

### SWE-agent 실제 공개 실행 궤적

SWE-agent 공식 저장소는 v0.7.0 demonstration 궤적을 `.traj` JSON으로 공개합니다. 사용한 파일은 커밋 `3ea751c087f32b16e039a2233dd6eefecef325d5`의 `marshmallow-code__marshmallow-1867.traj`이며 SHA-256은 `8856076ec31832f20aefa7f0a2714e3ad6bc752f14815d94d2e852e50213a459`입니다. 원문에는 14개의 action-observation 턴이 있습니다. 6번째 실행에서 344를 재현하고, 10번째 편집에서 `E999 IndentationError`로 거부된 뒤, 11번째 편집에서 들여쓰기를 수정하고 12번째 실행에서 345를 확인합니다. 마지막은 임시 재현 파일 삭제와 패치 제출입니다. 저장소 라이선스는 MIT입니다.

원문: https://raw.githubusercontent.com/SWE-agent/SWE-agent/3ea751c087f32b16e039a2233dd6eefecef325d5/trajectories/demonstrations/replay__marshmallow-code__marshmallow-1867__default__t-0.20__p-0.95__c-2.00__install-1___install_from_source/marshmallow-code__marshmallow-1867.traj

설명: https://github.com/SWE-agent/SWE-agent/blob/3ea751c087f32b16e039a2233dd6eefecef325d5/docs/usage/trajectories.md

라이선스: https://github.com/SWE-agent/SWE-agent/blob/3ea751c087f32b16e039a2233dd6eefecef325d5/LICENSE

### mini-SWE-agent 실제 공개 실행 궤적

mini-SWE-agent 공식 저장소의 `tests/test_data/github_issue.traj.json`은 assistant 명령과 user 도구 결과를 교대로 담은 실제 fixture입니다. 사용한 커밋은 `04d809ceab9df28f9adaed044884180159172930`, SHA-256은 `86d060a4881efc19b59b4ee6667b1c80b2b769544d4f6cecb42521e09e95c6a0`입니다. 첫 절대 경로 읽기는 반환 코드 1로 실패하고, 저장소와 tests 폴더를 확인한 뒤 상대 경로를 찾습니다. 문법 오류를 고친 뒤 출력 8.2를 확인하지만, 원래 입력 23÷0에서 `ZeroDivisionError`가 발생해 0 검사를 추가합니다. 마지막 행동은 시스템 지시가 요구한 단독 완료 명령에 git 명령을 결합했으며 반환 코드 래퍼도 없습니다. 따라서 코드 실행 성공, 요청 범위 준수, 종료 규칙 준수를 별도로 평가해야 합니다. 저장소 라이선스는 MIT입니다.

원문: https://raw.githubusercontent.com/SWE-agent/mini-swe-agent/04d809ceab9df28f9adaed044884180159172930/tests/test_data/github_issue.traj.json

라이선스: https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/LICENSE.md

## 버전과 범위

Ch 17의 실행 예제는 Python 표준 라이브러리만 사용하므로 LangChain 1.4·LangGraph 1.2 API에 의존하지 않습니다. Claude Code와 Codex의 제품 옵션은 교재 확인일 이후 바뀔 수 있습니다. 학생 실습 파일에는 확인일과 URL을 남겼으며, 실제 제품 도입 시 현재 문서를 다시 확인해야 합니다.

## 확인 필요 항목

Codex·Claude Code·Deep Research의 완전한 단일 실행 원시 로그는 공식 소개·문서에서 확보하지 못했습니다. 이 세 자료는 공식 추적 단서로만 사용합니다. 대신 SWE-agent와 mini-SWE-agent 공식 저장소의 공개 실행 궤적 두 건을 커밋과 해시로 고정해 사건 순서를 분석했습니다. 두 제품을 현재 환경에서 다시 실행하거나 외부 평가로 패치 정답을 확인하지는 않았습니다.
