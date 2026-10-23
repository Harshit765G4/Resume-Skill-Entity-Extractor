
import json
from pathlib import Path

ALLOWED_LABELS = {
    "SKILL",
    "JOB_TITLE",
    "DEGREE",
    "ORGANIZATION",
}


def validate_file(path: Path) -> int:
    count = 0

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)
            text = record["text"]
            entities = record["entities"]
            previous_end = 0

            for entity in entities:
                start = entity["start"]
                end = entity["end"]
                label = entity["label"]

                assert 0 <= start < end <= len(text), (
                    f"Invalid offsets: line {line_number}"
                )
                assert label in ALLOWED_LABELS, (
                    f"Invalid label {label!r}: line {line_number}"
                )
                assert start >= previous_end, (
                    f"Overlapping or unsorted entities: line {line_number}"
                )
                assert text[start:end].strip() == text[start:end], (
                    f"Entity has surrounding whitespace: line {line_number}"
                )

                previous_end = end

            count += 1

    return count


if __name__ == "__main__":
    files = [
        Path("data/annotated/synthetic_train.jsonl"),
        Path("data/annotated/synthetic_eval.jsonl"),
    ]

    for path in files:
        count = validate_file(path)
        print(f"{path}: {count} valid examples")

    print("Annotation validation passed.")
