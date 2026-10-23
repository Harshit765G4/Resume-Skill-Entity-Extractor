# Resume NER Annotation Guidelines

## Purpose

Create labeled examples for training and evaluating a
resume-specific Named Entity Recognition model.

## Entity labels

- SKILL: Explicitly mentioned technical or professional skills.
- JOB_TITLE: A role or position held or sought by a person.
- DEGREE: A named academic degree or qualification.
- ORGANIZATION: An explicitly named employer or institution.

## Annotation rules

1. Label only text explicitly present in the source.
2. Preserve the exact original text and character offsets.
3. Do not infer skills from job titles.
4. Do not label generic words as skills without context.
5. Annotate entity spans consistently across documents.
6. Keep training and evaluation documents separate.
7. Use synthetic or permissioned data; protect personal information.
8. Record ambiguous cases for review instead of guessing.

## Evaluation

Evaluate entity-level precision, recall and F1 on held-out
documents that were not used for training or model selection.
