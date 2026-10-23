
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "data" / "annotated" / "synthetic_train.jsonl"
TRAIN_PATH = ROOT / "data" / "annotated" / "train.jsonl"
VALIDATION_PATH = ROOT / "data" / "annotated" / "validation.jsonl"

VALIDATION_FRACTION = 0.2
SEED = 42


def main():
    with SOURCE_PATH.open(encoding="utf-8") as file:
        records = [
            json.loads(line)
            for line in file
            if line.strip()
        ]

    if len(records) < 5:
        raise ValueError("At least five examples are required.")

    random.Random(SEED).shuffle(records)

    validation_count = max(
        1, round(len(records) * VALIDATION_FRACTION)
    )
    validation = records[:validation_count]
    training = records[validation_count:]

    for path, rows in (
        (TRAIN_PATH, training),
        (VALIDATION_PATH, validation),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as file:
            for row in rows:
                file.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Training examples:   {len(training)}")
    print(f"Validation examples: {len(validation)}")
    print(f"Final evaluation:    data/annotated/synthetic_eval.jsonl (unchanged)")
    print(f"Training file:       {TRAIN_PATH}")
    print(f"Validation file:     {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
