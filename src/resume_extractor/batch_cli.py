import argparse
import json
import sys
from pathlib import Path

from resume_extractor.batch_processor import process_directory


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract skills from every PDF in a directory."
    )
    parser.add_argument("input_dir", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/batch_results.json"),
        help="Output JSON path (default: reports/batch_results.json)",
    )
    args = parser.parse_args(argv)

    try:
        report = process_directory(args.input_dir)
    except NotADirectoryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"Could not write output: {exc}", file=sys.stderr)
        return 1

    print(
        f"Processed: {report['total_files']} | "
        f"Successful: {report['successful_files']} | "
        f"Failed: {report['failed_files']}"
    )
    print(f"Results saved to: {args.output}")

    return 0 if report["failed_files"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
