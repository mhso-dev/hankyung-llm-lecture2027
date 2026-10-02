# Part 1 delivery verification

Date: 2026-09-09. Scope: complete Ch 3–5 and integrate them with the existing Ch 1–2.

## Completion evidence

The final machine-readable result is `delivery-results.json`. It checks the 35 canonical notebooks against the HTML code, actual outputs, and embedded notebook downloads; the ten required lesson blocks; three to five review questions per lesson; the 37 lecture / 59 practice hour allocation; local navigation targets; paired SVG/Excalidraw files; both distribution archives and their SHA-256 manifests; and preservation of the 36 baseline Ch 1–2 student files.

Final status: PASS. All 35 notebooks / 194 code cells (maximum 24 lines) match their 42 HTML pages and embedded downloads. There are 135 review questions, 35 SVG/Excalidraw pairs, 277 valid local links, zero missing links, and zero detected credential exposures. Both ZIP archives pass CRC and manifest-to-source SHA-256 checks. All 84 browser checks pass at 1280px and 390px, including copy/download behavior, text size, contrast, clipping, diagram bounds, and page overflow. Existing Ch 1–2 student files remain unchanged (36 baseline hashes).

Common regression tests: 37 passed plus 16 subtests. Ch 4 module tests: 8 passed, including a fresh installation of the public package. The new chapters have independent technical and Korean prose review, followed by final meaning review from a different model. Late visual checks corrected mobile SVG scaling in Ch 5-06–08 and the accompanying descriptions of their actual four-box diagrams; the final source hashes and browser results include those corrections.

## Reproduction

- Execute notebooks with `textbook/_notebook/execute.py` from their pinned `uv` project, using Python 3.12 and a fresh kernel for each notebook.
- Build each changed chapter with its `_build.py`, then run `textbook/_notebook/verify.py --chapter CHAPTER`.
- Build the Part 1 index and archive with `textbook/part1/_build_index.py`, then the common index and archive with `textbook/_notebook/build_index.py` and `build_bundle.py`.
- Run `textbook/part1/qa/check_delivery.py` with `python-dotenv` available.
- Run `textbook/_notebook/visual.cjs` for each chapter, the Part 1 index, and the common index at 1280px and 390px.

## Evidence records

- `integration-code-checks.json`: common regression tests and static checks; Ch 3 isolated Git execution.
- `student-install-check.json`: Ch 4 public files copied into a fresh directory, installed from `uv.lock`, and tested without importing the working repository.
- `model-student-install-check.json`: Ch 5's lockfile installed in a fresh directory without dependency overrides; the student kernel and model imports passed.
- `figure-review.json`: independent browser measurement of Ch 3 and Ch 5's 13 diagram pairs, including labels inside boxes, matching arrows, and semantic colors.
- `topic-review.md`: independent technical and educational review, including corrected token-budget calculations and the limits of model experiments.
- `language/` and each new chapter's `qa/language/`: language review snapshots, protected code/output hashes, and final meaning review.
- `final-meaning-review.md`: final review by a different model from the chapter authors.
- `research.md`: official references and version/model checks.
- `textbook/_notebook/checks/`: browser measurements and interaction results.

## Confirmed limitations

- Execution and browser checks use macOS. Windows/Linux execution and installation have not been independently measured.
- Ch 3 runs Git collaboration, review corrections, conflict resolution, recovery, and dummy-secret history cleaning in temporary local repositories. GitHub's hosted PR interface is explained but no real PR was published. Actual leaked credentials require revocation/replacement; the dummy exercise does not perform that external action.
- Ch 4 uses local HTTP fixtures and supplied public learning data. Live third-party websites and APIs are not required by the basic exercises.
- Ch 5 uses pinned pretrained local models. Model files are downloaded separately and are not bundled. The observed outputs are small controlled experiments, not general model rankings. Greedy repeated runs do not create independent stochastic samples. The context-rot exercise does not claim a length-based degradation that its outputs did not show. Cached loading and tokenization times are not generation latency or TTFT.
- No paid model API was invoked for the new Part 1 lessons. Generated illustration credits used: 0.
- Excalidraw MCP preview was unavailable. SVG and Excalidraw files share their element lists and are checked structurally and in the browser.
- The external Korean spelling service was skipped because its installed [korean-spell-check skill](/Users/mhso/.codex/plugins/cache/moai-cowork/moai-writer/1.4.1/skills/korean-spell-check/SKILL.md) prohibits “상업적 대량 처리” and “대량 배치”. This multi-chapter commercial course manuscript falls within that restriction. Local spelling review, prose review, and final meaning checks replace that external transmission.
