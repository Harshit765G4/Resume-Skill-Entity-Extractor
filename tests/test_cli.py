import json

import pymupdf

from resume_extractor.cli import main


def test_cli_prints_json_for_valid_resume(tmp_path, capsys):
    pdf_path = tmp_path / "resume.pdf"

    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((72, 72), "Python developer using TensorFlow.")
        document.save(pdf_path)

    exit_code = main([str(pdf_path)])

    captured = capsys.readouterr()
    result = json.loads(captured.out)

    assert exit_code == 0
    assert result["source_file"] == "resume.pdf"
    assert result["skills"] == ["Python", "TensorFlow"]
    assert captured.err == ""


def test_cli_reports_missing_file(tmp_path, capsys):
    exit_code = main([str(tmp_path / "missing.pdf")])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error:" in captured.err
    assert captured.out == ""
