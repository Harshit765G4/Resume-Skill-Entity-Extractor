from pathlib import Path

from resume_extractor.pdf_parser import extract_text
from resume_extractor.skill_extractor import extract_skills


def extract_resume(pdf_path: str | Path) -> dict:
    """Extract text from a resume PDF and identify recognized skills.

    Args:
        pdf_path: Path to the resume PDF.

    Returns:
        A dictionary containing the filename and recognized skills.

    Raises:
        FileNotFoundError: If the PDF does not exist.
        ValueError: If the PDF is invalid for extraction.
        RuntimeError: If the PDF cannot be read.
    """
    path = Path(pdf_path)
    text = extract_text(path)
    skills = extract_skills(text)

    return {
        "source_file": path.name,
        "skills": skills,
    }
