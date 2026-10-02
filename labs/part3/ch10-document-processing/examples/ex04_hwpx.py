import zipfile

from _paths import FIXTURES

from document_processing import load_hwpx, recognize_hwp_kind


def make_minimal_hwpx_marker() -> tuple:
    """로더 실습용 ZIP/XML 표식 fixture이며 한컴오피스 호환 문서 생성기가 아니다."""
    FIXTURES.mkdir(exist_ok=True)
    hwpx_path = FIXTURES / "minimal-marker.hwpx"
    section = """<?xml version="1.0" encoding="UTF-8"?>
<hp:section xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph">
  <hp:p><hp:run><hp:t>한글 문서 처리 실습입니다.</hp:t></hp:run></hp:p>
</hp:section>"""
    with zipfile.ZipFile(hwpx_path, "w") as archive:
        archive.writestr("Contents/content.hpf", "<package/>")
        archive.writestr("Contents/section0.xml", section)
    hwp_path = FIXTURES / "legacy-signature.hwp"
    hwp_path.write_bytes(bytes.fromhex("D0CF11E0A1B11AE1") + b"training-marker")
    return hwpx_path, hwp_path


def main() -> None:
    hwpx_path, hwp_path = make_minimal_hwpx_marker()
    docs = load_hwpx(hwpx_path)
    print(f"hwpx_kind={recognize_hwp_kind(hwpx_path)} sections={len(docs)}")
    print(f"text={docs[0].page_content}")
    print(f"legacy_container={recognize_hwp_kind(hwp_path)}")
    try:
        load_hwpx(hwp_path)
    except ValueError as error:
        print(f"legacy_load=rejected reason={error}")
    print("fixture_scope=loader marker only; not a full Hancom-compatible document")


if __name__ == "__main__":
    main()
