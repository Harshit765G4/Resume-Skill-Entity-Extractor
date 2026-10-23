import pymupdf
import pytest

from resume_extractor.pdf_parser import extract_text


def create_pdf(path, text=None):
    """Create a synthetic PDF for testing."""
    with pymupdf.open() as document:
        page = document.new_page()

        if text:
            page.insert_text((72, 72), text)

        document.save(path)


def test_extract_text_from_valid_pdf(tmp_path):
    pdf_path = tmp_path / "resume.pdf"
    expected_text = "Python Developer with machine learning experience."

    create_pdf(pdf_path, expected_text)

    result = extract_text(pdf_path)

    assert expected_text in result


def test_missing_pdf_raises_file_not_found(tmp_path):
    pdf_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        extract_text(pdf_path)


def test_non_pdf_file_raises_value_error(tmp_path):
    text_path = tmp_path / "resume.txt"
    text_path.write_text("This is not a PDF.", encoding="utf-8")

    with pytest.raises(ValueError, match="Expected a PDF file"):
        extract_text(text_path)


def test_pdf_without_extractable_text_raises_value_error(tmp_path):
    pdf_path = tmp_path / "empty.pdf"
    create_pdf(pdf_path)

    with pytest.raises(ValueError, match="No extractable text"):
        extract_text(pdf_path)
