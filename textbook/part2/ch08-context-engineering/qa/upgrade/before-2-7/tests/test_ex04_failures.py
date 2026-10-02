import importlib.util
from pathlib import Path


def load_example():
    path = Path(__file__).resolve().parents[1] / "examples" / "ex04_failures.py"
    spec = importlib.util.spec_from_file_location("ex04_failures", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_four_failure_modes_have_clean_baseline() -> None:
    cases = load_example().conditions()
    assert set(cases) == {"clean", "poisoning", "distraction", "confusion", "clash"}
    assert all("매주 월요일" in context for _, context in cases.values())


def test_evaluation_keeps_raw_checks() -> None:
    result = load_example().evaluate("월요일입니다. [E01 p.2]")
    assert result == {
        "mentions_monday": True,
        "has_source": True,
        "mentions_unsupported_wednesday": False,
        "claims_missing_information": False,
    }


def test_contradictory_refusal_is_not_counted_as_complete_answer() -> None:
    module = load_example()
    evaluation = module.evaluate("정보가 없습니다. 다만 월요일입니다. [E01 p.2]")
    assert module.is_complete_answer(evaluation) is False


def test_conflicting_weekdays_are_not_counted_as_complete_answer() -> None:
    module = load_example()
    evaluation = module.evaluate("정기 휴관일은 월요일과 수요일입니다. [E01 p.2]")
    assert module.is_complete_answer(evaluation) is False
