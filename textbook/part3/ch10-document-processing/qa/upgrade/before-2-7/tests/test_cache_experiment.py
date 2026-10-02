import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from document_processing import EmbeddingCache, preflight_corpus
from experiment import corpus_paths, load_questions, run_experiment


class RecordingEmbedder:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def __call__(self, texts: list[str]) -> list[list[float]]:
        self.calls.append(texts)
        return [[float(len(text)), 1.0] for text in texts]


def cache_call(cache: EmbeddingCache, embedder: RecordingEmbedder, **changes):
    options = {
        "texts": ["한국어 문장"],
        "provider": "local",
        "model": "model-a",
        "version": "v1",
        "dimensions": 2,
        "embedder": embedder,
    }
    return cache.embed(**{**options, **changes})


def test_embedding_cache_returns_hit_without_reembedding(tmp_path: Path) -> None:
    cache = EmbeddingCache(tmp_path)
    embedder = RecordingEmbedder()

    _, first = cache_call(cache, embedder)
    _, second = cache_call(cache, embedder)

    assert (first.hits, first.misses) == (0, 1)
    assert (second.hits, second.misses) == (1, 0)
    assert len(embedder.calls) == 1


@pytest.mark.parametrize(
    ("change", "value"),
    [
        ("texts", ["다른 문장"]),
        ("provider", "other-provider"),
        ("model", "model-b"),
        ("version", "v2"),
        ("dimensions", 3),
    ],
)
def test_embedding_cache_separates_material_embedding_inputs(
    tmp_path: Path, change: str, value: object
) -> None:
    cache = EmbeddingCache(tmp_path)
    embedder = RecordingEmbedder()
    cache_call(cache, embedder)

    _, stats = cache_call(cache, embedder, **{change: value})

    assert (stats.hits, stats.misses) == (0, 1)


def test_preflight_corpus_deduplicates_identical_content(tmp_path: Path) -> None:
    paths = [tmp_path / name for name in ("one.pdf", "copy.pdf", "two.pdf")]
    paths[0].write_bytes(b"same")
    paths[1].write_bytes(b"same")
    paths[2].write_bytes(b"different")

    result = preflight_corpus(paths, required=3)

    assert result == {"required": 3, "available": 2, "ready": False, "duplicate_files": 1}


def test_experiment_questions_use_expected_qids_and_gold_documents() -> None:
    rows = load_questions()

    assert {row["qid"] for row in rows} == {"Q001", "Q037", "Q088"}
    assert {row["doc_id"] for row in rows} <= {path.stem for path in corpus_paths()}


def test_experiment_corpus_paths_are_18_actual_pdf_files() -> None:
    paths = corpus_paths()

    assert len(paths) == 18
    assert all(path.is_file() and path.suffix == ".pdf" for path in paths)


@pytest.fixture(scope="module")
def experiment_result(tmp_path_factory: pytest.TempPathFactory):
    root = tmp_path_factory.mktemp("experiment")
    import experiment

    original_cache = experiment.CACHE_DIR
    experiment.CACHE_DIR = root / "cache"
    try:
        summaries = run_experiment(backend="educational-feature-hash", output_dir=root / "runs")
    finally:
        experiment.CACHE_DIR = original_cache
    return root, summaries


def test_experiment_writes_six_chunk_and_model_runs(experiment_result) -> None:
    _, summaries = experiment_result

    assert {(row["chunk_method"], row["embedding_candidate"]) for row in summaries} == {
        (chunk, model)
        for chunk in ("recursive", "token", "structural")
        for model in ("text-embedding-3-small", "text-embedding-3-large")
    }


def test_experiment_logs_loaded_corpus_page_counts(experiment_result) -> None:
    _, summaries = experiment_result

    assert len(summaries) == 6
    assert all(row["corpus_available"] == 18 for row in summaries)
    assert all(row["n_pages"] > 0 for row in summaries)


def test_experiment_keeps_metrics_as_future_evaluation_placeholders(experiment_result) -> None:
    root, summaries = experiment_result

    assert all(row["metrics"] == {} for row in summaries)
    for summary in summaries:
        details = [
            json.loads(line)
            for line in (root / "runs" / summary["detail_file"])
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        assert all(row["metrics"] == {} for row in details)


def test_experiment_second_cache_pass_has_no_misses(experiment_result) -> None:
    _, summaries = experiment_result

    assert all(row["second_pass_cache_misses"] == 0 for row in summaries)
