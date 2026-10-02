# 02-임베딩과-의미-유사도 — 품질 개선 진단과 결과

작성 2026-09-16. 규격: `textbook/QUALITY-UPGRADE.md`. 수정 전 원본: `qa/upgrade/before/`(`_src`, 노트북, 빌드 HTML, `figures/02-concept.*`).
생성기: `qa/upgrade/author_02.py`. 실행: `bash textbook/_notebook/upgrade/run_section.sh textbook/part1/ch05-llm-principles 02`(환경 변수 없이).
수정 전 수치는 01절 작업 때 남긴 챕터 기록 `gates-before.json`의 02절 값입니다.

## 게이트 수치

| 게이트 | 수정 전 | 수정 후 |
|---|---|---|
| G1 | 0 | 0 |
| G2 | 2 | 0 |
| G3 | 1 | 0 |
| G4 | 0 | 0 |
| G5 | 6 | 0 |
| G6 | 29 | 0 |
| G7 | 3 | 0 |
| 코드 셀 | 5 | 13 (준비 1 + 본문 12, 주석 뺀 코드 최대 11줄 = 3절 토큰 수 셀) |
| 검사한 문장 | 102 | 322 (`gates-wip-02.json`) |
| 모델 실행 | `encode()` 2번 | `encode()` 5번(내 컴퓨터의 임베딩 모델, API 호출 0, 비용 0) |

## 실행 환경

- 01절 재실행과 같은 전체 가상환경 `$ROOT/.cache/vm/venv-ch05-llm-principles`(torch 2.8.0+cpu, transformers 4.56.2, tokenizers 0.22.2, sentence-transformers 5.1.1, numpy 2.3.3, huggingface-hub 0.36.2, Python 3.12.13, Linux aarch64)와 모델 캐시 `$ROOT/.cache/vm/hf`(`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`@`e8f8c211226b894fcb81acc59f3b34ba3efd5f42`, blobs 합계 499,561,295바이트). `run_section.sh`가 자동으로 씀.
- 새 커널 실행 PASS(`PASS 02-임베딩과-의미-유사도.ipynb: 13 cells`, 한 번 약 7초). 같은 코드로 네 번 실행해 출력 글자가 모두 같았습니다. `outputs_sha256`은 `5ce4a77d…`와 `b29b686a…`가 번갈아 나왔는데, 마지막 셀(또는 9절 셀)의 stdout이 스트림 조각 한 개/두 개로 나뉜 차이뿐입니다(글자 동일).
- `verify.py --chapter` `PASS 8 sections / 52 code cells (max 25 lines)`(25줄은 개선 전 다른 절). `visual.cjs` 이 절 HTML 1280·390px PASS(`/tmp/ch05-02/vis`에서 01절 작업자의 경로만 바꾼 사본으로 실행, 공용 도구는 고치지 않음).
- 준비 셀의 `warnings.filterwarnings("ignore", message="IProgress not found")`: 넣지 않고 실행하니 `from sentence_transformers import …` 줄에서 `TqdmWarning: IProgress not found`가 stderr에 나와(사용자 폴더 경로 포함) 01절과 같은 한 줄을 두었습니다.

## 수정 전 주요 문제

- Ch 1~4·01절에서 가르치지 않은 NumPy를 전제: `import numpy as np`, `np.array`, `np.linalg.norm(toy, axis=1, keepdims=True)`, `ravel()`, 행렬곱 `@`(A 트랙 금지 목록의 `@` 줄과 같은 기호)·전치 `.T`, `np.argsort(-scores[0])[1:]`, `tolist()`, `np.round`, `np.allclose`·`np.isfinite`·`np.diag`. 본문이 이것을 한 단락에 몰아 설명(5문장 넘는 단락 3)
- f-string 형식 지정 `f"0 vs {i}: {scores[0, i]:.4f} | …"`, `print(f"\n…")`, 두 겹 호출 `round(float(vectors[0] @ changed), 4)`(G2 2건), `model.encode([...])[0]`, 검증 셀 `assert A and B`와 첫 줄 주석 없음(G3), 틀 주석 「위 설명의 조건을 실행하고 실제 출력을 확인합니다」 4곳
- 제목 셀·핵심 그림·준비물·결과 읽기 없음(G5 6건). 설명 셀이 `shape`·`axis`·`keepdims` 등 코드 이름+조사로 문장 시작(G6 english_start 18건)
- 옛 도식 캡션이 그림에 없는 「보라색은 모델의 처리, 빨간색은 확인할 제한」을 설명(01절 옛 도식과 같은 문제). Mermaid 0, 삽화 0, 설계표 없음(G7 3건)
- 「앞에서 배운 내용」이 「앞 절에서 토큰 ID의 열로 바뀌는 과정」 한 문장뿐이라 개선된 01절(토큰화기 두 개, 모델은 실행하지 않음)·Ch 2 함수·Ch 4 `shape`와 잇지 않음. 복습 3문항에 난이도 표시 없음
- 해석 문장 「네 문장 한 번의 결과」는 맞았으나, 반품 한 문장만 바꿔 보기로 「유사도는 정답이 아니다」를 말해 근거가 약함

## 바꾼 것

- 노트북(experiment 유지, 학습 질문 「단어가 달라도 뜻이 비슷한 문장을 숫자로 비교할 수 있을까요?」와 데이터 유지 — 같은 모델·revision, 문장 네 개, 반품 문장): 제목(할 일 3, `encode()` 5번·비용 0·1분 안팎, 모델 파일 약 500MB, 기준 버전 sentence-transformers 5.1.1·transformers 4.56.2·torch 2.8.0·numpy 2.3.3·revision) → 오늘 볼 그림(02-1) → 1 준비(`math`·`warnings`·`sentence_transformers.__version__`) → 2 모델 준비(`SentenceTransformer(이름, revision=)`, `get_sentence_embedding_dimension()` 384, `max_seq_length` 128) → 3 `model.tokenizer.tokenize()` 토큰 8·8·9·7, `▁` 표시 → 4 `encode()` → `(4, 384)`, `assert vectors.shape == (4, 384)` → 5 `dot_product()` 정의·호출(`점곱: 24`) → 6 `vector_length()`(`math.sqrt`)·`cosine_similarity()` 정의, 호출(5.0·0.96·1.0·`[4, -3]` 0.0) → 7 문장 벡터 0.8024·0.1044·0.8987 → 8 `normalize_embeddings=True` 길이 3.9723 → 1.0, 점곱 0.8987 → 9 값 바꿔 보기(반품 0.5931, **부정문 0.6716 추가**) → 10 01절 문장 쌍 0.8312·Ch 4 기사 요약 쌍 0.9517 → 정리
- NumPy는 import하지 않고, 모델이 반환한 배열의 `shape`·행 고르기 `vectors[0]`·슬라이싱 `[0:5]`·`len()`만 씀(Ch 4 01 데이터프레임 `shape`에 연결). `@`·`.T`는 기본 경로에서 없앰. 유사도는 Ch 2 04 함수 정의(셀 하나에 함수 하나, 정의·호출 셀 분리, 타입힌트 없음)와 `for`+`range()`로 직접 계산
- 본문 10블록 전체를 다시 씀: 이 절의 질문 두 개(비교할 수 있나 / 높으면 같은 뜻인가), 비유(연필 원판 — 방향 = 뜻, 벌어진 각 = 뜻의 차이, 길이는 비교에 안 씀), 용어 7개 표, 평균 풀링(설정 파일로만 확인, 토큰별 목록은 출력 안 함), 수식은 말 → 식 → 숫자(24 ÷ (5 × 5) = 0.96), 실험 해석(영어 문장 최고, 부정문 > 반품, 두 쌍, 결론 두 가지와 범위), 주의 메모 7개(기준값, Ch 11 평가 연결, 128토큰 자르기, `model.similarity()` 미실행, 캐시·오프라인 미실행, revision, 기준 버전), 복습 5문항(기초 2·적용 1·분석 2)
- 라이브러리 동작 확인(설치본·내려받은 설정): `SentenceTransformer.encode(…, convert_to_numpy=True, normalize_embeddings=False)` 기본값, 정규화는 `torch.nn.functional.normalize(p=2, dim=1)`(1126행), `1_Pooling/config.json` `pooling_mode_mean_tokens: true`, `sentence_bert_config.json` `max_seq_length: 128`, `models/Transformer.py` `truncation="longest_first"`·`max_length=self.max_seq_length`, transformers `truncation_side` 기본 `"right"`(앞부분을 남김), `similarity()` 메서드 존재(1208행, 실행 안 함)
- 뒤 챕터 연결: Ch 9 03 b3 「Ch 5 임베딩과 의미 유사도 — 문장 두 개를 벡터로 바꿔 코사인 유사도를 직접 계산했습니다」와 맞음(이 절은 직접 만든 함수로 계산). Ch 11 제목 「평가 기초 — 측정 가능한 검색 품질」은 `chapter.json`에서 확인
- 그림: Mermaid 4장 + 삽화 1장. 옛 `figures/02-concept.*`는 본문에서 뺌(원본 `before/figures/`, 옛 파일은 삭제하지 않음)

## 그림 확인

- PNG 네 장을 직접 열어 확인. 02-1 TB 여섯 상자(초록 문장 → 노랑 토큰 수 → 보라 모델 → 노랑 벡터 표 → 파랑 함수 → 노랑 유사도, viewBox 243). 02-2 TB 두 갈래가 모임(viewBox 353). 02-3 TB: 처음 화살표 라벨 `normalize_embeddings=True`가 `…=T`/`rue`로 잘려 라벨을 「정규화해 다시 encode()」로 바꾸고 인자 이름은 도식 읽기에 적음(viewBox 229). 02-4 xychart-beta 막대 한 계열 노랑(viewBox 700), 한글 범주 이름 따옴표
- 색: 01절에서 회색 점선이던 모델을 이 절에서는 실행하므로 보라, 학생이 정의한 함수는 파랑. 빨강 없음
- 삽화 02-5(연필 원판): 1회차 job `64d86066-26b5-460d-8cc3-61dc0cf254a9` 탈락(연필 네 자루, 넷째 파란 연필이 다른 방향이라 「같은 색 = 같은 방향」이 깨짐, 부채꼴 음영). 프롬프트에 「only three pencils in total」, 방향을 위·오른쪽으로 고정, 「no shaded areas」, 빈 영역을 적어 2회차 job `21f75add-e266-4919-bb4b-24c1b7bc9222` 채택. 합계 4크레딧(생성 전 잔액 2900). 저장 PNG(1100×614)를 기기에서 다시 받아 채택 job 결과를 같은 폭으로 줄인 것과 대조해 픽셀 차이 0, 탈락본과는 다름

## 검토에서 볼 곳

- 9절 값 바꿔 보기에 부정문을 더한 판단과, 결론을 「부정문 한 문장으로 본 것」으로 한정한 범위
- 평균 풀링을 설정 파일로만 확인하고 본문 「문장이 벡터가 되기까지」에 적은 설명 수준, 4절 「숫자 하나에 뜻이 붙어 있지 않다」는 문장(실행으로 보인 것은 앞 다섯 값뿐)
- 삽화가 시계 바늘처럼 보이는지(숫자·눈금 없음), 연필 두 자루가 「거의 같은 쪽」이 아니라 평행으로 나온 점

## 검토 (별도 세션 1차, 2026-09-16) — `qa/upgrade/review-round1-A.md`

- 판정 accept-with-fixes(중 1, 하 2). 모두 반영했습니다.
- 02-1(중): 3절 코드 셀에 `ids = model.tokenizer.encode(sentence)`와 `convert_ids_to_tokens(first_ids)` 출력을 더함(01절 메서드, 새 API 아님). 출력 `조각 8 | ID 10`·`조각 8 | ID 10`·`조각 9 | ID 11`·`조각 7 | ID 9`, `['<s>', '▁주문', …, '.', '</s>']`. 3절 설명·결과 읽기, 4절 예상(「ID 수가 9~11개」)·결과 읽기, b4(조각 8·8·9·7, ID 10·10·11·9, 특수 토큰까지 평균), b5, b7 128 한도(특수 토큰 포함), 복습 1, 그림 02-1 라벨 두 줄·화살표 `tokenize() · encode()`·alt·캡션·설계표. 특수 토큰까지 평균(토큰별 벡터 10개 평균과 `encode()` 차이 0.0, 가운데 8개 평균은 코사인 0.9867)과 128 한도 포함(긴 글 `[1, 128]`)은 마감 세션 기기 셸에서 다시 확인했고 본문에 「기기 셸에서 확인」으로 적음
- 02-2: [13]·b5 「숫자 하나만 보고는 취소인지 날씨인지 읽을 수 없습니다. 벡터 두 개를 비교해야 뜻이 가까운지 알 수 있습니다.」, 03 [7]·b4도 함께 고침
- 02-3: 삽화 그림 읽기 「판이 시계처럼 보여도 시각을 뜻하지 않고, 연필이 가리키는 방향만 봅니다.」
- C-2: 그림 02-4 「주황 막대그래프」「색은 주황 하나」. C-5: `02-5-연필-원판.prompt.md` 기록 고침, 실습 폴더 README MiniLM 캐시 「약 480 MiB」. 참고 자료 MiniLM 확인일 2026-09-16(같은 링크 다시 열어 200 확인, B 09-3과 같은 처리)
- 재실행: `author_02.py` 수정 → `run_section.sh … 02` 새 커널 두 번 PASS. 3절 셀만 출력이 바뀌고 나머지 12개 셀 출력 글자는 반영 전과 같음. `outputs_sha256` 반영 전 `5ce4a77d…` → `e1676185…`·`f43ffa90…`(두 실행 출력 글자는 같고 36번 셀 stdout 조각 수만 다름, 02 첫 작업 때 기록한 현상). 코드 셀 13, 검사한 문장 334

공통 검사(2026-09-16 마감 세션): 챕터 `upgrade_gates.py --label after --strict` 9/9 PASS(G1~G7 0, `gates-after.json`, 수정 전 262건), `verify.py --chapter` `PASS 9 sections / 132 code cells (max 17 lines)`, `visual.cjs` 9절+목차 × 1280·390px 20건 PASS, `pack.py`로 review-pack 9개 갱신(반영 전 묶음은 `before/review-round1-pack/`). 치환은 `mdpatch.py`와 같은 방식(생성기·노트북 설명 셀·`_src` 동시)으로 하고, 그림 파일(`.mmd`·`.caption.md`·설계표)을 함께 고친 뒤 `run_section.sh … NN --no-exec`.

## 남은 것

- 리뷰 묶음: `qa/upgrade/review-pack/02-임베딩과-의미-유사도.md`
- 정리 대상(삭제하지 않고 목록만): `figures/02-concept.excalidraw`·`.svg`(옛 도식), `/tmp/ch05-02`(탐색 스크립트·01 노트북 사본·visual 사본)
- 챕터 안 옛 생성기 `make_sources.py`와 `labs/part1/ch05-llm-principles/make_notebooks.py`는 실행하지 않았습니다(개선본을 덮어씀)
  - 2026-09-16 챕터 마감에서 처리: 두 파일 첫머리(docstring·`from __future__` 뒤)에 설명 주석과 `raise SystemExit(...)`를 넣고 `mv -n`으로 `qa/upgrade/before/generators/`(`make_sources.py`·`make_notebooks.py`)로 옮김. 삭제하지 않음
- 실습 폴더 `README.md`의 「multilingual MiniLM 캐시는 458 MiB」는 이번 기기에서 blobs 합계 약 476MiB(499,561,295바이트)로 달랐으나 고치지 않음(파일 시스템 차이로 보임, 노트북·본문은 「약 500MB」)


## §2-7 리팩터 (2026-09-21)

8절 「같은 계산을 NumPy로」(코드 셀 2개)를 더하고 9절 정규화를 NumPy로 바꿈. 절 번호 8~10 → 9~11. 반올림 전 유사도가 반복문 `0.8987315`·NumPy `0.8987313`으로 달라 결과 읽기·b7에 반올림 비교를 적음. 코드 셀 13 → 15, 코드 줄 79 → 90. 새 커널 두 번 출력 같음.
