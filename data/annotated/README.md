# Resume NER Annotation Guidelines

## Purpose

Create high-quality labeled examples for training and evaluating a resume-specific Named Entity Recognition (NER) model.

## Entity Labels

- **SKILL:** Explicitly mentioned technical or professional skills, tools, frameworks, platforms, methodologies, or competencies.
- **JOB_TITLE:** A professional role, designation, or position held or sought by a person.
- **DEGREE:** A named academic degree or formal educational qualification.
- **ORGANIZATION:** An explicitly named employer, educational institution, or other organization.

## Annotation Rules

1. Annotate only information explicitly present in the source text.
2. Preserve the exact original text and character offsets.
3. Use complete entity spans whenever the full name or title is present.
4. Do not infer skills from job titles, projects, or work experience.
5. Do not label generic words as skills without sufficient context.
6. Annotate repeated valid entity mentions wherever they occur.
7. Keep degree qualifications separate from fields of study or specializations.
8. Annotate complete organization names, including meaningful suffixes when present.
9. Do not assign multiple labels to the same text span unless explicitly supported by the annotation schema.
10. Annotate entities consistently across different documents.
11. Leave ambiguous cases for manual review rather than guessing.
12. Keep training, validation, and independent evaluation documents separate.
13. Use synthetic or permissioned data and protect personal information.

## Negative Examples

Negative examples must contain no valid entities from the four supported labels.

Examples may include technical-sounding phrases, generic responsibilities, and contextual words that should not be classified as entities.

Do not label an example as negative if it contains an explicitly identifiable entity.

## Entity Boundary Conventions

- Annotate complete job titles, such as "Machine Learning Engineer".
- Annotate complete named degrees, such as "Bachelor of Technology".
- Do not annotate a specialization as a degree by itself.
- Annotate the full organization name when explicitly available.
- Annotate explicit skill names without adding surrounding descriptive words.

## Dataset Quality Checks

Before accepting an annotation:

- Verify that the start and end offsets match the original text.
- Verify that the extracted text exactly matches the annotated entity.
- Confirm that the label belongs to the supported label set.
- Check that no valid entity has been missed.
- Confirm that negative examples contain no supported entities.
- Review ambiguous examples manually.

## Evaluation

Evaluate entity-level precision, recall, and F1 on held-out documents that were not used for training, hyperparameter tuning, or model selection.

Report overall and per-entity metrics. Document dataset size, class distribution, limitations, and evaluation methodology.

Synthetic evaluation results must not be presented as evidence of real-world performance.