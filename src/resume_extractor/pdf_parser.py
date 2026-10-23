from pathlib import Path

import pymupdf


def extract_text(pdf_path: str | Path) -> str:
    """Extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF document.

    Returns:
        Extracted text from all pages, joined with newlines.

    Raises:
        FileNotFoundError: If the PDF does not exist.
        ValueError: If the file is not a PDF or contains no extractable text.
        RuntimeError: If the PDF cannot be opened or read.
    """
    path = Path(pdf_path)

    if not path.is_file():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, received: {path.suffix}")

    try:
        with pymupdf.open(path) as document:
            text = "\n".join(page.get_text() for page in document)
    except Exception as exc:
        raise RuntimeError(f"Failed to read PDF: {path}") from exc

    text = text.strip()

    if not text:
        raise ValueError(
            "No extractable text found. The PDF may be empty or scanned."
        )

    return text
