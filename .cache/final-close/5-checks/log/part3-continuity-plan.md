# Part 3 run_continuity_bundle.py 실행 전 기록 (2026-10-01)
- 실행: `textbook/part3/qa/run_continuity_bundle.py` (`--reuse-upstream` 없이), 묶음 `part3-practice.zip` c6dea7c1… 사본에서만 실행(저장 노트북 다시 쓰지 않음).
- 실행하는 노트북: Ch 9 `06-실험-하네스` → Ch 10 `08-인덱싱-비교-실험` → Ch 11 `06-실험-로그와-자동-실행`.
- 예상 요청(셀 머리 주석·코드 기준): Ch 9 06 임베딩 7 + gpt-5.4-mini 1(입력 약 500·출력 약 150 토큰) · Ch 10 08 임베딩 13(설정 6 × 색인·검색 + 1) · Ch 11 06 임베딩 16(색인 1 + 개발 15문항 검색 15, evaluate.py는 요청 없음) → 합 37(임베딩 36·채팅 1).
- 요금 어림: 임베딩 text-embedding-3-small $0.02/1M — 색인 글 합 약 1M 토큰 이하(Ch 9 문서 청크 176×500자 + 107×1000자, Ch 10 1,372×400 이하, Ch 11 90쪽) → 약 $0.02 · 채팅 gpt-5.4-mini(과정 요금표 Ch 34: 입력 $0.75·출력 $4.50 /1M) → 약 $0.001. 합 약 $0.03, 넉넉히 잡아도 $0.1 미만(1달러 기준 아래).
- 환경: 3단계 명령의 `UV_CACHE_DIR=$ROOT/.cache/vm/bundle-check/uv-cache`는 연결 폴더라 `--with ipykernel` 임시 환경 설치가 `.data` 폴더를 못 지워 실패(시험: ipython-9.17.1 설치 Operation not permitted) → `UV_CACHE_DIR=/tmp/uv-cache`(Part 7과 같은 캐시, 내려받을 것 약 37MB). 풀어 둘 곳은 기기 `$TMPDIR/fc5-part3`(연결 폴더 안에서는 uv 설치·SQLite가 삭제 금지로 실패).
- 감싸개 `tools/keep_run.py`: 스크립트를 고치지 않고 돌리되 임시 폴더를 지우지 않고, 풀어 둔 묶음의 `.env` 자리표시 파일(주석 한 줄, 키 없음) unlink를 건너뜀.
