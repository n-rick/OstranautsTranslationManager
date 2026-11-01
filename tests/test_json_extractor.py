from src.scanner.json_extractor import JsonExtractor


def test_extract_multiline_json_string(tmp_path):
    source_text = "First line\n\nSecond line"
    source_file = tmp_path / "sample.json"
    source_file.write_text(
        '{"strDesc": "First line\n\nSecond line"}',
        encoding="utf-8",
    )

    units = JsonExtractor().extract(
        str(source_file),
        "interactions/sample.json",
    )

    assert len(units) == 1
    assert units[0].source_text == source_text