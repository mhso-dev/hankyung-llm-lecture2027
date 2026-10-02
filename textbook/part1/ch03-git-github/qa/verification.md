# Ch 3 검증 기록

개선 전 실행·화면 검증(2026-09-09)은 `qa/execution.md`에 있습니다. 이 파일은 품질 개선(2026-09-16)과 별도 세션 검토 1차 반영 뒤의 검증을 적습니다. Ch 2 `qa/verification.md`와 같은 방식입니다.

## 품질 개선 01~05절과 실습 절 06 (2026-09-16)

- 규격 `textbook/QUALITY-UPGRADE.md`로 01~05절을 다시 쓰고 §7-2 실습 절 06(Git 실습: 할인율 설정 PR 합치기, experiment)을 새로 만들었습니다. 생성기 `qa/upgrade/author_01.py`~`author_06.py`, 진단 `qa/upgrade/NN-diagnosis.md`, 절 사이 인계 `qa/upgrade/handoff.md`.
- 절마다 `run_section.sh`로 새 커널 실행 PASS, 게이트 G1~G7 0건(`qa/upgrade/gates-wip-NN.json`, 챕터 `gates-wip-all.json` 6/6). 모델 호출 0번.
- 그림: Mermaid 26장(절마다 PNG 직접 확인), 삽화 6장(Higgsfield nano_banana_pro, 절당 1장·재생성 1회 이내, job id와 크레딧은 각 `figures/NN-k-*.prompt.md`). 수정 전 파일은 `qa/upgrade/before/`.
- 동작 근거: 각 절 「참고 자료」의 Git·GitHub 공식 문서(확인일 표기)와 교재 환경 실행 출력. 05절 도구 동작은 git-filter-repo 2.47.0 README·소스와 기기 셸 실행(`05-diagnosis.md`), 검토 세션이 따로 확인한 동작은 `review-round1.md`의 [확인] 표시.

## 별도 세션 검토 1차 반영과 챕터 마감 (2026-09-16)

- 검토 보고서: `qa/upgrade/review-round1.md`(§01~06, 상 0·중 4·하 23). 반영 중 4/4·하 23/23, 미반영 없음. 항목별 반영은 보고서 끝 「반영 결과」, 절별 기록은 각 `qa/upgrade/NN-diagnosis.md` 「검토」 절에 있습니다.
- 재실행: 01~06 `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch03-git-github NN` 새 커널 PASS(Linux, Python 3.12.13, Git 2.34.1, git-filter-repo 2.47.0). 코드 셀 출력은 커밋 해시·임시 경로·실행 시간을 빼고 반영 전과 같습니다. 달라진 것은 02절 config 셀을 복제 셀에 합친 경계(출력 줄은 같음)와 `PR 설명 글:` 한 줄, 03절 라벨 줄 세 개(`작성자의 message.txt:`, `출고 기준 policy.txt:`, `리뷰어의 message.txt:`)입니다.
- `upgrade_gates.py textbook/part1/ch03-git-github --label after --strict`: 6/6절 G1~G7 0건(`qa/upgrade/gates-after.json`). 코드 셀 19·22·19·19·17·16 = 112, 검사한 문장 349·455·363·375·366·339. 수정 전(`gates-before.json`, 5절) G1 17·G2 3·G5 43·G6 155·G7 15, 합계 233건.
- `verify.py --chapter`: `PASS 6 sections / 112 code cells (max 18 lines)`.
- `visual.cjs`: 목차와 6절, 7페이지 × 1280·390px, 14건 PASS(가로 넘침·잘림·깨진 이미지·복사 오류·작은 글자 0). 기기 VM에 Playwright가 없어 Ch 2 마감 때 `/tmp/pw`에 설치한 playwright-core 1.63.0과, puppeteer Chrome 153 headless shell을 실행 파일로 지정하는 `playwright` 모듈을 `NODE_PATH=/tmp/pw/node_modules`로 불러 돌렸습니다. 처음 실행에서 02-3(viewBox 870)·04-4(885)·05-3(928)의 SVG 글자가 본문 축소 뒤 14px 미만(13.1~13.98px)이라 실패했고, 라벨을 줄여 806·806·851로 다시 렌더해 통과했습니다.
- 다시 렌더한 그림(PNG 직접 확인): 01-2(.env 상태 표시 라벨), 02-1(작성자 쪽 `git clone`·`git fetch`), 02-3·04-2·05-3·06-2(실선 요청 → 점선 응답, `messageAlign: left`, 한 줄 라벨), 04-4(라벨 세 줄).
- 삽화 05-5: 채택 job `7bc1a6fa-087c-472c-9273-023b5dc5beea`와 탈락 job `fd474ddb-e478-4947-95ed-8cf7d2abaeaf`의 결과를 Higgsfield에서 다시 받아(새 생성 없음) 폭 1100px로 줄여 저장본과 비교했습니다. 저장본은 탈락본과 평균 픽셀 차이 0.0이었습니다. 채택본을 1100×614로 교체하고 그림 읽기·alt·캡션과 맞는지 확인했습니다. 추가 크레딧 0.
- 규격 문서 추가: `QUALITY-UPGRADE.md` §6 외부 도구 챕터의 준비물 기준 버전, §5-3 sequenceDiagram 받아 오기(실선 요청 → 점선 응답)와 라벨 겹침 처리(`messageAlign: left` + 한 줄), §5-4 삽화 저장본을 채택 job 결과와 대조. `PLAYBOOK.md` §4 세 줄.
- 함께 고친 곳: 실습 폴더 `labs/part1/ch03-git-github/README.md`(기준 Git 버전, 06절 한 문장), `qa/upgrade/handoff.md` §03→§04 참조 기록 정의 표시, 설계표 02·05·06, `집필점검표.md` 02행과 현재 기준 절.
- 챕터 요약: `qa/upgrade/chapter-summary.md`(Ch 04 작업자용).

### 확인 필요 항목 (검토 1차 반영)

- 다운로드 묶음 `textbook/downloads/part1-practice.zip`의 Ch 3은 개선 전 노트북 5개입니다. Part 목차(`textbook/part1/_build_index.py`, `index.html`)도 Ch 3 절 수 5입니다. 둘 다 전체 마감 때 다시 만듭니다.
- 강사 확인: 02절 강의·실습 범위 문장, 기준 Git 버전 표기, 규격에 더한 세 규칙, 교체한 05-5 삽화.
- Windows·macOS 출력, 실제 GitHub PR 화면, Git 2.36 이상에서의 `--sensitive-data-removal`은 이번에 실행하지 않았습니다.

- §2-7 리팩터(2026-09-21): 03~06 노트북 새 커널 두 번 PASS(Git 2.34.1, Python 3.12.13), 리팩터 전과 출력 같음(해시·임시 경로·filter-repo 걸린 시간 제외), `upgrade_gates.py --label after-2-7` 6/6 G1~G7 0, `verify.py --chapter` `PASS 6 sections / 108 code cells (max 18 lines)`, `{{` 0, visual 03~06 × 1280·390 8/8(`qa/upgrade/visual-after-2-7.json`), `part1-practice.zip`(67파일, `git_tools.py` 포함)을 풀어 03·06 PYTHONPATH 없이 PASS. 세부 `qa/upgrade/handoff.md` 「§2-7 확인」.
