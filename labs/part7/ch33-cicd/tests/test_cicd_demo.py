from pathlib import Path
from cicd_demo import answer, image_digest

def test_answer_requires_question():
    assert answer("") == "질문이 필요합니다."

def test_digest_is_stable(tmp_path: Path):
    artifact = tmp_path / "image.tar"
    artifact.write_bytes(b"agent-service-v1")
    assert image_digest(artifact) == image_digest(artifact)
