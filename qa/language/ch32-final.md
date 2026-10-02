# Ch32 Docker 한국어 감사 기록

## 범위와 기준

- 대상: 교재 절 5개, 노트북 마크다운 5개, `labs/part7/ch32-docker/README.md`, 도식 SVG 5개
- 장르: 산문 · 최소 심각도: S1
- 초기 기준본: `qa/language/baseline/ch32-src/`, `qa/language/baseline/ch32-notebook-markdown/`
- 기술 재실행 직후 기준 SHA-256: `qa/language/ch32-post-tech-sha256-before-language-final.txt`
- 최종 SHA-256: `qa/language/ch32-final-sha256.txt`

## 진단 요약

이미지 레이어, 멀티스테이지 빌드, 캐시와 이미지 크기, Compose·pgvector, 환경변수·시크릿·상태 확인을 실제 실행 범위와 함께 설명합니다. 전문을 독자, 편집자, 낭독 관점으로 세 번 읽었습니다. 문단마다 수치·날짜·고유명사·기술적 양태와 노트북 결과를 대조하고, 교재 문어체 금지 표현, 번역투, 이중 피동, 수사적 대조를 다시 검색했습니다.

외부 맞춤법 검사는 상업적 대량 처리 금지 정책 때문에 전체 원문을 전송하지 않았습니다. 코드 블록·명령어·경로를 제외하고 전문을 로컬에서 정독하여 띄어쓰기, 조사와 어미 호응, 수량 표현, 표준 문어체를 점검했습니다.

## 정독 소견

- 독자: Docker 이미지와 Compose 실행 환경을 처음 실제로 확인하는 수강생
- 목적: 빌드 결과와 실행 중 상태를 구분하고, 실제 측정값의 범위와 한계를 함께 설명합니다.
- 전체 인상: 각 절이 개념, 실행, 관찰 결과, 한계로 자연스럽게 이어집니다. 기술적 대조는 원리를 구분하는 데 필요하므로 보존했습니다.

### 고친 자리

| 위치 | 수정 | 근거 |
| --- | --- | --- |
| 01~05절 `확인할 점` | `task 전용 이름` → `실습 전용 이름` | 학생용 교재의 한국어 문어체로 통일 |

### 손대지 않은 자리

- 노트북 마크다운은 이미 `실습 전용`으로 정리돼 있어 수정하지 않았습니다.
- 기준 이미지 418,111,662바이트, 최적화 이미지 57,560,686바이트, 감소율 86.2%와 모든 코드·실행 출력·날짜·기술적 한정어는 보존했습니다.
- 실패 확인용 `buidler` 표기는 의도한 오류 재현의 일부이므로 보존했습니다.

## 수정 텍스트 경로

- `textbook/part7/ch32-docker/_src/01-이미지와-레이어.html`
- `textbook/part7/ch32-docker/_src/02-uv-멀티스테이지-빌드.html`
- `textbook/part7/ch32-docker/_src/03-빌드-캐시와-이미지-크기.html`
- `textbook/part7/ch32-docker/_src/04-Compose와-pgvector-스택.html`
- `textbook/part7/ch32-docker/_src/05-환경변수-시크릿-헬스체크-로그.html`

## 도식과 실행 자료 확인

다섯 SVG는 모두 완결된 `aria-label`과 화살표를 제공하며, 상자 색·레이블·화살표·캡션의 설명이 일치합니다. 03절의 최신 이미지 크기와 감소율은 `_src`, 생성 HTML, 노트북 출력, `textbook/part7/ch32-docker/qa/verification.md`에서 모두 같습니다.

언어 감사 전후 노트북 코드·출력 해시는 일치합니다. 비교 기록은 `qa/language/ch32-notebook-code-output-sha256-post-tech.txt`와 `qa/language/ch32-notebook-code-output-sha256-final.txt`입니다. 노트북 마크다운 해시도 `qa/language/ch32-notebook-markdown-sha256-post-tech.txt`와 `qa/language/ch32-notebook-markdown-sha256-final.txt`에서 일치합니다.

## 기계 점검과 최종 검수

- `_build.py`: 챕터 색인과 5개 절 생성
- `verify.py`: `PASS 5 sections / 23 code cells (max 13 lines)`
- `verify_gates.py`: 절별 기록은 `qa/language/ch32-*-verify-gates-final.txt`에 보관했습니다. P0의 저윤문 WARN은 2.5~3.8%의 국소 수정률입니다. 04절 P1 WARN은 의미상 필요한 기술 대조를 보존한 결과입니다. 03절 P3 numbers WARN은 기술 재실행으로 갱신한 이미지 크기이며 노트북 출력과 일치합니다. 01·05절 P3 quotations FAIL은 언어 감사 전에 이뤄진 코드 표기와 도식 캡션 갱신이 초기 기준본의 인용 표기와 달라졌기 때문입니다. 이번 윤문으로 수치·인용·코드·출력은 변경하지 않았습니다.

Phase 6에서는 원문과 최종본을 문단 단위로 대조해 사실·주장·수치·날짜·고유명사·인용·예시·한정어·제목 독립성·문단 순서를 확인했습니다. 새 주장이나 수사, 과도한 격식화와 문학화가 없으며, 다섯 국소 수정은 Docker 자원 변경 범위라는 본래 의미를 유지합니다.

최종 검수: `corrected`

- 의미 보존 15항: 통과
- 자연성 잔존: 학생용 안내의 영문 명사 한 곳을 다섯 절에서 국소 보정
- 과윤문: 없음
- 게이트 재확인: exit 1. 위의 초기 기준본 대비 기술 갱신과 저윤문 경고를 정독으로 판정했습니다.

## 확인 필요 항목

없음.
