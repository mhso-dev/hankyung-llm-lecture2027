# 진단 기록 — 챕터 끝 실습 절을 지침에 반영 (2026-09-16)

- 트리거: `/project evolve`(명시 요청 — 사용자 「미들웨어 실습이 맘에 든다. 지침에 추가했나? 안 했으면 업데이트」)
- 사전 상태: `textbook/QUALITY-UPGRADE.md` §7-2에는 규칙이 있었으나 `AGENTS.md` §9 체인 ⑨·§19와 `easy-upgrade-editor`(Claude·Codex)에는 없었다. 에이전트 7-step ⑤는 「절 추가」를 blocker로 규정해 실습 절 추가와 충돌했다. §19에 낡은 사실(Higgsfield 잔액 1크레딧, 게이트 「시범 첫 단계에서 작성」)이 남아 있었다.
- 수정 파일(3개): `AGENTS.md`(§9 ⑨ 체인·라우팅 문장, §19 그림·실습 절·검사·순서), `.claude/agents/easy-upgrade-editor.md`, `.codex/agents/easy-upgrade-editor.toml`(description, ⑤ 범위 예외, 6-8 실습 절 절차, 체크리스트 1줄, 출력).
- 되돌리기 원본: `.moai/evolution/chapter-practice-before-2026-09-16/`(수정 전 세 파일 전체).
- 기준 사례: `textbook/part6/ch22-middleware/_src/09-Middleware-실습.html`, `labs/part6/ch22-middleware/notebooks/09-Middleware-실습.ipynb`.
- 검증: AGENTS.md 361줄(500줄 이내), HARD 블록 수 변동 없음, Codex TOML 파싱 확인.
