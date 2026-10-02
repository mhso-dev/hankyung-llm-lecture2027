# Ch 1 최종 검증

2026-09-09 작성. 결과: 교재 집필·노트북 실행·주제 검토·화면/복사·배포 검증 완료. 아래의 미검증 범위는 완료 주장에 포함하지 않습니다.

## 산출물

- HTML: 챕터 목차와 개념 5절. `_src/` 원본과 `chapter.json`, 공통 템플릿을 사용하는 `_build.py`로 생성합니다.
- 시수: 강의 5h·실습 3h, 총 8h. 각 절 산문은 약 2,500자 이상이며 총 20개 복습 문항·해설과 별도 A/B 자가진단 6과제·답안이 있습니다.
- 노트북: 5개·25개 코드 셀. 최대 19줄, Python 3.12.13 새 커널 순차 실행. 코드/출력 해시를 검증했습니다.
- 도식: SVG와 편집 가능한 Excalidraw JSON 5쌍. 실제 예제와 같은 경로·연산·환경 관계를 표현합니다.
- 실습 배포: `textbook/downloads/ch01-practice.zip`, 노트북 5개와 README·hello.py·pyproject.toml·uv.lock. 전체 `llm-practice.zip`은 55개 실습 파일로 갱신했습니다. 학생 시작 화면에 Ch 1을 추가했습니다.

## 실제 확인한 결과

| 검증 | 결과 | 근거 |
|---|---|---|
| 새 커널 실행 | 5/5 PASS, 총 25셀, Python 3.12.13 | 각 ipynb metadata.verification, qa/execution.md |
| HTML·코드·출력·다운로드 | 5절·25셀 모두 일치, 최대 19줄 | 공통 checks/notebook-contracts-part1-ch01-development-environment.json |
| PC/모바일 화면·복사 | 1280px·390px × 6페이지 = 12건 PASS | 공통 checks/ch01-development-environment/visual-results.json |
| 글자·대비·잘림 | 본문16px/보조14px 이상, 대비 기준 통과, 잘림·가로 넘침·영역 밖 텍스트 0 | 같은 화면 검사 기록 |
| 공통 도구 테스트 | 37 passed, 16 subtests passed | textbook/_notebook/tests 실행 |
| 정적 검사 | 변경 빌더·배포 도구·도식 생성기 Ruff E9/F63/F7/F82 통과 | 실제 검사 실행 |
| 도구 미발견 환경 | PATH에 Git·uv·Docker가 없어도 05절이 미준비를 기록하고 완료 | qa/missing-tools.json |
| 진단 예제 추가 조건 | 수량 4, 실제 합계 12000 | qa/diagnostic-check.json |
| 독립 교육·기술 검토 | PASS | qa/topic-review.md |
| 한국어 최종 전문 정독 | corrected, 의미 보존·과윤문 검수 통과 | qa/language/04-final-language-audit.md |
| 배포 파일 재현 | ZIP을 새 임시 폴더에 풀고 uv sync --locked·버전·hello.py 실제 실행 통과 | qa/delivery-check.json |
| 파일·개인정보 | 내부 파일 링크 33개 정상, ZIP에 개인 절대 경로·비밀값·.env·.venv 없음 | qa/delivery-check.json |

화면에서 셀별 복사·전체 복사·내려받은 노트북을 원본과 대조했습니다. 전체 비교형은 기본 실행 후 실제 실패/수정이 이어지고, 실험 해석형은 실행 코드를 예제 블록에 한 번만 배치합니다. 공통 실행기의 비밀값 검사와 추가 배포 검사는 실제 키 값 자체를 로그에 기록하지 않았습니다.

## 검토 중 수정한 주요 내용

기본 정상 실행을 경로·계산 실패보다 앞에 추가했습니다. stdlib 가상환경 생성이 uv 관리 Python에서 실행되지 않는 문제를 확인해 실제 실행 가능한 uv venv로 바꿨습니다. 가상환경의 상태를 셸 활성화로 오해할 수 있는 문구, 실행하지 않은 패키지 충돌과 반복 실험 주장을 제거했습니다. 준비 상태 점검과 A/B 학습 수준 자가진단을 분리하고, 각 진단의 답안과 다음 학습 경로를 명시했습니다.

## 확인 필요 항목

1. **A/B 트랙 공식 배치 기준은 미정입니다.** 05절은 비공식 자가진단·답안·학습 안내를 제공하며 공식 성적이나 기관의 확정 기준으로 표시하지 않습니다.
2. **OS별 신규 앱 설치와 VS Code 디버거 GUI 조작은 미검증입니다.** 공식 Windows/macOS/Linux 설치 안내를 확인했고, macOS의 Python·uv·Git·pdb 및 Docker 응답을 실제 실행했습니다. Windows/Linux 신규 설치 화면과 VS Code F5/F10 화면을 실행 검증했다고 주장하지 않습니다.
3. **Docker는 클라이언트·서버 응답 범위만 확인했습니다.** 이 호스트에서는 둘 다 29.4.1로 응답했습니다. 이미지 다운로드·컨테이너 생성/실행은 후속 챕터 범위이며 이번에 실행하지 않았습니다.
4. **Excalidraw MCP 미리보기는 미지원입니다.** 생성기에서 편집 가능한 JSON과 SVG를 함께 만들고 화면·구조를 검사했습니다. 교육 목적에 도식이 충분하여 생성형 삽화를 추가하지 않았습니다. 이미지 크레딧 사용 0.
5. **외부 맞춤법 검사는 생략했습니다.** [korean-spell-check SKILL.md](/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-spell-check/SKILL.md)의 “대량 배치, SaaS 백엔드 연동, 상업 서비스 내 무단 재판매·재노출에는 사용하지 않습니다.” 제한에 따라 원문을 전송하지 않았습니다. 일반 슬롭 검토, 로컬 맞춤법·윤문, 다른 검토자의 Phase 6 전문 정독을 수행했습니다.
6. **문체 자동 지표에는 경고가 남습니다.** 교재의 반복 용어·단계별 문장에 산문 essay 기준선이 적용되어 높은 위험 지표와 낮은 변경률 경고가 나왔습니다. 이를 무조건 통과로 처리하지 않았으며, 검토자가 전문을 읽어 설명·절차·문제 문맥을 확인했습니다. 최종 판정은 corrected입니다.

## 품질 개선과 챕터 끝 실습 절 (2026-09-16)

규격 `textbook/QUALITY-UPGRADE.md`로 01~05절을 다시 쓰고, 챕터 끝 실습 절 `06-개발환경-실습`(「개발환경 실습: 새 연습 폴더 점검하기」)을 붙였습니다. 위의 「산출물」「실제 확인한 결과」는 개선 전 판본(5절·25셀, Excalidraw 도식, macOS 실행)의 기록입니다.

- 실행 환경: Cowork 기기 VM(Linux aarch64), Python 3.12.13, uv 0.12.3, git 2.34.1, docker 없음. 모델 호출 0번.
- `execute.py`: 6개 노트북을 새 커널에서 실행해 모두 PASS(코드 셀 11·12·14·14·14·19개). 검토 1차 반영 뒤 다시 실행한 출력은 반영 전과 글자 단위로 같았습니다.
- `verify.py --chapter`: `PASS 6 sections / 84 code cells (max 14 lines)`.
- `upgrade_gates.py --label after --strict`: G1~G7 모두 0건, 6/6절 통과. 수정 전(5절)은 G1 2·G2 1·G3 11·G4 0·G5 29·G6 197·G7 15, 합계 255건이었습니다.
- `visual.cjs`: 목차와 6절, 7페이지 × 1280px·390px, 14건 모두 PASS(가로 넘침·잘림·깨진 이미지·복사 오류 0).
- 그림: Mermaid 23장(절마다 3~4장)과 삽화 6장(nano_banana_pro, 절마다 1장). PNG를 직접 열어 방향·색·라벨을 확인했습니다.
- 사다리: 환경 챕터 예외(규격 §2 끝)로 표준 라이브러리 import와 결과 값의 메서드를 씁니다. 해당 코드 셀 67개에 `upgrade_allow=["stdlib-import"]`를 적었습니다.
- 실습 절 결과: 실행 1(작업 폴더 practice) True 5칸, Docker 칸만 False. 실행 2(한 칸 위 임시 폴더) True 2칸, 달라진 칸 3, 종료 코드 2(`can't open file`)·128(`not a git repository`).
- 별도 세션 검토 1회(`qa/upgrade/review-round1.md`): 6절 모두 accept-with-fixes, 상 0·중 11·하 27. 사실 오류 두 건을 다시 확인하고 고쳤습니다. 인자 없는 `git diff`는 기록할 목록(index)과 파일을 비교합니다(공식 문서, 기기 셸에서 `git add` 전 7줄·뒤 0줄). 실습 폴더 `hello.py`는 빈 줄을 지워 본문의 네 줄과 맞췄습니다. 반영 내역은 보고서 끝 「반영 결과」와 각 `qa/upgrade/NN-diagnosis.md`에 있습니다.
- 챕터 요약: `qa/upgrade/chapter-summary.md`(다음 챕터 작업자용).

### 확인 필요 항목 (품질 개선)

- 실습 묶음 `textbook/downloads/ch01-practice.zip`은 개선 전 파일입니다(06 노트북 없음, `hello.py` 다섯 줄). 전체 챕터가 끝난 뒤 다시 만듭니다.
- A/B 트랙 공식 배치 기준은 미정입니다. 학생 문장은 「첫 주에 강사가 안내합니다」이고, `[[미정: …]]` 표시는 HTML 주석으로 남겼습니다.
- Docker가 설치된 컴퓨터의 05·06절 출력, VS Code 디버거·커널 선택 화면, Windows 출력은 이번에 실행하지 않았습니다.
- 강사 확인이 남았습니다.
