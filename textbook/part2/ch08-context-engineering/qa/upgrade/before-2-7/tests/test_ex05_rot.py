import importlib.util
from pathlib import Path


def load_example():
    path = Path(__file__).resolve().parents[1] / "examples" / "ex05_rot.py"
    spec = importlib.util.spec_from_file_location("ex05_rot", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_only_evidence_position_changes() -> None:
    module = load_example()
    noise = module.filler(100)
    contexts = {position: module.position_evidence(noise, position) for position in ("start", "middle", "end")}
    for context in contexts.values():
        assert context.count(module.EVIDENCE) == 1
        restored = context.replace("\n" + module.EVIDENCE, "").replace(
            module.EVIDENCE + "\n", ""
        )
        assert restored.replace("\n", "") == noise.replace("\n", "")


def test_length_conditions_are_ordered() -> None:
    module = load_example()
    estimates = [module.estimate_tokens(module.filler(value)) for value in module.TARGET_TOKENS.values()]
    assert estimates == sorted(estimates)
    assert len(set(estimates)) == 3
