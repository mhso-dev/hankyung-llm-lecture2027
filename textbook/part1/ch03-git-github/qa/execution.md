# Ch 3 실행·화면 검증

확인일: 2026-09-09.

## 새 커널 실행

```text
uv run --project labs/part1/ch03-git-github --with nbclient==0.11.0 --with ipykernel==7.3.0 --with pip --with python-dotenv==1.2.3 python textbook/_notebook/execute.py labs/part1/ch03-git-github/notebooks/*.ipynb --cwd .
```

결과: 5개 노트북 모두 PASS, 각 6개 코드 셀, Python 3.12.13, 오류 허용 비활성화. 대표 관찰값은 집필 점검표에 기록했습니다.

## 빌드와 계약 검사

```text
uv run --project labs/part1/ch03-git-github --with pillow python textbook/part1/ch03-git-github/_build.py
uv run --project labs/part1/ch03-git-github python textbook/_notebook/verify.py --chapter textbook/part1/ch03-git-github
```

결과: `PASS 5 sections / 30 code cells (max 22 lines)`. HTML의 입력 코드, 실제 출력, 내장 다운로드 노트북이 정본 노트북과 일치했습니다.

## 화면 4축과 상호작용

```text
NODE_PATH=/Users/mhso/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules node textbook/_notebook/visual.cjs textbook/part1/ch03-git-github
```

결과: 1280px와 390px에서 절 5개와 index를 검사해 12/12 PASS. 작은 글자, 대비 오류, 잘림, 본문 밖 텍스트, SVG 경계 오류, 수평 페이지 넘침, 깨진 이미지, 복사 오류, Before/After 배치 오류가 모두 0건입니다.

확인 필요 항목: Windows/Linux 브라우저는 실측하지 않았습니다. Excalidraw 연결 도구가 호출 목록에 없어 도구 미리보기는 수행하지 못했고, 같은 생성기의 SVG·Excalidraw JSON 구문과 브라우저 SVG 경계를 검사했습니다.

## 최종 재검증

2026-09-09: Git 전역 기본 브랜치를 `master`로 정한 별도 설정과 임시 작업 폴더에서 5개 노트북·30셀을 새 커널로 실행했습니다. 03절의 해결 문장에 정책의 14시 이전·이후 조건을 명시한 뒤 해당 6셀을 다시 실행했습니다. 최종 빌드·코드·출력·다운로드 대조는 5/5, 화면·복사 검사는 1280px와 390px에서 12/12 통과했습니다. 독립 언어 감사 Phase 6 판정은 `accept`입니다. 근거는 `textbook/part1/qa/language/ch03-audit.md`와 공통 화면 검사 결과에 있습니다.
