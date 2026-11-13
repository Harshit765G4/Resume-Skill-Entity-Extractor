import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "annotated"

FILES = [
    "synthetic_eval.jsonl",
    "realistic_eval.jsonl",
]


def correct_degree_spans(records):
    corrections = 0

    for record in records:
        text = record["text"]

        for entity in record["entities"]:
            if entity["label"] != "DEGREE":
                continue

            start = entity["start"]
            end = entity["end"]
            entity_text = text[start:end]

            if entity_text.endswith(" degree"):
                new_end = end - len(" degree")
                entity["end"] = new_end
                corrections += 1

    return corrections


def main():
    for filename in FILES:
        source_path = DATA_DIR / filename
        output_path = DATA_DIR / filename.replace(
            ".jsonl", "_v2.jsonl"
        )

        if output_path.exists():
            raise FileExistsError(
                f"Refusing to overwrite existing file: {output_path}"
            )

        records = []

        with source_path.open(encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    records.append(json.loads(line))

        corrections = correct_degree_spans(records)

        with output_path.open("x", encoding="utf-8") as file:
            for record in records:
                file.write(
                    json.dumps(record, ensure_ascii=False) + "\n"
                )

        print(f"\nCreated: {output_path.name}")
        print(f"Corrections: {corrections}")


if __name__ == "__main__":
    main()