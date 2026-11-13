
import argparse
import json
from pathlib import Path

import spacy
from spacy.scorer import Scorer
from spacy.training import Example


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a trained spaCy resume NER model."
    )

    parser.add_argument(
        "--model",
        type=Path,
        default=ROOT / "models" / "resume_ner",
        help="Path to the trained spaCy model directory.",
    )

    parser.add_argument(
        "--data",
        type=Path,
        default=ROOT / "data" / "annotated" / "synthetic_eval.jsonl",
        help="Path to the evaluation JSONL dataset.",
    )

    args = parser.parse_args()

    # Resolve model path
    model_path = args.model
    if not model_path.is_absolute():
        model_path = ROOT / model_path

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model not found: {model_path}"
        )

    # Resolve evaluation dataset path
    eval_path = args.data
    if not eval_path.is_absolute():
        eval_path = ROOT / eval_path

    if not eval_path.is_file():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {eval_path}"
        )

    # Load model
    nlp = spacy.load(model_path)

    examples = []

    with eval_path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            record = json.loads(line)
            text = record["text"]

            # Create the gold-standard annotation
            gold = Example.from_dict(
                nlp.make_doc(text),
                {
                    "entities": [
                        (
                            item["start"],
                            item["end"],
                            item["label"],
                        )
                        for item in record["entities"]
                    ]
                },
            )

            # Run model prediction
            predicted = nlp(text)

            # Add prediction and reference to evaluation
            examples.append(
                Example(predicted, gold.reference)
            )

            # Display predictions
            print(f"\nText: {text}")
            print("Predicted entities:")

            if predicted.ents:
                for entity in predicted.ents:
                    print(
                        f"  {entity.text:<30} {entity.label_}"
                    )
            else:
                print("  (none)")

    if not examples:
        raise ValueError(
            "Evaluation dataset is empty."
        )

    # Calculate evaluation metrics
    scores = Scorer().score(examples)

    print("\n" + "=" * 55)
    print("NER EVALUATION RESULTS")
    print("=" * 55)

    print(f"Evaluation dataset : {eval_path.name}")
    print(f"Model              : {model_path.name}")
    print(f"Number of examples : {len(examples)}")

    print("\n--- Overall entity-level evaluation ---")
    print(f"Precision : {scores['ents_p']:.4f}")
    print(f"Recall    : {scores['ents_r']:.4f}")
    print(f"F1 score  : {scores['ents_f']:.4f}")

    print("\n--- Per-label evaluation ---")

    per_type = scores.get("ents_per_type", {})

    for label in (
        "SKILL",
        "JOB_TITLE",
        "DEGREE",
        "ORGANIZATION",
    ):
        metrics = per_type.get(label, {})

        print(
            f"{label:<15} "
            f"P={metrics.get('p', 0.0):.4f}  "
            f"R={metrics.get('r', 0.0):.4f}  "
            f"F1={metrics.get('f', 0.0):.4f}"
        )

    print("=" * 55)


if __name__ == "__main__":
    main()
