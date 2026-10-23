import argparse
import json
import sys
from pathlib import Path

from resume_extractor.pipeline import extract_resume


def main(argv: list[str] | None = None) -> int:
    """Run the resume extractor from the command line."""
    parser = argparse.ArgumentParser(
        description="Extract recognized skills from a resume PDF."
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to the resume PDF",
    )
    args = parser.parse_args(argv)

    try:
        result = extract_resume(args.pdf_path)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
