import pymupdf
import pytest

from resume_extractor.pipeline import extract_resume


def create_resume_pdf(path, text):
    """Create a synthetic resume PDF for testing."""
    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((72, 72), text)
        document.save(path)


def test_extract_resume_returns_structured_skills(tmp_path):
    pdf_path = tmp_path / "sample_resume.pdf"

    create_resume_pdf(
        pdf_path,
        "Python developer with TensorFlow and machine learning experience.",
    )

    result = extract_resume(pdf_path)

    assert result == {
        "source_file": "sample_resume.pdf",
        "skills": ["Python", "Machine Learning", "TensorFlow"],
    }


def test_extract_resume_propagates_missing_file_error(tmp_path):
    missing_path = tmp_path / "missing_resume.pdf"

    with pytest.raises(FileNotFoundError):
        extract_resume(missing_path)


def test_extract_resume_rejects_pdf_without_text(tmp_path):
    pdf_path = tmp_path / "empty_resume.pdf"

    with pymupdf.open() as document:
        document.new_page()
        document.save(pdf_path)

    with pytest.raises(ValueError, match="No extractable text"):
        extract_resume(pdf_path)
