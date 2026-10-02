from tempfile import TemporaryDirectory

from _paths import ROOT

from document_processing import (
    educational_feature_vectors,
    embed_with_cache,
    estimate_embedding_cost,
)


def main() -> None:
    texts = ["제주 배송은 이틀이 더 필요합니다.", "환불은 7일 이내 신청합니다."]
    model = "text-embedding-3-small"
    with TemporaryDirectory(dir=ROOT) as directory:
        common = {
            "texts": texts,
            "cache_dir": ROOT / directory,
            "provider": "educational-feature-hash",
            "model": model,
            "version": "v1",
            "dimensions": 128,
            "input_prefix": "",
            "embedder": educational_feature_vectors,
        }
        first_vectors, first = embed_with_cache(**common)
        _, second = embed_with_cache(**common)
    estimate = estimate_embedding_cost(texts, usd_per_million_tokens=0.02)
    print(f"candidate_model={model} status=[[미정: 임베딩 모델]]")
    print(f"first_pass=hits:{first.hits},misses:{first.misses}")
    print(f"second_pass=hits:{second.hits},misses:{second.misses}")
    print(f"vector_dimensions={len(first_vectors[0])}")
    print(f"estimated_tokens={int(estimate['tokens'])} estimated_usd={estimate['estimated_usd']:.8f}")


if __name__ == "__main__":
    main()
