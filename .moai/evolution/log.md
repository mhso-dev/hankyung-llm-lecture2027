2026-09-15 | explicit request | textbook/QUALITY-UPGRADE.md(신규) · AGENTS.md §9·§15·§16·§17·§19 · easy-upgrade-editor(신규) · figure-maker · lab-notebook-builder · textbook-writer · context.md · config.json | 품질 개선 단계 규격과 체인 ⑨ 추가. 원문: quality-upgrade-before-2026-09-15/
2026-09-09 | reusable template | textbook/_template · AUTHORING.md · AGENTS.md · agents | 비교형/실험형 템플릿과 새 세션 집필·검토 기준 확정. 실행·화면·지침 검증 완료. template-guidance-verification.md 참고.
2026-09-08 | repeated correction | AGENTS.md·textbook-writer 양쪽 | §17 노트북 우선 집필·실제 커널/API 검증·공통 HTML 형식·설명과 실제 연산 대조를 반영. 원문은 notebook-format-before에 보존.
# evolution log (최신순)
2026-09-16 | /project evolve | AGENTS.md §9 ⑨·§19, easy-upgrade-editor(Claude·Codex) | 챕터 끝 실습 절({NN}-{챕터}-실습, Ch 22 09-Middleware-실습 기준)을 체인 ⑨·에이전트 절차에 반영, 절 추가 blocker 예외, §19 낡은 사실 갱신. 진단: chapter-practice-2026-09-16.md
2026-09-15 | pilot result | QUALITY-UPGRADE.md §3·§5-3·§6·§7·§10, upgrade_gates.py G5, Ch 22 | 시범 8절 게이트 386→0건·검토 2회 반영. 규격 상태를 「시범 결과 반영, 강사 확인 대기」로 갱신. 삽화 8장 대기.
2026-09-07 | inventory drift | AGENTS.md §5·§12, figure-maker, config.json | Higgsfield 커넥터 연결 확인 → '미인증' 표기를 실제 상태로 갱신
2026-09-07 | repeated correction | AGENTS.md §16, figure-maker | 삽화는 장식이 아닌 교육 자료 — 설명 대상 문장·3질문 게이트·허용 4유형·검수 기준 추가
2026-09-07 | deliverable | labs/data/rag-corpus | RAG 문서 세트 21 PDF·질의셋 149 생성, context.md 미정 항목 '도메인 문서 세트' 확정
2026-09-07 | repeated correction | AGENTS.md §14-1, context.md | 작업 단위=챕터, 집필/검토 세션 분리, 챕터 종료 시 '만든 것' 기록, 세션별 모델 결정

## 2026-09-08 — Ch 9 집필·검토 반영
- AGENTS.md: §14-4 신설(문어체 어휘 표 17행), §14-5 신설(산출물 구조·빌드), §15·§16 실무 보강, §14-1 검토 반영 절차, §9 체인 ① 갱신, §18 "회수" 내부 용어 주석
- 에이전트: textbook-writer(집필 순서 코드→본문, 빌드, 체크리스트 3항 추가), figure-maker(생성기 정본, 삽화 모델·검수)
- 교재: Ch 9 6절 문체 수정 ~115곳, "함정" 0건, 데이터셋 문서 동기화
