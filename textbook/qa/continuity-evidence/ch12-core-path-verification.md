> 후속 전체 검증: 최종 ZIP 현재 파일 대조·압축 해제본 실행은 `bundle-execution-results.json`, 최종 화면은 `global-visual-results.json`에서 확인합니다. 아래는 담당 구간 실행 당시의 기록입니다.

# Ch 12 핵심 노트북 경로 수정·검증

## 수정 결과

- 01~06 노트북은 `Path.cwd()`와 상위 폴더를 차례로 확인해 `labs/part3/ch12-retrieval-tuning/data`가 존재하는 과정 루트를 찾습니다.
- 찾은 과정 루트에서 `chapter_dir`, `data_dir`, `runs`를 구성하므로 과정 루트와 README가 안내하는 `.../ch12-retrieval-tuning/notebooks` 양쪽 실행 위치에서 같은 자료와 로그를 사용합니다.
- 여섯 노트북의 고정 결과 파일은 최신 결과를 가리키는 포인터로 유지합니다. 갱신 전 바이트는 `runs/core-history/before-<SHA 접두사>-<파일명>`에 한 번 보존하고, 새 결과는 `runs/core-history/<UTC 실행 ID>-<파일명>`에 먼저 저장한 뒤 포인터를 갱신합니다.
- 활성 노트북 생성기는 없어서 동기화할 별도 생성 원본은 없습니다.
- 다른 작성자가 추가한 04절의 “Kiwi 검색 토큰과 Ch 5·Ch 10 토큰을 직접 비교하지 않는다”는 Markdown 설명은 그대로 보존했습니다. 07~12 노트북, README, `pyproject.toml`, `uv.lock`, 배포 목록은 수정하지 않았습니다.

## 학생 경로 새 커널 실행

- Ch 12 폴더에서 `uv sync --locked`를 실행해 잠금 환경을 동기화했습니다. 학생 커널에는 Python 3.12, `ipykernel==7.3.0`, `pip==26.2`, `psycopg==3.3.5`, `pgvector==0.4.2`, `langchain-openai==1.6.1`이 설치돼 있습니다.
- 검증 러너의 임시 환경과 학생 환경을 분리했습니다. `--kernel-python`에는 `/Users/mhso/working/claude/projects/한국경제신문/labs/part3/ch12-retrieval-tuning/.venv/bin/python`을, `--cwd`에는 README 실행 위치인 `labs/part3/ch12-retrieval-tuning/notebooks`를 지정했습니다.
- 01·02·05·06의 실제 임베딩 API를 다시 호출했습니다. 02·03은 로컬 `hankyung-part3-pgvector` 컨테이너에서 실행했고 변경된 표는 `ch12_core_hnsw`, `ch12_core_dim_vector`, `ch12_core_dim_halfvec`, `ch12_core_filter`뿐입니다. 검증 뒤 컨테이너를 중지했습니다.
- 실행 결과:
  - 01: `PASS`, 코드 셀 7개, 코드 해시 `dceed2c3eafaa049319d5d704e8a0b1b1a34723399f4848cd13ff4f7302d658a`, 출력 해시 `7e9097a96b342a588ed8abdfe0cac9b88e506942aad109586168bf31027d0dd2`.
  - 02: `PASS`, 코드 셀 8개, 코드 해시 `6cd1d4242a5486a2744f788b4fea4d9a8eb37b0c0225e73db4502ad2b2bb0865`, 출력 해시 `054ae267081661d788b0e2a74c3178a5e74f7e7e254f362cc063823d6e35ac14`.
  - 03: `PASS`, 코드 셀 7개, 코드 해시 `a16b8f36d5daf300dc958bbf062fbc8a09aa7c5533616ef6156b3ea520799fc3`, 출력 해시 `76902abde80d0536a2f19199c54a78f94353067e4ddc5ebd3b535256d803294a`.
  - 04: `PASS`, 코드 셀 7개, 코드 해시 `c074ccdb4cc2aef991100b420c9dcc361bf26528e942cc3889d33dd7838ecbad`, 출력 해시 `7ac56ce603e03843e082e49fd6d86048d6f0c08661442210a931fa5e99f2a14d`.
  - 05: `PASS`, 코드 셀 9개, 코드 해시 `250cf592a37cbda1a4b030ece733a0ef9a93ce05f32f11e7d300f5d4fba9004f`, 출력 해시 `8fad7a087db28e8e100a244622c894047e7676735625bdeca5c5d4867b97a590`.
  - 06: `PASS`, 코드 셀 9개, 코드 해시 `8b2d0013c767b59690ea80123572554f2c0891f1c55be367530e33e5e751379e`, 출력 해시 `f2a4032d4043e66146c4a1845e736feccb2bad62cf6ee170dbc0d8732e335d65`.
- 모든 실행 메타데이터는 Python 3.12.13, `fresh_kernel=true`, `allow_errors=false`, `status=passed`입니다. 저장된 코드·출력에서 다시 계산한 해시도 메타데이터와 일치합니다.
- 수정 후 가장 긴 코드 셀은 20행입니다. 여섯 노트북 코드에는 `Path("labs/part3/ch12-retrieval-tuning/...")` 형태의 고정 상대 경로가 남아 있지 않습니다.

## 결과와 본문 수치 대조

- 01: 코사인과 L2 모두 8개 질문 중 7개 정답을 top-3에 포함했습니다.
- 02: `vector(2001)` HNSW는 2,000차원 제한 오류, `halfvec(2001)` HNSW는 생성 성공을 반환했습니다.
- 03: iterative scan 전 0개, `strict_order` 적용 뒤 5개를 반환했습니다.
- 04: Kiwi+BM25는 8개 질문 중 8개 정답을 top-3에 포함했습니다.
- 05: dense 7/8, sparse 8/8입니다.
- 06: dense 7/8, sparse 8/8, 동일 가중치 RRF 7/8입니다.
- 여섯 최신 포인터의 JSON은 수정 전 포인터와 각각 바이트 단위로 같아 본문의 결과 수치를 바꿀 필요가 없습니다. `_src`에는 고정 과정 루트 경로도 없으므로 본문 파일은 수정하지 않았습니다. 새 노트북 코드와 출력은 상위 Ch 12 빌드에서 삽입합니다.

## 로그 보존 검증

- 수정 전 여섯 포인터를 해시 접두사의 `before-*` 파일로 보존했고 모두 원본과 바이트 단위로 같습니다.
- 실행별 새 파일:
  - `20260909T174506809610-core-01-exact.json`
  - `20260909T174508887627-core-02-hnsw.json`
  - `20260909T174510227986-core-03-iterative-scan.json`
  - `20260909T174512049970-core-04-bm25.json`
  - `20260909T174515609696-core-05-dense-sparse.json`
  - `20260909T174519370916-core-06-rrf.json`
- 각 고정 포인터는 대응하는 새 실행별 파일과 바이트 단위로 같습니다. 고정 포인터의 내용이 재현되어 SHA-256도 수정 전과 같습니다: 01 `f8e81361e9c79fa5aa4203cb933cd0a084efe63fd804eae570dbc6896b64c758`, 02 `e007a959899ec0ea866ca7d03597fec13bbd3c84bf677c9048251658f1519175`, 03 `4d9be88254b631d348b3572c8216ad57b6c2bd8166f7f58a46ac596f83e9e1d1`, 04 `e5405673f7efcd5188ad1586ac18fdcb68fcc10fb6e6999097692a4b62d97f00`, 05 `ee06e48ac32d706c9078b4dd2d4ef4937e8198f7a132cca3a523ce490f3e4669`, 06 `4e3fa11084a4a09e5839c43c82786269f5a0a4e0b0aab0df490f0b044c511369`.

## 현재 상태

README가 안내하는 노트북 폴더에서 Ch 12 01~06을 각 챕터 잠금 환경의 새 커널로 독립 실행할 수 있습니다. 데이터 읽기, 실제 API, pgvector 전용 표, 실행별 로그 보존, 최신 포인터 갱신을 모두 같은 경로에서 확인했습니다. 최종 HTML·ZIP 반영과 압축 해제본 재실행은 상위 전체 연결성 검증에서 수행합니다.
