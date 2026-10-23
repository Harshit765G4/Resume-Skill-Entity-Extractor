import pymupdf
import pytest

from resume_extractor.batch_processor import process_directory


def create_pdf(path, text=None):
    with pymupdf.open() as document:
        page = document.new_page()
        if text:
            page.insert_text((72, 72), text)
        document.save(path)


def test_process_directory_handles_success_and_failure(tmp_path):
    input_dir = tmp_path / "resumes"
    input_dir.mkdir()

    create_pdf(
        input_dir / "candidate_a.pdf",
        "Python developer with TensorFlow experience.",
    )
    create_pdf(input_dir / "candidate_b.pdf")

    report = process_directory(input_dir)

    assert report["total_files"] == 2
    assert report["successful_files"] == 1
    assert report["failed_files"] == 1

    first, second = report["results"]

    assert first["source_file"] == "candidate_a.pdf"
    assert first["status"] == "success"
    assert first["skills"] == ["Python", "TensorFlow"]

    assert second["source_file"] == "candidate_b.pdf"
    assert second["status"] == "error"


def test_process_directory_rejects_missing_directory(tmp_path):
    with pytest.raises(NotADirectoryError):
        process_directory(tmp_path / "missing")
