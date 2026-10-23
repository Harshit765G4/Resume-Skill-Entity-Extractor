import pytest

from resume_extractor.skill_extractor import extract_skills


def test_extracts_and_normalizes_skills():
    text = (
        "Experienced in PYTHON, sklearn, "
        "machine learning and TensorFlow."
    )

    assert extract_skills(text) == [
        "Python",
        "Machine Learning",
        "TensorFlow",
        "Scikit-learn",
    ]


def test_does_not_match_partial_words():
    assert extract_skills("I enjoy learning and gitters.") == []


def test_normalizes_aliases_without_duplicates():
    text = "Python, python, and PYTHON"

    assert extract_skills(text) == ["Python"]


def test_returns_empty_list_for_empty_text():
    assert extract_skills("") == []
    assert extract_skills("   ") == []


def test_rejects_non_string_input():
    with pytest.raises(TypeError, match="text must be a string"):
        extract_skills(None)
