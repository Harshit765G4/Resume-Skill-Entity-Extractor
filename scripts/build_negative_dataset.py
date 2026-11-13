
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "annotated"

OUTPUT_PATH = DATA_DIR / "synthetic_negative_review.jsonl"

SOURCE_FILES = [
    "synthetic_train.jsonl",
    "synthetic_eval.jsonl",
    "realistic_eval.jsonl",
]

# New sentences without explicit SKILL, JOB_TITLE,
# DEGREE, or ORGANIZATION entities.
NEGATIVE_SENTENCES = [
    "The team completed the assigned work ahead of schedule.",
    "The candidate demonstrated strong problem-solving abilities.",
    "The project involved reviewing several business requirements.",
    "The student completed multiple practical assignments.",
    "The company expanded its operations into new markets.",
    "The applicant has experience working in collaborative environments.",
    "The department organized a technical knowledge-sharing session.",
    "The system processes large volumes of information.",
    "The candidate participated in several academic activities.",
    "The team improved the overall workflow.",
    "The organization provides services to multiple clients.",
    "The report contains an overview of project activities.",
    "The applicant completed a postgraduate qualification.",
    "The company is recruiting for several open positions.",
    "The student received recognition for academic performance.",
    "The project focused on improving operational efficiency.",
    "The candidate has experience managing multiple responsibilities.",
    "The department reviewed its internal processes.",
    "The team conducted a detailed performance assessment.",
    "The applicant participated in extracurricular activities.",
    "The company opened a new regional office.",
    "The candidate successfully completed the assigned tasks.",
    "The report summarizes the findings of the study.",
    "The organization supports professional development activities.",
    "The project was completed within the planned timeline.",
    "The student participated in a university-level competition.",
    "The team evaluated several possible solutions.",
    "The applicant demonstrated effective communication abilities.",
    "The company improved its customer support process.",
    "The candidate worked on multiple academic assignments.",
]


def normalize(text):
    return " ".join(text.casefold().split())


def load_existing_texts():
    existing = set()

    for filename in SOURCE_FILES:
        path = DATA_DIR / filename

        if not path.exists():
            raise FileNotFoundError(path)

        with path.open(encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    record = json.loads(line)
                    existing.add(normalize(record["text"]))

    return existing


def build_dataset():
    existing_texts = load_existing_texts()
    generated_texts = set()
    records = []

    for text in NEGATIVE_SENTENCES:
        normalized = normalize(text)

        if normalized in existing_texts:
            print(f"Skipped existing sentence: {text}")
            continue

        if normalized in generated_texts:
            print(f"Skipped duplicate sentence: {text}")
            continue

        records.append({
            "text": text,
            "entities": []
        })

        generated_texts.add(normalized)

    return records


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    records = build_dataset()

    if not records:
        raise ValueError("No new negative examples were generated.")

    # Exclusive creation: never overwrite an existing review file.
    with OUTPUT_PATH.open(
        "x",
        encoding="utf-8",
        newline="\n"
    ) as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Generated negative examples: {len(records)}")
    print(f"All examples have empty entity lists.")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
