# Resume Skill & Entity Extractor

An NLP-based resume parsing system that extracts technical skills from PDF resumes using a configurable skill taxonomy and experiments with custom Named Entity Recognition (NER) using spaCy.

The experimental NER model identifies four entity types:

- `SKILL`
- `JOB_TITLE`
- `DEGREE`
- `ORGANIZATION`

> **Project status:** Core PDF extraction, taxonomy-based skill matching, CLI, batch processing, dataset validation, and custom NER training are implemented. The selected NER checkpoint has completed preliminary evaluation on small synthetic datasets. Further validation on diverse, independently sourced resumes is required before production use.

## Features

- **PDF text extraction:** Extracts selectable text from PDF files using PyMuPDF.
- **Skill extraction:** Matches technical skills and aliases against a configurable taxonomy.
- **Custom NER:** Trains a spaCy model to identify skills, job titles, degrees, and organizations.
- **Single-resume CLI:** Processes individual PDF resumes and returns structured JSON.
- **Batch processing:** Processes multiple PDFs and reports successful and failed files.
- **Dataset tooling:** Builds synthetic annotations, validates entity spans, and creates training/validation splits.
- **NER evaluation:** Reports entity-level precision, recall, and F1, including per-entity metrics.
- **Automated tests:** Tests PDF parsing, skill matching, pipeline behavior, CLI, and batch processing.

## Architecture

```text
                  PDF Resume
                      |
                      v
              PDF Text Extraction
                   (PyMuPDF)
                      |
                      v
              Resume Processing
                   Pipeline
                      |
                      v
              Skill Taxonomy Matcher
                      |
                      v
              Structured JSON Output


          Experimental NER Workflow
                      |
                      v
             Annotated JSONL Dataset
                      |
                      v
              Dataset Validation
                      |
                      v
              Train / Validation Split
                      |
                      v
                spaCy NER Training
                      |
                      v
               NER Model Checkpoint
                      |
                      v
              Independent Evaluation
```

The taxonomy-based matcher is the current primary extraction pipeline. The custom spaCy NER model is a separate experimental component and is not yet integrated into the primary PDF extraction pipeline.

## Technology Stack

- Python 3.11+
- spaCy 3.8
- PyMuPDF
- pytest
- JSON / JSONL
- Regular expressions
- Git and GitHub

## Project Structure

```text
resume-skill-entity-extractor/
├── data/
│   └── annotated/
│       ├── README.md
│       ├── synthetic_train.jsonl
│       ├── synthetic_eval.jsonl
│       └── realistic_eval.jsonl
├── models/
│   └── resume_ner_final/       # Locally generated model checkpoint
├── reports/
├── scripts/
│   ├── build_synthetic_dataset.py
│   ├── evaluate_ner.py
│   ├── split_dataset.py
│   ├── train_ner.py
│   └── validate_annotations.py
├── src/
│   └── resume_extractor/
│       ├── batch_cli.py
│       ├── batch_processor.py
│       ├── cli.py
│       ├── pdf_parser.py
│       ├── pipeline.py
│       └── skill_extractor.py
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Usage

### Extract skills from a PDF

```powershell
python -m resume_extractor.cli path\to\resume.pdf
```

The CLI prints JSON containing the source filename and recognized skills.

### Process multiple PDF resumes

```powershell
python -m resume_extractor.batch_cli .\data\raw\demo --output .\reports\batch_results.json
```

The batch command generates a JSON report containing per-file status and aggregate success/failure counts.

### Run automated tests

```powershell
python -m pytest -q
```

## Experimental NER Model

### Entity labels

| Label | Description |
|---|---|
| `SKILL` | Technical skills and technologies |
| `JOB_TITLE` | Professional roles and job titles |
| `DEGREE` | Academic qualifications |
| `ORGANIZATION` | Company and organization names |

### Training workflow

Generate and validate the training dataset:

```powershell
python .\scripts\build_synthetic_dataset.py
python .\scripts\validate_annotations.py
```

Create the training/validation split:

```powershell
python .\scripts\split_dataset.py
```

Train the NER model:

```powershell
python .\scripts\train_ner.py
```

### Evaluate the selected checkpoint

```powershell
python .\scripts\evaluate_ner.py --model models/resume_ner_final --data data/annotated/synthetic_eval.jsonl

python .\scripts\evaluate_ner.py --model models/resume_ner_final --data data/annotated/realistic_eval.jsonl
```

The selected checkpoint is stored locally at:

```text
models/resume_ner_final/
```

Model artifacts and generated data splits are excluded from version control. Regenerate them using the training scripts or retain the local checkpoint for evaluation.

## NER Evaluation Results

The selected checkpoint was evaluated on two separate datasets.

### Overall results

| Metric | Synthetic Evaluation | Independently Authored Synthetic Evaluation |
|---|---:|---:|
| Number of examples | 4 | 8 |
| Precision | 1.0000 | 0.9310 |
| Recall | 0.9091 | 1.0000 |
| **F1 Score** | **0.9524** | **0.9643** |

### Per-entity F1 scores

| Entity | Synthetic Evaluation | Independently Authored Evaluation |
|---|---:|---:|
| SKILL | 1.0000 | 1.0000 |
| JOB_TITLE | 0.8000 | 0.8571 |
| DEGREE | 1.0000 | 1.0000 |
| ORGANIZATION | 1.0000 | 1.0000 |

### Evaluation observations

- The model correctly identifies the evaluated skills, degrees, and organizations in both datasets.
- Job title extraction remains an area for improvement.
- The model incorrectly identifies phrases such as `business data` and `machine learning workflows` as job titles in the independently authored evaluation set.
- The evaluation datasets are small and synthetic. These results are preliminary benchmarks, not estimates of performance on real-world resumes.

## Model Experimentation

Two training approaches were compared:

1. **Original checkpoint:** Trained on the initial annotated dataset. Achieved an F1 score of 0.9524 on the synthetic evaluation set and 0.9643 on the independently authored synthetic evaluation set.
2. **Negative-example experiment:** Additional negative examples were introduced to reduce false-positive entity predictions. The resulting model did not improve overall evaluation performance, particularly for degree and organization extraction.

The original checkpoint was retained as the selected model because it achieved better overall results on both evaluation datasets.

## Current Limitations

- The annotated dataset is small and primarily synthetic.
- The evaluation sets contain only 4 and 8 examples respectively.
- Independently authored synthetic examples are not a substitute for a representative real-world test set.
- Job title extraction can produce false positives for phrases that resemble professional roles.
- Skill matching only recognizes entries and aliases in the configured taxonomy.
- Scanned PDFs without an OCR text layer are not supported by the current extraction pipeline.
- The custom NER model has not been validated across a sufficiently diverse collection of real resumes.
- The experimental NER model is not yet integrated into the primary PDF extraction pipeline.

## Roadmap

- Expand the independently authored evaluation dataset.
- Collect appropriately permissioned and anonymized resume examples.
- Improve job title boundary detection and false-positive handling.
- Compare custom NER against rule-based extraction.
- Add work experience and education extraction.
- Improve scanned PDF support through OCR.
- Integrate NER into the resume processing pipeline.
- Add a REST API or web interface.
- Add reproducible evaluation and CI checks.

## Responsible Data Use

Use synthetic, public-domain, or properly permissioned resume data. Resumes may contain sensitive personal information. Avoid committing real resumes, personal identifiers, credentials, or other sensitive information to the repository.

## License

No license has been selected yet. Add an appropriate license before distributing the project for reuse.
