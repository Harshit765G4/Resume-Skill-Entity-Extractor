# Resume Skill & Entity Extractor

An NLP-based resume parsing system that extracts technical skills from PDF resumes and experiments with custom Named Entity Recognition (NER) to identify skills, job titles, degrees, and organizations.

> **Project status:** Early development. The PDF extraction, skill-matching pipeline, CLI, batch processing, and initial NER training workflow are implemented. The custom NER model is experimental and has not yet been validated on a sufficiently large, representative resume dataset.

## Features

- **PDF text extraction:** Extracts selectable text from PDF files using PyMuPDF.
- **Skill extraction:** Matches known skill names and aliases against a configurable taxonomy.
- **Custom NER:** Trains a spaCy model to recognize `SKILL`, `JOB_TITLE`, `DEGREE`, and `ORGANIZATION`.
- **Single-resume CLI:** Returns extracted skills as JSON.
- **Batch processing:** Processes PDFs in a directory and reports successful and failed files.
- **Dataset tooling:** Generates synthetic annotations, validates entity spans, and splits data into training and validation sets.
- **Automated tests:** Covers PDF parsing, skill matching, pipeline behavior, CLI, and batch processing.

## Architecture

```text
PDF Resume
    |
    v
PDF Text Extraction (PyMuPDF)
    |
    v
Resume Processing Pipeline
    |
    +--> Skill Taxonomy Matcher
    |
    +--> Custom spaCy NER (experimental)
    |
    v
Structured Results / JSON
```

The current production-style pipeline uses taxonomy-based skill matching. The custom NER model is trained and evaluated through separate scripts and is still experimental.

## Technology Stack

- Python 3.11+
- spaCy 3.8
- PyMuPDF
- pytest
- JSONL for annotated training and evaluation data

## Project Structure

```text
resume-skill-entity-extractor/
├── data/
│   ├── annotated/
│   │   ├── README.md
│   │   ├── synthetic_train.jsonl
│   │   └── synthetic_eval.jsonl
│   ├── processed/
│   └── raw/
├── models/
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

### Extract skills from one PDF

```powershell
python -m resume_extractor.cli path\to\resume.pdf
```

The CLI prints JSON containing the source filename and recognized skills.

### Process a directory of PDFs

```powershell
python -m resume_extractor.batch_cli .\data\raw\demo --output .\reports\batch_results.json
```

The batch command writes a JSON report containing per-file status and aggregate success/failure counts.

### Run the test suite

```powershell
python -m pytest -q
```

### Train the custom NER model

Generate and validate the synthetic dataset:

```powershell
python .\scripts\build_synthetic_dataset.py
python .\scripts\validate_annotations.py
```

Create the training/validation split and train the model:

```powershell
python .\scripts\split_dataset.py
python .\scripts\train_ner.py
```

Evaluate against the separate evaluation file:

```powershell
python .\scripts\evaluate_ner.py
```

Training produces a local model under `models/`. Model artifacts and generated data splits are intentionally excluded from version control; regenerate them using the scripts above.

## Current Limitations

- The NER dataset is synthetic and small.
- The evaluation dataset currently contains only four examples, so its metrics are not reliable estimates of real-world performance.
- Synthetic training and validation examples may contain similar wording.
- Skill matching only recognizes entries and aliases in the configured taxonomy.
- Scanned PDFs without an OCR text layer are not supported by the current text-extraction pipeline.
- The custom NER model has not yet been validated on a sufficiently diverse collection of real or independently authored resume examples.

## Roadmap

- Expand the independently authored evaluation dataset.
- Improve per-entity precision, recall, F1, and error analysis.
- Compare custom NER against a rule-based baseline.
- Add robust experience and education extraction.
- Improve handling of scanned PDFs and OCR.
- Add a REST API or user interface.
- Add reproducible model evaluation and CI checks.

## Responsible Data Use

Use synthetic, public-domain, or properly permissioned resume data. Resumes can contain personal information; avoid committing real resumes, personal identifiers, credentials, or other sensitive data to the repository.

## License

No license has been selected yet. Add a license before distributing the project for reuse.
