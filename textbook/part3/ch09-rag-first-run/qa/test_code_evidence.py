from check_content import (
    check_output_manifest,
    check_preserved_outputs,
    check_reference_expansion,
)


def test_legacy_source_references_are_absent_or_expand_correctly() -> None:
    assert check_reference_expansion() == []


def test_preserved_outputs_match_before_snapshot() -> None:
    assert len(check_preserved_outputs()) == 12


def test_output_manifest_hashes_match_files() -> None:
    assert len(check_output_manifest()) == 12
