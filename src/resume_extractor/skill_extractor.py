import re


SKILL_TAXONOMY = {
    "Python": ["python"],
    "C++": ["c++", "cpp"],
    "Java": ["java"],
    "SQL": ["sql", "structured query language"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "NLP": ["natural language processing", "nlp"],
    "spaCy": ["spacy"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs"],
    "MongoDB": ["mongodb"],
    "MySQL": ["mysql"],
    "Docker": ["docker"],
    "Git": ["git"],
    "AWS": ["aws", "amazon web services"],
}


def extract_skills(text: str) -> list[str]:
    """Return recognized skills in canonical taxonomy form."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if not text.strip():
        return []

    found = set()

    for canonical_name, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            pattern = (
                r"(?<!\w)"
                + re.escape(alias)
                + r"(?!\w)"
            )

            if re.search(pattern, text, flags=re.IGNORECASE):
                found.add(canonical_name)
                break

    # Return skills in a stable, predictable order.
    return [
        skill
        for skill in SKILL_TAXONOMY
        if skill in found
    ]
