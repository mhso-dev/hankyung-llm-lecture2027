# Ch31 실행 검증

- 실행일: 2026-09-11
- Python 3.12.13
- 독립 데이터베이스: `kdt-ch31-postgres`, `localhost:55431`, PostgreSQL 17.8, pgvector 0.8.1
- 재시작: `docker start kdt-ch31-postgres`; 준비 확인: `docker exec kdt-ch31-postgres pg_isready -U postgres`
- 제거: 전체 Part 7 묶음 검증이 끝난 뒤 `docker rm -f kdt-ch31-postgres`

## 실제 결과

- 01절: 질문은 `['환불', '배송', '결제']` 순서로 조회됐습니다. 0.15초 대기 세 건은 순차 0.468초, 동시 0.195초였습니다.
- 02절: 별도 트랜잭션 Before는 잔액 400·500과 총액 900을 남겼습니다. 한 트랜잭션 After는 500·500과 총액 1000을 유지했습니다.
- 03절: `upgrade head` 뒤 `ch31_migration.tickets`, `downgrade base` 뒤 NULL, 재적용 뒤 같은 표를 확인했습니다.
- 04절: 풀 크기 1·추가 연결 0·대기 0.2초에서 `TimeoutError`를 재현했습니다. 점유 시간을 줄이고 대기를 1초로 둔 실행은 두 결과가 모두 1이며 체크아웃 연결 0으로 끝났습니다.
- 05절: 코사인 검색 첫 결과는 ‘배송’이었고 3행의 실행 계획은 Seq Scan을 선택했습니다. value 6을 12로 계산한 실행은 체크포인트 3행을 저장했습니다. 논리 덤프를 별도 `ch31_restore` 데이터베이스에 복원해 문서 3행, 체크포인트 3행, HNSW 인덱스 존재를 확인했습니다.

## 자동 검증

- `execute.py`: 다섯 노트북 모두 새 커널 PASS, 코드 셀 27개
- `_build.py`: index와 다섯 절 HTML 생성
- `verify.py --chapter`: 5 sections / 27 code cells, 최대 25줄 PASS
- 서비스 정적 검사와 실행: `ruff check`, `python -m app.service`
- 공개 파일: `qa/public-files.json`에 루트 상대 경로만 기록하고 `.env`, 실패 기록, 개인 절대 경로를 제외했습니다.

## 확인 필요 항목

운영 데이터 규모의 HNSW 재현율·지연, 전체 연결 예산, 정기 복원 훈련과 보존 정책은 이 로컬 실습으로 확인하지 않았습니다. 복원 데이터베이스에서 그래프 스레드를 다시 재개하는 경로도 추가 검증 항목입니다. 본문 한국어 감사는 작성자와 다른 검토자가 완료했으며 accept 판정입니다.
