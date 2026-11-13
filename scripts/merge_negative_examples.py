
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "annotated"

SOURCE_PATH = DATA_DIR / "synthetic_train.jsonl"
NEGATIVE_PATH = DATA_DIR / "synthetic_negative_review.jsonl"
BACKUP_PATH = DATA_DIR / "synthetic_train_before_negative_merge.jsonl.bak"
TEMP_PATH = DATA_DIR / "synthetic_train.merge.tmp"

EVALUATION_FILES = [
    DATA_DIR / "synthetic_eval.jsonl",
    DATA_DIR / "realistic_eval.jsonl",
]


def load_jsonl(path):
    with path.open(encoding="utf-8") as file:
        return [
            json.loads(line)
            for line in file
            if line.strip()
        ]


def normalize(text):
    return " ".join(text.casefold().split())


def main():
    for path in [SOURCE_PATH, NEGATIVE_PATH, *EVALUATION_FILES]:
        if not path.exists():
            raise FileNotFoundError(path)

    if BACKUP_PATH.exists():
        raise FileExistsError(
            f"Backup already exists: {BACKUP_PATH}"
        )

    if TEMP_PATH.exists():
        raise FileExistsError(
            f"Temporary file already exists: {TEMP_PATH}"
        )

    original = load_jsonl(SOURCE_PATH)
    negatives = load_jsonl(NEGATIVE_PATH)
    evaluation_records = []

    for path in EVALUATION_FILES:
        evaluation_records.extend(load_jsonl(path))

    if len(negatives) != 30:
        raise ValueError(
            f"Expected 30 negative examples, found {len(negatives)}."
        )

    if any(record.get("entities") != [] for record in negatives):
        raise ValueError(
            "Every proposed negative example must have an empty entities list."
        )

    existing_texts = {
        normalize(record["text"])
        for record in original + evaluation_records
    }

    generated_texts = set()

    for record in negatives:
        text = normalize(record["text"])

        if text in existing_texts:
            raise ValueError(
                f"Duplicate against existing data or evaluation: "
                f"{record['text']}"
            )

        if text in generated_texts:
            raise ValueError(
                f"Duplicate negative example: {record['text']}"
            )

        generated_texts.add(text)

    merged = original + negatives

    original_bytes = SOURCE_PATH.read_bytes()

    # Preserve the original source without overwriting any backup.
    with BACKUP_PATH.open("xb") as backup:
        backup.write(original_bytes)

    try:
        with TEMP_PATH.open(
            "x", encoding="utf-8", newline="\n"
        ) as file:
            for record in merged:
                file.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )

        TEMP_PATH.replace(SOURCE_PATH)

    except Exception:
        TEMP_PATH.unlink(missing_ok=True)
        raise

    negative_count = sum(
        not record["entities"] for record in merged
    )

    print(f"Original examples: {len(original)}")
    print(f"Added negatives:   {len(negatives)}")
    print(f"Final examples:    {len(merged)}")
    print(f"Positive examples: {len(merged) - negative_count}")
    print(f"Negative examples: {negative_count}")
    print(
        f"Negative proportion: "
        f"{negative_count / len(merged):.1%}"
    )
    print(f"Backup saved: {BACKUP_PATH}")
    print("Evaluation datasets were not modified.")


if __name__ == "__main__":
    main()
