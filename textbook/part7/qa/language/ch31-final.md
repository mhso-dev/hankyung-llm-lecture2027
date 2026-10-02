# Ch31 한국어 최종 감사

## 진단 요약

- 대상은 `_src/`의 다섯 절, 다섯 노트북 Markdown 셀, `labs/part7/ch31-database/README.md`입니다. 장르는 산문이며 최소 심각도는 S1로 적용했습니다. 코드 셀·출력·명령어·경로는 감사 대상에서 제외했습니다.
- `ai-slop-reviewer` 기준의 일반 슬롭 점검과 로컬 맞춤법·띄어쓰기 정독 뒤 `korean-humanize` 기준의 전문 정독을 적용했습니다. 영문 수사 구조, 이중 피동, 구어 축약, 금지된 비유 동사, `함정` 표현과 S1 수준의 문장 오류는 발견되지 않았습니다.
- 외부 맞춤법 전송은 생략했습니다. `korean-spell-check`의 대량 배치·상업 서비스 제한 때문에 과정 교재 챕터 전체를 공용 서비스에 전송하지 않았습니다. 외부 전송 없이 전문 정독으로 맞춤법과 띄어쓰기를 확인했습니다.
- 짧은 문장이 이어지는 곳은 학습 목표·절차·정리·퀴즈의 목록성 교육 문맥입니다. 핵심 설명 단락에는 단문과 복문이 섞여 있어 기계적인 단문화로 판정하지 않았습니다. 기술적 대조문과 한정어는 의미를 보존하기 위해 그대로 두었습니다.

## 수정 경로와 주요 변경사항

- 수정한 학생용 본문, 노트북 Markdown, README는 없습니다. 원문이 기술 문서로서 정확하고 자연스럽게 읽혀 불필요한 치환을 하지 않았습니다.
- 노트북 Markdown과 README의 SHA-256은 감사 시작 기준본과 같습니다. 언어 감사 중 코드와 실행 출력을 수정하지 않았습니다. 이후 통합 검증에서 03절 준비 셀의 현재·상위 폴더 탐색 경로가 보정되어 코드 해시만 바뀌었고, Markdown에는 변경이 없습니다. 재실행과 재빌드 뒤 검증기는 다섯 절과 27개 코드 셀을 통과시켰습니다.

## 구조 메트릭과 검증

- `_src/` SHA-256: 01 `cead55b396725297f242566b4d3b0f4f14c4843c0c874f51410c93e362db2c55`, 02 `3ddde6a4a54467e298f07af883cde7ad194c2c9a90392118a2d5a7b8ba268adc`, 03 `89caec122afc18bbfaff9d365d26bfcfd051691ca60acbc7f15a91323805c147`, 04 `d077481c5cf5c0f1d45a4c6a52ccdf785b4495ca3abbad53568f0205f9fcec9e`, 05 `6faf7d306db4fac47bcbc3b42ac31b7202e256dd326dc068ffb16ad387404f78`입니다.
- 통합 검증 뒤 03절 노트북 SHA-256은 `f7c9626fbb5dfb82f5316b95466e836e5b2b798c6f39baf22fdcab532b9b2cf8`입니다. 나머지 노트북 Markdown과 README는 감사 시작 기준본과 같습니다.
- `uv run --project labs/part7/ch31-database --with pillow python textbook/part7/ch31-database/_build.py`를 실행해 다섯 HTML과 `index.html`을 다시 생성했습니다.
- `uv run --project labs/part7/ch31-database python textbook/_notebook/verify.py --chapter textbook/part7/ch31-database`는 `PASS 5 sections / 27 code cells (max 25 lines)`를 반환했습니다.

## Phase 6 최종 검수

최종 검수: accept

- 의미 보존 15항: 통과. 수치·날짜·고유명사·인용·용어·조건·예시·제목·문단 순서를 바꾸지 않았습니다.
- 자연성 잔존: S1 수준 패턴이 없습니다. 기술적 의미를 가진 대조문은 보존했습니다.
- 과윤문: 없습니다. 격식 상향, 상투구 주입, 문학화, 한정어·양태 변경이 없습니다.
- 게이트: Ch31에는 수정이 없으므로 원문↔원문 대조로 실행하지 않았습니다. 대신 재빌드와 노트북·HTML 무결성 검증을 통과했습니다.
- Codex 적대적 감사: 해당 선택 도구가 없어 실행하지 않았습니다.

판정: accept. 확인이 필요한 잔여 언어 항목은 없습니다.
