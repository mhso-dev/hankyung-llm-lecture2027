> 후속 전체 검증: 최종 ZIP 현재 파일 대조·압축 해제본 실행은 `bundle-execution-results.json`, 최종 화면은 `global-visual-results.json`에서 확인합니다. 아래는 담당 구간 실행 당시의 기록입니다.

# Ch6→Ch7→Ch8 연결성 수정 후 검증

검증일은 2026-09-10(Asia/Seoul)입니다. 수정 전 증거는 `full-course-before.tar.gz`와 `ch06-08-review.md`에 보존했습니다.

## 수정한 연결

| 연결 | 수정 내용 | 최종 산출물 |
|---|---|---|
| Ch5→Ch6 | Ch5의 선택표는 사람이 API 호출 전에 모델 후보를 고르는 기준이고 Ch6 코드가 후보를 자동 선택하지 않는다고 01절에 명시했습니다. Ch2 A트랙의 클래스 문법과 이 절에서 처음 배우는 Pydantic의 경계도 03절 본문·노트북에 추가했습니다. | `textbook/part2/ch06-langchain-start/_src/01-*`, `_src/03-*`, Ch6 03 노트북 |
| Ch6 비용·캐시 | `input_token_details.cache_read`를 전체 입력에서 분리해 일반 입력·캐시 입력·출력 단가를 적용하는 `estimate_cost()`를 구현했습니다. 가격 기준일·단가 정책과 제공자별 원자료를 정본 및 마이크로초 UTC 실행 사본에 저장합니다. | `labs/part2/ch06-langchain-start/runs/provider-comparison-continuity.json` |
| Ch6→Ch7 | Ch7 08이 Ch6 정본을 직접 읽고 필수 필드, `run_id`, SHA-256 지문, 가격 정책을 확인합니다. 고객 문의는 별도이므로 수치를 직접 비교하지 않고 같은 측정 형식만 사용합니다. | `labs/part2/ch07-prompt-engineering/runs/prompt-ab-continuity.json` |
| Ch7 A/B 기록 | 프롬프트 원문·변경 이유·응답 원문·입출력/캐시 토큰·지연·예상 비용·가격 정책을 저장합니다. `mention_count`는 정독 보조이고 생성 답변 품질은 `human_review_required`로 남깁니다. 기존 `prompt-ab-v1.json`은 수정하지 않았습니다. | Ch7 08 노트북·본문·README·생성기 |
| Ch7→Ch8 | Ch8 06이 Ch7 정본을 직접 읽고 `run_id`와 SHA-256 지문, 가격 정책을 상속합니다. 서로 다른 질문의 수치를 직접 비교하지 않는 한계도 본문과 노트북에 명시했습니다. | `labs/part2/ch08-context-engineering/runs/context-design-continuity.json` |
| Ch8 원문→Ch9 | `E01-p5`의 “90분 무료”를 실제 PDF·`memory.json`과 같은 “회원 최초 2시간 무료”로 고쳤습니다. `E01-p3`이 Ch9의 `doc_id=E01, page=3`과 같은 위치이며 질문에 따라 2쪽을 선택할 수 있다고 설명했습니다. | Ch8 02·06 노트북, 생성기, 본문 |
| Ch8 Compress | E01 2쪽에 없던 “임시 휴관”과 3쪽에 없던 “성인 회원”을 실제 원문의 공휴일 예외와 회원 한 사람 범위로 교체했습니다. | Ch8 03 노트북·생성기 |
| 학생 작업 폴더 | Ch6~8 로그 코드는 현재 폴더와 상위 폴더에서 과정 루트를 찾은 뒤 모든 입력·출력 경로를 결합합니다. 최종 실행은 저장소 루트가 아니라 각 `notebooks/` 폴더를 작업 폴더로 지정했습니다. | Ch6 06, Ch7 08, Ch8 06 노트북·생성기 |
| Ch7→Ch11·Ch15 | Ch11이 검색된 문서 순위를 평가하고 생성 답변의 정확성·근거성은 Ch15가 평가한다고 Ch7 08과 Ch8 06의 다음 학습 연결에 명시했습니다. | Ch7 08·Ch8 06 본문 |

## 실행 증거

세 챕터에서 `uv sync --locked`를 실행한 뒤 각 `.venv`의 Python 3.12.13, ipykernel 7.3.0, pip 26.2를 확인했습니다. 실행기는 외부 프로세스에서 사용했고, 실제 커널은 각 챕터의 `.venv/bin/python`으로 고정했습니다.

최종 학생 작업 폴더 실행은 다음 순서로 통과했습니다.

```text
PASS 06-토큰-비용-지연-비교.ipynb: 9 cells
PASS 08-프롬프트-버전과-AB-비교.ipynb: 9 cells
PASS 06-단계적-공개와-설계-비교.ipynb: 18 cells
```

각 실행의 `--cwd`는 해당 챕터의 `notebooks/` 폴더였습니다. Ch8 02는 E01-p5 수정 뒤 15개 코드 셀, Ch8 03은 출처 근거 수정 뒤 13개 코드 셀을 새 커널에서 통과했습니다. Ch6 03은 마크다운만 수정했으므로 API를 다시 호출하지 않았습니다. 수정 전과 후의 코드·출력 해시가 같고 기존 검증 메타데이터도 그대로 유지됨을 확인했습니다.

최종 정본의 실행 계보는 다음과 같습니다.

```text
ch06-provider-20260909T173655923454Z
  SHA-256 531b30d0c1a07e49a653a651f9a082b3716bca142fed6e081dc15482b5f6b10a
→ ch07-prompt-ab-20260909T174009751770Z
  SHA-256 e124b791d070bc023c70176bedeb3cdb3e73924c16b4e991be718f37f26bc02b
→ ch08-context-20260909T174025306280Z
  SHA-256 88b3520bb65415b39acf7f805a9769ed01918ef57f63c307474ab9f5c5ba77aa
```

Ch7의 `source_record`는 Ch6의 ID와 지문을, Ch8의 `source_record`는 Ch7의 ID와 지문을 보존합니다. 각 단계의 `runs/continuity/<마이크로초 UTC>/` 사본도 남아 있으며 `exist_ok=False`로 같은 이름의 덮어쓰기를 거부합니다.

비용·경로·원문·로그 계보 회귀는 다음 명령으로 검증했습니다.

```bash
uv run --project labs/part2/ch08-context-engineering --with pytest \
  pytest -q labs/part2/ch08-context-engineering/tests/test_ch06_ch08_continuity.py
```

결과는 `5 passed in 0.01s`입니다. 여러 캐시 입력이 포함된 합성 사용량으로 세 챕터의 비용 함수가 0.000093달러를 계산하는지, Ch8의 금지된 근거 문구가 제거됐는지, 학생 작업 폴더에서 과정 루트를 찾는지, 레거시 로그 해시가 유지되는지, 세 정본의 `run_id`·지문·가격 정책이 이어지는지 검사했습니다. 전체 출력은 `ch06-08-tests.txt`에 저장했습니다.

## 본문·노트북·생성기·HTML 검증

수정한 여섯 노트북의 셀 원문이 각 `_make_notebooks.py`가 생성하는 원문과 일치함을 별도 임시 폴더에서 확인했습니다. 세 챕터를 다시 빌드한 뒤 검증 결과는 다음과 같습니다.

```text
PASS 6 sections / 48 code cells (max 22 lines)
PASS 8 sections / 58 code cells (max 23 lines)
PASS 6 sections / 80 code cells (max 25 lines)
```

전체 빌드·검증 출력은 `ch06-08-build-verify.txt`에 저장했습니다. 도식에는 수정 대상인 90분·임시 휴관·성인 회원 문구가 없어 SVG·편집 원본 변경은 필요하지 않았습니다.

레거시 로그의 SHA-256은 수정 전과 같습니다.

- Ch7 `prompt-ab-v1.json`: `16a4b672...f4341`
- Ch8 `ex01_budget.jsonl`: `e3b6a71d...2f70f`
- Ch8 `ex04_failures.jsonl`: `d23dbb45...3394`
- Ch8 `ex05_rot.jsonl`: `6a9db927...db00`
- Ch8 `ex06_compare.jsonl`: `5cb060d6...c5c0c`

## 남은 제한

Anthropic과 Google API 키가 없어 Ch6의 두 제공자 행은 `skipped`입니다. OpenAI 경로와 로그 전달은 실제 API로 검증했지만, 두 제공자의 사용량·캐시 세부 필드와 비용은 확인하지 못했습니다. 이 제한은 Ch6 본문의 확인 필요 항목에 유지했습니다.

배포 ZIP 구성·압축 해제본 실행과 PC·모바일 화면 검사는 전체 배포 담당 단계에서 새 정본 세 파일을 포함해 수행해야 합니다. 이 문서는 해당 작업을 완료로 표시하지 않습니다.

최종 정적 대조에서도 Ch6→Ch7→Ch8의 파일 지문과 `run_id`, 가격 정책이 일치했고, 빌드 HTML에서 폐기한 “90분 무료”·“임시 휴관은 별도 공지”·“성인 회원 1명 기준”이 사라지고 “회원은 최초 2시간 무료입니다.”가 표시됨을 확인했습니다.
