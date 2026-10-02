# Ch 17 한국어 최종 감사 보고서

## 판정

- 장르: 산문
- 최소 심각도: S1
- 최종 검수: `corrected`
- 의미 보존 15항: 통과
- 과윤문: 없음
- 전달 판정: 수락

다섯 절의 본문, 챕터 메타데이터, 실습 안내, 노트북 마크다운, 도식 캡션을 전문 정독했습니다. 절마다 같았던 실행 안내와 확인 문장을 실제 실험 항목에 맞게 고쳤고, 도식 캡션도 각 도식이 설명하는 판단 절차로 바꿨습니다. Ch 17의 기술적 경계, 공개 궤적의 증거 수준, Ch 18·Ch 20 연결 관계는 그대로 보존했습니다.

원본 동결본은 `textbook/part5/qa/language/ch17-original/`에 보관했습니다. 원본 전체 해시는 `ch17-original/SHA256SUMS`, 노트북 코드·출력 기준선은 `ch17-original/NOTEBOOK_PROTECTED_SHA256.json`에 있습니다.

## 한국어 감사 3단

1. `moai-coworker:ai-slop-reviewer`: 다섯 절과 보조 문서를 처음부터 끝까지 읽고, 반복 안내문·범용 캡션·압축 명사구·구어 축약을 국소 교정했습니다.
2. `moai-writer:korean-spell-check`: 외부 전송을 실행하지 않았습니다. 스킬의 `SKILL.md` 29행은 “대량 배치, SaaS 백엔드 연동, 상업 서비스 내 무단 재판매·재노출에는 사용하지 않습니다”라고 규정하고, 35행도 “상업적 대량 처리”를 사용 금지로 지정합니다. 이 교재는 상업 교육용 다문서 묶음이므로 `nara-speller.co.kr` 전송을 생략했습니다.
3. `moai-writer:korean-humanize`: 절별로 입력을 나누어 산문·S1 조건으로 메트릭과 구조 게이트를 실행한 뒤 Phase 6 원문 대조를 완료했습니다. 게이트 증거는 `textbook/part5/qa/language/ch17-gates/`에 보관했습니다.

선택 항목인 `mcp__moai__codex_*` 적대적 감사 도구는 이 런타임에 노출되지 않아 실행하지 않았습니다. 프로젝트 지침에 따른 다른 모델의 최종 의미 검토는 상위 통합 검토에서 별도로 진행합니다.

## 게이트 결과

| 범위 | run_id | P0 문자 변경률 | 구조 게이트 | P3 불변식 | Phase 6 |
|---|---:|---:|---|---|---|
| 01절 | 2026-09-10-012 | 6.7% | INCONCLUSIVE | PASS | accept |
| 02절 | 2026-09-10-007 | 3.5% | WARN | PASS | accept |
| 03절 | 2026-09-10-008 | 5.8% | INCONCLUSIVE | PASS | accept |
| 04절 | 2026-09-10-009 | 4.2% | WARN | PASS | corrected |
| 05절 | 2026-09-10-010 | 4.0% | WARN | PASS | accept |
| 메타·README·노트북 마크다운·캡션 | 2026-09-10-011 | 10.2% | PASS | PASS | accept |

02·04·05절의 WARN은 필요한 문장만 고쳐 변경률이 5%보다 낮다는 알림입니다. 01·03절의 INCONCLUSIVE와 01~05절의 리듬 REPORT는 학습 목표·고정 소제목·복습 문제처럼 짧은 교육 구조까지 문장으로 센 결과입니다. Phase 6에서 각 절을 연속된 산문으로 다시 읽어 문장 호흡과 문단 역할을 확인했습니다. 04절은 쉼표 뒤 수치를 게이트가 누락으로 읽은 첫 교정안을 되돌리고 수치를 원래 위치에 보존한 뒤 P3 PASS를 다시 확인했습니다.

## 주요 변경

- 다섯 절에 반복되던 범용 실행 안내를 각 노트북의 실제 데이터와 관찰 항목으로 교체했습니다.
- 워크플로우와 에이전트의 경계를 결정 주체로 설명하는 핵심 대조를 유지하면서 조사 생략과 압축 표현을 풀었습니다.
- 01 도식의 보라색 상자가 모든 결정을 모델이 내린다는 뜻으로 읽히지 않도록 설명 범위를 명확히 했습니다.
- 03 도식은 반복 경로가 아니라 모델·도구 결과·상태 갱신·정지 조건을 나열한 구성 요소 개요임을 명시했습니다.
- 공개 궤적과 공식 제품 설명을 구분하는 문장을 다듬고, `--max-turns` 같은 코드 문자열은 그대로 보존했습니다.
- 노트북 마크다운의 “중단 이유”, “계기판 계산”, “둘째 궤적”을 각각 “정지 이유”, “단계·비용·지연 계산”, “두 번째 궤적”으로 고쳤습니다.
- 도식 캡션 다섯 개를 동일한 색 범례에서 절별 학습 내용으로 교체했습니다.

## 검증

- 원본↔윤문본 수치·URL·고정 섹션 구조: 5/5 PASS
- 감사 동결 시점의 노트북 코드 셀·출력·실행 횟수: 5/5 원본 기준선과 동일. 감사 완료 후 02 노트북의 기술 버그를 수정한 내용은 보고서 말미에 별도로 기록했습니다.
- SVG·Excalidraw·그림 생성기: 원본 기준선과 동일
- 학생용 한국어 금지 표현 검색: 0건. 노트북 코드 문자열과 저장 출력은 검색 대상에서 제외했습니다.
- 빌드: `uv run --project labs/part5/ch17-agent-overview --with pillow python textbook/part5/ch17-agent-overview/_build.py` — index 1개와 절 HTML 5개 생성
- 노트북-HTML 계약: `uv run --no-project --python 3.12 --with nbformat --with pillow --with pygments python textbook/_notebook/verify.py --chapter textbook/part5/ch17-agent-overview` — `PASS 5 sections / 25 code cells (max 17 lines)`
- Part 5 전체 배포 검사는 다운로드 압축 파일을 포함하는 통합 단계에서 실행해야 합니다.

## 최종 SHA-256

```text
f7b438760419a0fb82b5e0830cd336099d46276787da519d455fb621bca2aadb  textbook/part5/ch17-agent-overview/_src/01-워크플로우와-에이전트-경계.html
d782b572bdf377d19714d223ec70c9d51c62808ca920a469fe9721795d32319d  textbook/part5/ch17-agent-overview/_src/02-워크플로우가-충분한-조건.html
e1d4f45c5a381bf424d69576bd1ee0e925f6d2ea2e92c2a886b86594860a107c  textbook/part5/ch17-agent-overview/_src/03-모델-도구-루프와-정지-조건.html
e9fb8407ab60f8d2bb3b7a844812d6d276ea7bbdd446e6f8401fe0e40d9f6917  textbook/part5/ch17-agent-overview/_src/04-자율성의-대가.html
6de7b8a3cd8e6d8cf4c5281c95a49cdec5c229dcfa2ff672d14594d076940ae0  textbook/part5/ch17-agent-overview/_src/05-제품-트레이스와-자율성-진단.html
9cf652995957bf722f75a0acc0c0ddc7a5efdcf7e5d47cf745bd5d0eb52c36e4  textbook/part5/ch17-agent-overview/chapter.json
1961e77b02e94acdb2ee3b680b401f55194480c1d15a0bd8d3db9c1289132320  textbook/part5/ch17-agent-overview/figures/01-흐름.caption.md
709062fd52c2b848b5b3b4b601d68488c57108bd4ae9b6fcfb325b21d5dc2a89  textbook/part5/ch17-agent-overview/figures/02-흐름.caption.md
46236ebd65a5bb7579e1aa933c51518c104de184faf679e244005bc7b21551b7  textbook/part5/ch17-agent-overview/figures/03-흐름.caption.md
e795b1cbfd367433b7f6ca05035997829b6a097c4326b8a6fb5e85e45daa76ea  textbook/part5/ch17-agent-overview/figures/04-흐름.caption.md
25091d25f13005d8e81d10ec810fd74520d16369ac63f8261f9b4c8a07461e18  textbook/part5/ch17-agent-overview/figures/05-흐름.caption.md
f2f6df1c09933d5a1d6b12eda7e24284cb3b177a6bcb67cb68777a6f6d10f72d  labs/part5/ch17-agent-overview/README.md
8495098c89d9e0f656f4e684052ac3ed1a36c4095797464650f02d95f6ec35df  labs/part5/ch17-agent-overview/notebooks/01-워크플로우와-에이전트-경계.ipynb
87db56645b7afed16892d30d17130f91b9e695c42ffb4635d129b0742c456cb5  labs/part5/ch17-agent-overview/notebooks/02-워크플로우가-충분한-조건.ipynb
aaa4b960dd8d661488b0e7780ba585dcdf93c9513455aa3de762e1ced5a55603  labs/part5/ch17-agent-overview/notebooks/03-모델-도구-루프와-정지-조건.ipynb
a84258b58aa0b859150190567cf6599206bffdf2d1d37712c468bd6630fc6f21  labs/part5/ch17-agent-overview/notebooks/04-자율성의-대가.ipynb
7700280aae341215906d088e52830ddac18c574311e6b76a982becdf8c37fdad  labs/part5/ch17-agent-overview/notebooks/05-제품-트레이스와-자율성-진단.ipynb
942349c7a60f234d4d5a06319301c593b8e26d91508b7572ecd2cad6f3a2faff  textbook/part5/ch17-agent-overview/index.html
7c3a1f34ff93749a2fbcdd4629edbe91c7f4afbad6af6e12ffd0d37d08b2dd61  textbook/part5/ch17-agent-overview/01-워크플로우와-에이전트-경계.html
8d0fe4c97915ffd4cf65f91252ef768d8bfca9a0666cfe38cf4dfdac6d435eec  textbook/part5/ch17-agent-overview/02-워크플로우가-충분한-조건.html
a9ddda3f5dc607ac90496d6a1824ebd1d15c9d35e24eb40dec857fb9283c48d6  textbook/part5/ch17-agent-overview/03-모델-도구-루프와-정지-조건.html
82f09104b6771d3c215ce65d150cc2fcb99da280fdd76aa4412003d7f4831991  textbook/part5/ch17-agent-overview/04-자율성의-대가.html
b2c50f1e67756c7d916d608cd60d9401dfb2ece90db60ebd78b34756b3d5d700  textbook/part5/ch17-agent-overview/05-제품-트레이스와-자율성-진단.html
```

## 1차 기술 수정: 02 노트북 반복 출력

한국어 감사가 끝난 뒤, 02 노트북 마지막 셀의 임계값 반복에서 출력문이 반복문 밖에 있어 5만 출력되는 버그를 수정했습니다. 출력문을 반복문 안으로 옮기고 새 커널에서 실행해 임계값 3·4·5가 모두 저장된 것을 확인했습니다. `_src/02-워크플로우가-충분한-조건.html`은 바꾸지 않았고, HTML을 다시 빌드한 뒤 노트북-출력-다운로드 계약 검사를 다시 통과했습니다.

- 1차 기술 수정 직후 02 코드 셀 SHA-256: `979f0a98c1f6f75c9de629bc535ac4b4b5d613ac6cc323745dcc34c80f5d740c`
- 1차 기술 수정 직후 02 출력 SHA-256: `3a2b704e2b0287adaeed5af2ce7000ee95eced0859204eb94e8304d79991bcd9`
- 1차 기술 수정 직후 02 실행 횟수 SHA-256: `f5baf0e4336fd53b4c82b453ece859868475160d36f22e9551a0e9b10ac9cc00`
- 1차 기술 수정 직후 02 코드·출력·실행 횟수 결합 SHA-256: `0b6f5bbd9a1f0aaa59521fa2c5b5383de296ab78513d2dd0d0d3be65b0626567`
- 1차 기술 수정 직후 02 노트북 SHA-256: `b835910ccb0bbf9b459a22b765207c5fb36dc485166c0b4e25d8623c1b6733f0`
- 1차 기술 수정 직후 02 `_src` SHA-256: `d782b572bdf377d19714d223ec70c9d51c62808ca920a469fe9721795d32319d`
- 1차 기술 수정 직후 02 빌드 HTML SHA-256: `cef58cf6e2d64cd9bd4f2ab839b70ef72aa645fd54699550b4b54a5dc7a3e9d7`
- 재검증: `PASS 5 sections / 25 code cells (max 17 lines)`

## 2차 최종 기술 수정: 타입 표기와 미사용 import

5개 노트북의 함수 타입 표기 오류 8건을 고치고 준비 셀의 미사용 import를 정리한 뒤 새 커널에서 다시 실행했습니다. `_src` 본문과 노트북 마크다운은 한국어 감사 확정본과 같습니다. 추가된 한국어는 04 준비 셀의 “비용·지연 사건의 필드 타입을 고정해 합산 대상을 분명히 합니다.”라는 주석 한 줄입니다. 이 주석은 `CostEvent` 타입 정의와 바로 이어지며, `ms`와 `cost`를 합산하는 후속 코드의 대상을 설명합니다. 본문의 뜻과 계산 결과는 달라지 않았습니다.

| 절 | 코드 셀 SHA-256 | 출력 SHA-256 | 실행 횟수 SHA-256 | 코드·출력·실행 횟수 결합 SHA-256 |
|---|---|---|---|---|
| 01 | `143d6b7b35ca7bcfd88654c748c3260639d2ff84ecc559a7cec4a880b0035f12` | `ee4a81364438cf83524ffc4e9c5cb82bd1bef4bebac2704d3dc30eaeac8e724d` | `f5baf0e4336fd53b4c82b453ece859868475160d36f22e9551a0e9b10ac9cc00` | `7a20e6eb313113f2e8f1177ebab84487e7df16dee77b8eac5412ac23cfa52569` |
| 02 | `cf57455eb4d7855278e294a58d26871cfeecaf9fcc7010a6456beec19feee964` | `3a2b704e2b0287adaeed5af2ce7000ee95eced0859204eb94e8304d79991bcd9` | `f5baf0e4336fd53b4c82b453ece859868475160d36f22e9551a0e9b10ac9cc00` | `e37647c668aad6cb2033789ef02ae6c9ba2bf8f4e8becedbab3d62149556e67b` |
| 03 | `98cbdb9602436dad0e3e05e5083c815952b7af41326bca9c9b9229b12e5622b7` | `8e2d315abc4e6595de811d68fa4c5fccd84236dcd4ac5cf99cae5976afc991fe` | `f5baf0e4336fd53b4c82b453ece859868475160d36f22e9551a0e9b10ac9cc00` | `d93fdd40d73e4f772e720901ee246685ee5335abf3ca1a010b36900a2c4a85a4` |
| 04 | `1ccdfb67bbc4dd39965116b62dff35abafcebc7143fd74389e7e84fd003792be` | `011069a1dee08dd5a9778bc635c802496e8650a20440b26143ffb76f5247002c` | `f5baf0e4336fd53b4c82b453ece859868475160d36f22e9551a0e9b10ac9cc00` | `17ff10d5329eddbd2e23cff4aab1552d56b472d8f8f4e9dc3b54c2d0098582b7` |
| 05 | `874c038255df74186f0eeecb6d64ffe2b98780df2daf505cc2425679d4dece1b` | `fd6585cae8f83904c668f2985e3c7769a21e02f726e13dc46346658bf7606a0d` | `f5baf0e4336fd53b4c82b453ece859868475160d36f22e9551a0e9b10ac9cc00` | `4c7a3ecf83fde999331b0c7e4950869db3f83769e9e5d7f827a14757a2ae5d40` |

최종 검증은 노트북-본문-출력-다운로드 계약 `PASS 5 sections / 25 code cells (max 17 lines)`, Ruff `All checks passed!`, Pyright 오류 0건, 기술 검토 `APPROVE`입니다. 새 커널의 `executed_at`은 2026-09-10 06:44:46~06:44:49Z입니다.
