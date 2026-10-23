from pathlib import Path

from resume_extractor.pipeline import extract_resume


def process_directory(input_dir: str | Path) -> dict:
    """Process all PDF files directly inside a directory."""
    directory = Path(input_dir)

    if not directory.is_dir():
        raise NotADirectoryError(
            f"Input directory not found: {directory}"
        )

    pdf_files = sorted(
        path for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    results = []

    for pdf_path in pdf_files:
        try:
            result = extract_resume(pdf_path)
            results.append({
                **result,
                "status": "success",
            })
        except (ValueError, RuntimeError, OSError) as exc:
            results.append({
                "source_file": pdf_path.name,
                "skills": [],
                "status": "error",
                "error": str(exc),
            })

    successful = sum(
        result["status"] == "success" for result in results
    )

    return {
        "input_directory": str(directory.resolve()),
        "total_files": len(results),
        "successful_files": successful,
        "failed_files": len(results) - successful,
        "results": results,
    }
