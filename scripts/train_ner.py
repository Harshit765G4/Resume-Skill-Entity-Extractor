
import json
import random
import shutil
from pathlib import Path

import spacy
from spacy.scorer import Scorer
from spacy.training import Example
from spacy.util import minibatch


ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "data" / "annotated" / "train.jsonl"
VALIDATION_PATH = ROOT / "data" / "annotated" / "validation.jsonl"
MODEL_PATH = ROOT / "models" / "resume_ner"
BEST_MODEL_PATH = ROOT / "models" / "resume_ner_best"

LABELS = {"SKILL", "JOB_TITLE", "DEGREE", "ORGANIZATION"}
EPOCHS = 30
BATCH_SIZE = 8
SEED = 42


def load_records(nlp, path):
    records = []

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            record = json.loads(line)
            text = record["text"]
            spans = [
                (item["start"], item["end"], item["label"])
                for item in record["entities"]
            ]

            for start, end, label in spans:
                if label not in LABELS:
                    raise ValueError(
                        f"Unknown label in {path.name}, line {line_number}: {label}"
                    )
                if not 0 <= start < end <= len(text):
                    raise ValueError(
                        f"Invalid span in {path.name}, line {line_number}: "
                        f"{start}:{end}"
                    )

            doc = nlp.make_doc(text)
            records.append(
                Example.from_dict(doc, {"entities": spans})
            )

    if not records:
        raise ValueError(f"Dataset is empty: {path}")

    return records


def evaluate_model(nlp, examples):
    scorer = Scorer()
    scored_examples = []

    for example in examples:
        text = example.reference.text
        predicted = nlp(text)
        scored_examples.append(
            Example(predicted, example.reference)
        )

    return scorer.score(scored_examples)


def main():
    random.seed(SEED)

    if BEST_MODEL_PATH.exists():
        shutil.rmtree(BEST_MODEL_PATH)

    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")

    train_examples = load_records(nlp, TRAIN_PATH)
    validation_examples = load_records(nlp, VALIDATION_PATH)

    for label in sorted(LABELS):
        ner.add_label(label)

    optimizer = nlp.initialize(
        get_examples=lambda: train_examples
    )

    best_f1 = -1.0

    for epoch in range(EPOCHS):
        random.shuffle(train_examples)
        losses = {}

        for batch in minibatch(train_examples, size=BATCH_SIZE):
            nlp.update(
                batch,
                sgd=optimizer,
                drop=0.2,
                losses=losses,
            )

        scores = evaluate_model(nlp, validation_examples)
        precision = scores["ents_p"]
        recall = scores["ents_r"]
        f1 = scores["ents_f"]

        print(
            f"Epoch {epoch + 1:02}/{EPOCHS} "
            f"| Loss: {losses.get('ner', 0.0):.4f} "
            f"| Val P: {precision:.4f} "
            f"| Val R: {recall:.4f} "
            f"| Val F1: {f1:.4f}"
        )

        if f1 > best_f1:
            best_f1 = f1
            nlp.to_disk(BEST_MODEL_PATH)
            print(f"  Saved new best model (validation F1: {best_f1:.4f})")

    if MODEL_PATH.exists():
        shutil.rmtree(MODEL_PATH)

    shutil.copytree(BEST_MODEL_PATH, MODEL_PATH)

    print(f"\nBest validation F1: {best_f1:.4f}")
    print(f"Best model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
