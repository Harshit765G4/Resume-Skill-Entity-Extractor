# Experiment 02: Impact of Negative Examples on Resume NER

## 1. Objective

Evaluate whether adding negative examples to the synthetic training dataset improves the performance of the resume-specific spaCy NER model.

## 2. Dataset Changes

| Metric | Before | After |
|---|---:|---:|
| Total training records | 138 | 168 |
| Positive examples | 129 | 129 |
| Negative examples | 9 | 39 |
| Negative-example ratio | 6.5% | 23.2% |

The updated dataset was validated, and the train-validation split was regenerated using random seed 42.

- Training records: 134
- Validation records: 34
- Training negative ratio: 23.1%
- Validation negative ratio: 23.5%

## 3. Training Configuration

- Framework: spaCy
- Architecture: Blank English pipeline with NER component
- Entity labels: SKILL, JOB_TITLE, DEGREE, ORGANIZATION
- Epochs: 30
- Batch size: 8
- Dropout: 0.2
- Random seed: 42
- Best validation F1: 0.8750
- Best epoch: 11 (tied with epoch 12)

## 4. Model Checkpoints

| Model | Local checkpoint |
|---|---|
| Original baseline | `models/resume_ner_final` |
| Negative-example experiment | `models/resume_ner_with_negatives` |

Both checkpoints were preserved.

## 5. Evaluation Results

### Synthetic evaluation v2

| Metric | Original | Experimental |
|---|---:|---:|
| Precision | 0.9000 | 1.0000 |
| Recall | 0.8182 | 0.9091 |
| F1 | 0.8571 | 0.9524 |

### Realistic evaluation v2

| Metric | Original | Experimental |
|---|---:|---:|
| Precision | 0.8966 | 0.9310 |
| Recall | 0.9630 | 1.0000 |
| F1 | 0.9286 | 0.9643 |

## 6. Per-Entity Results

### Realistic evaluation v2

| Entity | Original F1 | Experimental F1 |
|---|---:|---:|
| SKILL | 1.0000 | 0.9231 |
| JOB_TITLE | 0.8571 | 1.0000 |
| DEGREE | 0.6667 | 1.0000 |
| ORGANIZATION | 1.0000 | 1.0000 |

## 7. Qualitative Findings

Improvements:
- Corrected degree entity boundaries.
- Reduced incorrect JOB_TITLE predictions for generic phrases.
- Improved JOB_TITLE recognition.
- Improved DEGREE recognition.

Remaining issues:
- Person names can be incorrectly classified as SKILL.
- Generic phrases such as "machine learning workflows" can still be classified as entities.
- Skill precision decreased slightly on the realistic evaluation set.

## 8. Conclusion

The negative-example experiment achieved higher overall F1 on both corrected evaluation datasets.

The experimental checkpoint is the current preferred candidate for further testing. The original checkpoint remains preserved as the baseline.

These results are preliminary because the evaluation datasets are small and synthetic. They do not establish real-world production performance.

The combined evaluation set contains only 12 examples (4 synthetic and 8 realistic), so the observed improvements should be treated as preliminary rather than statistically conclusive.

## 9. Next Steps

1. Expand independent evaluation data.
2. Add challenging negative examples.
3. Test person-name false positives.
4. Measure per-entity precision and recall on a larger dataset.
5. Evaluate on permissioned real-world resumes.
6. Integrate the selected NER model into the PDF extraction pipeline.