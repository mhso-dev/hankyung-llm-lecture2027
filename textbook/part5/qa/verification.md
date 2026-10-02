# Part 5 교재 완료 검증

검증일: 2026-09-10. 학생 시작점은 [Part 5 목차](../index.html), 실습은 [Part 5 ZIP](../../downloads/part5-practice.zip)입니다. Ch 17–20의 21개 절과 실행 노트북 21개, SVG·편집 가능한 Excalidraw 21쌍, 해설을 갖춘 복습 86문항을 작성했습니다. 강의 18시간·실습 30시간이며 전체 교재는 Ch 1–20의 138절입니다.

## 범위와 검증 결과

| 항목 | 확인 결과 | 근거 |
|---|---|---|
| 장별 구성 | Ch 17 5절, Ch 18 6절, Ch 19 6절, Ch 20 4절 | `scope-summary.json` |
| 실행 코드 | 151셀, 셀당 최대 24줄, 노트북 21개 새 커널 순차 실행 | 노트북 `metadata.verification`, `notebook-readiness.json` |
| HTML 대조 | 코드·실제 출력·내장 노트북 다운로드와 정본 일치 | `integration-results.json` |
| 페이지·링크 | 27개 HTML, 로컬 링크 395개, 누락 0개 | `delivery-results.json` |
| 화면·복사 | 1280px·390px 합계 54건 통과 | `*-visual-summary.json`, `../../_notebook/checks/` |
| 도식 | 21쌍의 라벨·화살표 대조, 경계·모바일 표시 확인 | `figure-consistency.json`, `figure-previews/` |
| 회귀 검사 | 44 passed, 26 subtests passed | `common-technical-review.md` |
| 배포 | Part 5 ZIP 59항목, 전체 ZIP 269항목, 정본·manifest 해시 일치 | `delivery-results.json` |
| 독립 폴더 실행 | ZIP 압축 해제 후 잠금 환경 설치, 대표 오프라인 노트북 3개 실행 | `bundle-execution.json` |
| 비공개 자료 | 실제 키·가상환경·캐시·비공개 전체 질문셋을 배포하지 않음 | 배포 검사와 공개 파일 목록 |

화면 검사는 작은 글자, 명암, 잘림, SVG 경계, 페이지 가로 넘침, 이미지 누락, 셀/전체 복사, 다운로드와 실패·수정 배치를 확인했습니다. Ch 20의 모바일 실행 경로 문자열은 화살표 주변에 공백을 넣어 줄바꿈되도록 수정했습니다. 원고의 각 절은 학습 목표부터 참고 자료까지 고정 구조를 따르며 신규 용어를 7개 이내로 구성했습니다.

## 실행과 기술 검토

Python 3.12.13·uv 잠금 환경에서 검증했습니다. 사용한 패키지는 LangChain 1.4.0, langchain-openai 1.6.0, LangGraph 1.2.11, OpenAI 2.29.0, Pydantic 2.12.5입니다. Ch 18은 직접 OpenAI SDK를 사용하고, Ch 19·20은 도입 범위에 맞는 LangChain·LangGraph API를 사용합니다. 공통 검사기의 직접 SDK 예외는 Ch 18 경로에만 적용되도록 회귀 검사를 추가했습니다. 공개 파일의 중간 경로에 있는 심볼릭 링크도 거부하도록 배포 도구를 보완했습니다.

Ch 17의 합성 계산은 실측과 구분하며 공개 궤적의 원본·커밋·MIT 라이선스를 대조했습니다. Ch 18의 실제 API 실험은 게이트·실패 라우팅·동적 워커·평가 종료 조건을 검증하고 동일 과제의 다섯 패턴 결과를 기록했습니다. Ch 19는 반환 스키마 검증, 호출 결과 ID 연결과 주문 ID에 결합된 애플리케이션 확인 상태를 검증했습니다. Ch 20은 실제 도구 순환, 오류 결과 반환, 반복 제한 예외와 정상 종료, 같은 그래프에서 고정 선택과 모델 선택을 확인했습니다.

장별 근거: `ch17-technical-review.md`, `ch18-technical-review.md`, `ch19-technical-review.md`, `ch20-technical-review.md`. 공통 검토: `common-technical-review.md`. 원본 출처: `ch17-source-evidence.json` 및 각 장 `qa/research.md`와 학생용 참고 자료.

## 한국어 검토

장별 집필자와 분리된 검토자가 일반 슬롭·맞춤법·문맥·의미를 확인했습니다. `language/ch17-final.md`, `language/ch18-final.md`, `language/ch19-final.md`, `language/ch20-final.md`와 `language/part5-guides-final.md`가 승인 기록입니다. 코드·실행 출력·수치·URL은 보호하고 실제 기술 수정은 재실행했습니다. 통합 담당자의 최종 의미 대조는 `independent-meaning-review.md`에 기록했습니다.

외부 맞춤법 전송은 [korean-spell-check SKILL.md](/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-spell-check/SKILL.md:35)의 **“상업적 대량 처리”** 금지에 따라 생략했습니다. 이 교재 여러 절의 일괄 전송에 해당한다고 판단했으며 로컬 정독으로 맞춤법을 확인했습니다. 외부 맞춤법 서비스를 사용했다고 주장하지 않습니다.

## 확인 필요 항목과 남은 제한

- 실제 API 청구액은 청구서로 대조하지 않았습니다. 본문의 비용은 실제 사용량과 수록 단가를 사용한 추정이며 재실행할 때 모델 답변·지연·비용이 달라질 수 있습니다.
- Ch 17의 제품 분석은 고정된 공개 데모·테스트 기록입니다. 현재 버전 제품들을 동일 조건으로 새로 실행한 성능 비교가 아닙니다.
- macOS에서 실행했습니다. Windows/Linux의 환경 설치와 화면은 직접 실행하지 않았습니다.
- 노트북 Ruff에는 Ch 18의 미사용 import 7건·세미콜론 9건, Ch 20의 미사용 import 3건 등 **LOW 19건**을 남겼습니다. 기능 검토는 승인됐지만 스타일 진단이 모두 0건인 상태는 아닙니다. 상세는 `ch18-lint-findings.json`·`ch20-lint-findings.json`입니다.
- Excalidraw MCP 미리보기를 사용할 수 없어 같은 도형 명세로 SVG와 편집 가능한 Excalidraw JSON을 생성하고 요소·화면을 검증했습니다. 생성형 삽화는 사용하지 않았으며 Higgsfield 사용량은 0크레딧입니다.

## 유지보수와 최종 파일

학생 본문의 정본은 각 챕터 `_src/`, 실행 코드·출력의 정본은 `labs/part5/.../notebooks/*.ipynb`입니다. 이를 `_build.py`로 빌드하고 Part 5 `_build_index.py`와 공통 배포 도구로 묶습니다. `_author.py`, `author_chapter.py`, `_make_sources.py` 같은 초기 초안 작성 도구로 감사 완료 원고를 덮어쓰지 않습니다. 도식의 최종 명세는 각 `figures/` 생성기와 원본 파일입니다.

최종 파일 해시는 `final-manifest.json`, ZIP 해시는 `delivery-results.json`에 기록합니다. 검증 보고서의 링크는 프로젝트 내부 기록을 가리킵니다.
