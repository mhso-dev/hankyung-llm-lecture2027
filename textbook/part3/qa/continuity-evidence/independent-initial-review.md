# Independent Ch8-Ch12 continuity review: initial state

## Verdict

**PARTIAL / REQUEST CHANGES.** The pre-change materials contain confirmed continuity defects. Several direct data checks pass, but the pre-change prose, notebook APIs, Ch11-to-Ch12 log contract, and distribution state do not satisfy the completion criteria.

This review is independent of the writing and implementation lanes. It uses the preserved pre-change archive at `textbook/part3/qa/continuity-evidence/before.tar.gz` and direct inspection of current source, notebooks, data, logs, and bundle inputs. Existing QA PASS labels were not used as evidence.

## Confirmed defects

| ID | Severity | Promise or claim | Direct evidence and impact |
| --- | --- | --- | --- |
| F-01 | High | Ch8 `_src/06-단계적-공개와-설계-비교.html:88` says Ch11 evaluates selection and answer results. | Ch11 `_src/01-질의셋과-정답-문서-ID.html:7` explicitly limits automated work to retrieval metrics and defers automated answer evaluation to Ch15. Students can mistake retrieval evaluation for answer evaluation. |
| F-02 | High | Ch9 `_src/04-생성과-출처-인용.html:7` says source-format compliance is measured from Ch11. | Ch11 defines retrieval metrics and answer-review criteria but does not automate answer or citation-format evaluation. That automation is assigned to Ch15. |
| F-03 | High | Ch9 `_src/01-RAG-지도.html:19` and `_src/02-로더와-스플리터.html:16` say Ch4 already used `pypdf.PdfReader` and `page.extract_text()`. | Direct search of the student Ch4 text and notebooks finds no such API. Ch4's parsing lesson uses HTML parsing. The false prerequisite sends students looking for absent code and hides that PDF parsing is first introduced in Ch9. |
| F-04 | High | Ch12 `_src/01-벡터-거리와-정확-검색.html:4` refers to Ch9's `search()`. | Extracting all code cells from the six Ch9 student notebooks finds no `def search`; they use `similarity_search()` and `similarity_search_with_score()`. `search()` exists only in the non-distributed internal `labs/part3/ch09-rag-first-run/rag.py`. ZIP-only students cannot recover the named function. |
| F-05 | High | Ch11 `_src/01-질의셋과-정답-문서-ID.html:4` says Ch10 implemented PDF-to-page-to-chunk processing with `doc_id` and `page`. | Direct notebook inspection shows Ch10 separately demonstrates PDF metadata/extraction and synthetic chunking. The complete PDF-to-`Document`-to-chunk path is in Ch9. The claim points students to an output that Ch10 did not create. |
| F-06 | Medium | Ch10 `_src/01-문서와-메타데이터.html:77` promises that Ch12 aggregates failures by `file_type` and `parser`. | Direct search of Ch12 source, notebooks, and data finds no use or aggregation of either field. The promised downstream use is absent. |
| F-07 | High | Ch11 `_src/06-실험-로그와-자동-실행.html:7,11` and Ch11 `README.md:9` require `corpus_fingerprint`, `slices`, and per-question `results` containing `qid`, `gold_doc_ids`, `returned_count`, ranks, and metrics. They say Ch12 will accumulate 30 or more logs using the same evaluation file. | Each row of Ch12 `runs/advanced-experiment-log.jsonl` contains only aggregate metrics plus `corpus_sha256`, `query_sha256`, settings, counts, timing, and split. `advanced-test-result.json` is also aggregate-only. No per-question raw result exists, so the averages cannot be diagnosed and the promised Ch11 log contract is not carried forward. |
| F-08 | Medium | Ch12's integrated run selects Ch11 question Q009. | `runs/advanced-integrated-result.json` stores the question text but omits `qid`, `gold_doc_ids`, and `split`. The result is not self-identifying against the inherited evaluation set. |
| F-09 | Medium | Ch10 `_src/index.html:27` says Ch12 changes chunking, search, and reranking settings based on metrics. | The 36-run experiment uses fixed `advanced-documents.json` chunks and varies TF-IDF `analyzer`/`ngram` plus MMR `report_k`/`lambda`. It does not compare chunking settings. The stated experiment scope is broader than the code. |
| F-10 | High | Ch9 lesson 4 fixes the citation format as `[doc_id p.page]` and says both `doc_id` and `page` are required. | The newly generated Ch9 continuity record builds page-tagged context but prompts only for a bracketed document ID. Its actual API output ends in `[E01]`, without a page. The saved answer therefore violates the chapter's own citation format and is unsuitable as a later answer-evaluation record until it is freshly regenerated with a page citation. |
| F-11 | Medium | The continuity log's `config` field should describe the retrieval/generation settings and remain constant across questions in one run. | Ch9 notebook 06 loads `qid`, `gold_doc_ids`, and `question` into the YAML configuration, then saves the whole object under `config` while also saving those fields at the top level. This duplicates labels inside settings and would make a multi-question run appear to have different configurations. |
| F-12 | High | Ch11's revised minimum log contract requires `run_date` plus returned document, page, chunk, and rank fields in each question result. | The first revised Ch12 continuity logs add 15 per-question rows to every dev/test report, but those rows contain only `candidate_doc_ids` and `top_doc_ids` string lists. They omit `page`, `chunk_id`, and `rank`; the test report also omits `run_date`. The raw result cannot diagnose page/chunk selection or fully satisfy the promised log contract. |
| F-13 | Medium | `source_chapter` identifies the chapter that produced a retrieval run in the Ch9 and Ch10 handoff logs. | The first revised Ch12 dev/test logs set `source_chapter` to `Ch11` even though Ch12 produced the runs. The inherited question file is already identified by `query_source`. Reusing one field with a different meaning breaks schema consistency. |
| F-14 | High | Ch11's revised lesson 6 says its own minimum per-question result preserves document, page, chunk, and rank. | Ch11 `evaluate.py::evaluate()` initially retained only `top_doc_ids` for the standalone baseline, discarding page and score and never assigning chunk/rank fields. Only the external Ch9/Ch10-log path retained structured `top_results`. The baseline therefore did not satisfy the chapter's own revised log contract. |
| F-15 | High | Metric names must identify a cutoff that was actually observed. | The Ch9 handoff saves only two ranked candidates, so Recall@5, Precision@5, nDCG@5, and Recall@50 are all unmeasured. The Ch10 handoff saves five candidates, so its @5 metrics are measurable but Recall@50 is not. The initial continuity evaluator computed every metric anyway, treating absent ranks as observed nonrelevant results. |
| F-16 | High | The revised learning path says development questions are used during design and test questions are inspected only after selection. | Ch11 notebook 01 still used `dataset[:30]` and printed the full 30-question gold-document distribution while teaching dataset-size comparison. That continues to expose test labels before selection and contradicts the new guide's warning about prior full-set inspection. |
| F-17 | Medium | Ch9's revised prose must describe the canonical handoff log that its notebook actually writes. | The first revision of Ch9 `index.html:5` said the JSONL stored only settings and retrieval IDs even though the record also stored `answer`. Lesson 6 said Ch11 would extend a blank `metrics` member, but the Ch9 record had no such member and Ch11 correctly wrote a separate evaluation result. This conflicted with the non-overwrite rule and the actual log schema. |

## Directly passing checks

| ID | Claim | Evidence |
| --- | --- | --- |
| P-01 | Ch11 and Ch12 use the same 30 evaluation questions. | Canonical comparison with `jq -S` and `cmp` returns 0. All fields and values match: `qid`, `split`, `question`, `gold_doc_ids`, `answerable`, `tier`, and `type`. The split is 15 dev and 15 test. The file byte hashes differ because one file is JSONL and the other is a JSON array. |
| P-02 | Ch12 advanced parents and children are derived from the distributed PDFs. | Reconstructing the generator under the locked Ch12 environment (`pypdf==6.18.0`) yields 6 parents and 175 children with zero text, ID, page, source, or chunk-boundary differences. Every child `parent_id` resolves. Repeating with Ch11's older `pypdf==6.1.1` produces whitespace differences, so the exact output is parser-version dependent and must be verified in the Ch12 environment. |
| P-03 | Ch11 answer-criteria example citations resolve to the actual PDF pages. | Reading the PDFs with pypdf confirms E02 p.4 contains the domestic lodging and per-diem facts used in `[E02 p.4]`; E01 p.2 contains the Monday-closure and holiday-exception facts used in `[E01 p.2]`. |
| P-04 | The 36 setting runs are separate from the integrated RAG run. | The experiment log has 36 rows, 36 unique run IDs, and 36 unique settings; every row is `split=dev`, `query_count=15`. `advanced-test-result.json` separately evaluates the selected setting on 15 test questions. `advanced-integrated-result.json` is a separate one-question dense+sparse+reranker+generation run. Ch12 lesson 12 and its README describe this boundary. |
| P-05 | The new continuity guide states the principal comparison boundaries. | `labs/part3/continuity-guide.md:3,28-34` distinguishes retrieval from generation evaluation; document, question, chunking, retrieval, cutoff, and unit changes; Ch11 and Ch12 baselines; core and advanced data; and the 36-run search experiment from the integrated RAG run. Its referenced continuity logs still require creation and bundle verification. |

## Distribution state at the initial checkpoint

- `textbook/part3/public-files.json` lists Ch9 and Ch10 continuity logs, but both target files were absent at this checkpoint.
- `textbook/downloads/part3-practice.zip` and `textbook/downloads/llm-practice.zip` predate the guide and continuity-log additions and therefore cannot yet prove the ZIP-only path.
- Ch13 and Ch15 are not authored in this repository. Ch12-to-Ch13 and Ch12-to-Ch15 are therefore future contracts, not verified implementations. The final report must keep that limitation explicit.

## Reproducible evidence commands

```bash
jq -r '.cells[] | select(.cell_type=="code") | .source[]' \
  labs/part3/ch09-rag-first-run/notebooks/*.ipynb | \
  rg 'def search|similarity_search'

cmp -s \
  <(jq -S -s . labs/part3/ch11-evaluation/data/evaluation-queries.jsonl) \
  <(jq -S . labs/part3/ch12-retrieval-tuning/data/advanced-queries.json)

jq -s '{rows:length, run_ids:(map(.run_id)|unique|length), settings:(map(.settings)|unique|length), splits:(map(.split)|unique)}' \
  labs/part3/ch12-retrieval-tuning/runs/advanced-experiment-log.jsonl

jq -s '.[0] | keys' \
  labs/part3/ch12-retrieval-tuning/runs/advanced-experiment-log.jsonl
jq 'keys' \
  labs/part3/ch12-retrieval-tuning/runs/advanced-integrated-result.json
```

## Stop condition for final PASS

F-01 through F-17 must be corrected and rebuilt; HTML, notebooks, data, and logs must agree; fresh execution must prove the changed paths; both ZIPs must contain the required files without dangling paths; and an extracted ZIP must complete the representative Ch9-to-Ch10-to-Ch11 path. The independent final review will re-run the identifier, split, log-schema, output, and ZIP checks against the post-change state.
