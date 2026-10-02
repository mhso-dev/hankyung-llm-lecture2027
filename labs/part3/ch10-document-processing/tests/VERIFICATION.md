# Verification

- Date: 2026-09-08
- Command: `uv sync && uv run pytest -q && uv run ruff check tests`
- Tests: 38 passed in 1.76s, 0 failed
- Ruff: 0 errors
- Regressions fixed: 2
  1. HWPX numeric section ordering (`section2` before `section10`)
  2. Explicit failure when one Unicode code point exceeds `chunk_tokens`
