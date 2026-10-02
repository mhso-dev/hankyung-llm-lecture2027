# Ch 12 핵심 노트북 경로 연결성 — 수정 전 기록

검토 시점의 학생 파일은 `textbook/qa/continuity-evidence/full-course-before.tar.gz`, `before-manifest.json`, `notebook-before-invariants.json`에 보존되어 있습니다. 기존 QA 판정을 근거로 대신하지 않고 Ch 12 README와 01~06 학생 노트북의 실제 코드 셀을 직접 대조했습니다.

## README 실행 위치 → 01~06 데이터·로그 경로

- **학생 안내:** Ch 12 README는 VS Code에서 `labs/part3/ch12-retrieval-tuning` 폴더를 열고 이 챕터의 `.venv` 커널을 선택하도록 안내합니다. 따라서 노트북의 일반 실행 위치는 `.../ch12-retrieval-tuning/notebooks`입니다.
- **현재 구현:** 01·02·04·05·06 노트북은 `Path("labs/part3/ch12-retrieval-tuning/data")`에서 데이터를 읽습니다. 01~06 모두 결과를 `Path("labs/part3/ch12-retrieval-tuning/runs")`에 씁니다.
- **재현 결과:** 위 상대 경로는 과정 루트에서 실행할 때만 존재합니다. README의 노트북 폴더에서 실행하면 `notebooks/labs/part3/ch12-retrieval-tuning/...`를 가리켜 01·02·04·05·06은 데이터 파일 읽기에서, 03은 로그 저장에서 실패합니다.
- **영향:** 배포 ZIP만 받은 학생이 안내한 폴더와 커널을 사용해도 01~06을 독립 실행할 수 없습니다. 이전 검증은 과정 루트를 `cwd`로 사용해 이 경로 결함을 가렸습니다.
- **중요도:** 매우 높음. 학생의 대표 실행 경로에서 여섯 노트북이 모두 실패합니다.
- **최소 수정 계획:** 각 노트북이 `Path.cwd()`와 상위 폴더를 차례로 확인해 `labs/part3/ch12-retrieval-tuning/data`가 존재하는 과정 루트를 찾고, `chapter_dir = course_root / "labs/part3/ch12-retrieval-tuning"` 아래의 `data`와 `runs`를 사용하게 합니다. 기존 Ch 12 04절 토큰 단위 설명 셀과 다른 코드·출력 의미는 유지합니다.

## 01~06 실행 결과 로그 보존

- **현재 구현:** 각 노트북은 `runs/core-01-exact.json`부터 `core-06-rrf.json`까지 고정 파일명을 직접 `write_text()`해 이전 정식 결과를 덮어씁니다.
- **수정 전 SHA-256:** `core-01-exact.json` `f8e81361…c758`, `core-02-hnsw.json` `e007a959…175`, `core-03-iterative-scan.json` `4d9be882…e1d1`, `core-04-bm25.json` `e5405673…f00`, `core-05-dense-sparse.json` `ee06e48a…4669`, `core-06-rrf.json` `4e3fa110…11369`입니다. 전체 해시는 검증 기록에 남깁니다.
- **영향:** 경로 수정 후 새 커널 재실행을 하면 수정 전 실행 증거가 작업 폴더에서 사라집니다. 전체 스냅샷에는 남지만 학생이 이후 실행별 결과를 비교할 수 없습니다.
- **중요도:** 높음. 실행 결과의 계보와 재검증 가능성에 영향을 줍니다.
- **최소 수정 계획:** 고정 파일은 최신 결과를 가리키는 정식 포인터로 유지합니다. 갱신 전 기존 바이트를 SHA 접두사의 `runs/core-history/before-*.json`으로 한 번 보존하고, 새 결과는 UTC 실행 ID가 든 `runs/core-history/<run_id>-core-*.json`에 먼저 기록한 뒤 포인터를 갱신합니다. 현재 여섯 원본의 해시 불변, 새 실행별 파일 6개, 포인터와 새 파일의 내용 일치를 검증합니다.

## 검증 계획

1. 코드 수정 전에 여섯 노트북의 모든 코드 셀이 25행 이하인지 확인합니다.
2. Ch 12에서 `uv sync --locked`를 실행합니다.
3. 검증 러너의 환경과 학생 환경을 분리하고, `--kernel-python`에는 Ch 12 `.venv/bin/python` 절대 경로를, `--cwd`에는 README 경로인 노트북 폴더를 지정합니다.
4. 01~06을 각각 새 커널에서 준비 셀부터 실행합니다. 01·02·05·06은 실제 임베딩 API를 사용하고 02·03은 로컬 pgvector의 `ch12_core_*` 테이블만 변경합니다.
5. 새 실행 후 데이터 경로, 출력·검증 해시, 기존·새 로그, 고정 포인터, 본문에 포함될 코드·출력을 대조합니다.
