
import argparse
import json
from pathlib import Path

import spacy
from spacy.scorer import Scorer
from spacy.training import Example


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "resume_ner"


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate the trained resume NER model."
    )

    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "data" / "annotated" / "synthetic_eval.jsonl",
        help="Path to the evaluation JSONL dataset.",
    )

    args = parser.parse_args()
    eval_path = args.data

    if not eval_path.is_absolute():
        eval_path = ROOT / eval_path

    if not eval_path.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {eval_path}"
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    nlp = spacy.load(MODEL_PATH)
    examples = []

    with eval_path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = json.loads(line)
            text = record["text"]

            gold = Example.from_dict(
                nlp.make_doc(text),
                {
                    "entities": [
                        (item["start"], item["end"], item["label"])
                        for item in record["entities"]
                    ]
                },
            )

            predicted = nlp(text)
            examples.append(Example(predicted, gold.reference))

            print(f"\nText: {text}")
            print("Predicted entities:")

            if predicted.ents:
                for entity in predicted.ents:
                    print(f"  {entity.text:<30} {entity.label_}")
            else:
                print("  (none)")

    if not examples:
        raise ValueError("Evaluation dataset is empty.")

    scores = Scorer().score(examples)

    print(f"\nEvaluation dataset: {eval_path.name}")
    print(f"Number of examples: {len(examples)}")

    print("\n--- Overall entity-level evaluation ---")
    print(f"Precision: {scores['ents_p']:.4f}")
    print(f"Recall:    {scores['ents_r']:.4f}")
    print(f"F1 score:  {scores['ents_f']:.4f}")

    print("\n--- Per-label evaluation ---")

    per_type = scores.get("ents_per_type", {})

    for label in ("SKILL", "JOB_TITLE", "DEGREE", "ORGANIZATION"):
        metrics = per_type.get(label, {})
        print(
            f"{label:<15} "
            f"P={metrics.get('p', 0.0):.4f}  "
            f"R={metrics.get('r', 0.0):.4f}  "
            f"F1={metrics.get('f', 0.0):.4f}"
        )


if __name__ == "__main__":
    main()
