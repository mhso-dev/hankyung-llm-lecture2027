# Ch27 DeepAgents 기술 근거 검토

검토일: 2026-09-11 · 범위: Ch27 8절, 노트북·README의 실행 범위, 도식

## 판정

DeepAgents 0.7.0의 설치 소스·실행 출력과 현재 공식 문서를 대조했습니다. 각 절이 소스 검사, 로컬 백엔드 입출력, 실제 OpenAI 모델 호출, 고정 문자열 도구의 범위를 구분하도록 확인했습니다. 03절의 저장 출력과 달랐던 할 일 상태 설명은 기술 보정 기준선에서 고쳤습니다.

## 공식 근거

- [Deep Agents overview](https://docs.langchain.com/oss/python/deepagents/overview) — Deep Agents가 LangChain·LangGraph 위의 에이전트 하네스이며 파일시스템·서브에이전트·문맥 관리를 제공한다고 설명합니다.
- [Deep Agents backends](https://docs.langchain.com/oss/python/deepagents/backends) — 가상 파일시스템의 `ls`, `read`, `write`, `edit`, `delete`, `glob`, `grep`와 실행 지원 백엔드에서만 가능한 명령 실행을 구분합니다.
- [Deep Agents subagents](https://docs.langchain.com/oss/python/deepagents/subagents) — 서브에이전트의 분리된 문맥과 부모에게 반환하는 최종 결과의 경계를 설명합니다.
- [DeepAgents 0.7.0 release](https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.0) — 0.7.0 기준의 변경을 확인하는 릴리스 기록입니다.
- [OpenAI gpt-5.4-mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini) — 2026-09-11에 확인한 이 장의 모델·가격 가정의 공식 기준입니다.

## 실행 범위 대조

- 01절은 `create_deep_agent` 설치 소스에 조립 경로가 있는지를 검사합니다. 일곱 항목이 True라는 출력은 기능 품질이나 활성 상태의 증명이 아닙니다.
- 02·03·05·06·07·08절은 저장된 실행에서 `gpt-5.4-mini` 모델을 호출합니다. 02는 `course_lookup` ToolMessage, 03은 두 `write_todos`, 06은 부모의 `task`, 08은 허용 쓰기와 거부 ToolMessage를 확인합니다.
- 04절은 모델을 호출하지 않고 `FilesystemBackend`의 실제 로컬 쓰기·읽기·목록 조회를 확인합니다.
- 05절의 `large_result`와 06·07절의 `source_lookup`은 의도적으로 만든 고정 자료입니다. 07절은 실제 웹 탐색이 아니라 제공한 overview·release 문자열만 조사하는 범위입니다.
- 03절의 5,395→1,895와 64.9%는 노트북 API 호출의 절감률이 아니라 릴리스 PR의 gpt-5.5 hello 첫 턴 수치를 재계산한 값입니다.

## 기술 보정과 한계

- 03절 실제 출력은 `버전 확인`과 `결과 설명`이 모두 `completed`입니다. 본문과 정리의 `결과 설명 in_progress` 주장을 모두 실제 출력과 같게 고쳤습니다. 생성 초안 스크립트는 재생성 시 기존 정본을 중단하도록 보호되어 있습니다.
- 05절은 ToolMessage가 알려 준 이번 호출의 경로를 정규식으로 읽어 해당 파일만 검사하고, 저장 본문이 `'근거 문장입니다. ' * 3000`과 일치하는지 확인하도록 보강했습니다. 이전 실행의 잔존 파일이 `any()` 검사를 통과시키는 문제를 없앴습니다.
- 04·05·07·08절의 작업 경로와 07절 `.env` 탐색은 노트북 작업 디렉터리에 의존하지 않고 상위 폴더에서 프로젝트 루트를 찾도록 보정된 실행 기록을 최종 기준으로 사용합니다.

## 도식

도식은 파랑=학생 코드·실행 흐름, 보라=모델 판단, 초록=도구·데이터, 노랑=측정, 빨강=실패·권한 경계로 역할을 맞췄습니다. 모델 판단이 아닌 `CompiledStateGraph`, 격리 문맥, 통합 실행 코드는 보라색에서 각각 데이터·코드 역할로 옮겼고, source-reviewer의 모델 판단만 보라색으로 표시했습니다.

## 버전 주의

현재 공식 문서는 0.7.0 이후의 기능을 포함할 수 있습니다. 이 장의 사실 주장은 설치한 `deepagents==0.7.0` 소스와 0.7.0 릴리스 기록을 우선으로 읽어야 하며, 후속 패키지 갱신 때는 다시 대조해야 합니다.
