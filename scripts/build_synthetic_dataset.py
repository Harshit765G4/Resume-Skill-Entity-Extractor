
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "annotated" / "synthetic_train.jsonl"

LABELS = {"SKILL", "JOB_TITLE", "DEGREE", "ORGANIZATION"}


def make_record(text, mentions):
    """Create exact character offsets from (surface, label) pairs."""
    entities = []

    for surface, label in mentions:
        if label not in LABELS:
            raise ValueError(f"Unknown label: {label}")

        if text.count(surface) != 1:
            raise ValueError(
                f"Expected '{surface}' exactly once in: {text}"
            )

        start = text.index(surface)
        entities.append({
            "start": start,
            "end": start + len(surface),
            "label": label,
        })

    entities.sort(key=lambda entity: entity["start"])

    for previous, current in zip(entities, entities[1:]):
        if previous["end"] > current["start"]:
            raise ValueError(f"Overlapping entities in: {text}")

    return {"text": text, "entities": entities}


def build_dataset():
    records = []

    # Combined resume examples: job titles, organizations and skills.
    combined = [
        (
            "Python developer at Acme Technologies.",
            [("Python", "SKILL"), ("developer", "JOB_TITLE"),
             ("Acme Technologies", "ORGANIZATION")],
        ),
        (
            "Machine Learning Engineer at Nova Labs builds models with TensorFlow.",
            [("Machine Learning Engineer", "JOB_TITLE"),
             ("Nova Labs", "ORGANIZATION"), ("TensorFlow", "SKILL")],
        ),
        (
            "Data Analyst at Northstar Analytics queries data with SQL.",
            [("Data Analyst", "JOB_TITLE"),
             ("Northstar Analytics", "ORGANIZATION"), ("SQL", "SKILL")],
        ),
        (
            "Software Engineer at Bluebird Systems deploys services with Docker.",
            [("Software Engineer", "JOB_TITLE"),
             ("Bluebird Systems", "ORGANIZATION"), ("Docker", "SKILL")],
        ),
        (
            "Cloud Engineer at Vertex Cloud works with AWS.",
            [("Cloud Engineer", "JOB_TITLE"),
             ("Vertex Cloud", "ORGANIZATION"), ("AWS", "SKILL")],
        ),
        (
            "NLP Engineer at Meridian AI builds pipelines with spaCy.",
            [("NLP Engineer", "JOB_TITLE"),
             ("Meridian AI", "ORGANIZATION"), ("spaCy", "SKILL")],
        ),
        (
            "Computer Vision Engineer at Bright Vision trains models using PyTorch.",
            [("Computer Vision Engineer", "JOB_TITLE"),
             ("Bright Vision", "ORGANIZATION"), ("PyTorch", "SKILL")],
        ),
        (
            "Backend Developer at Orbit Systems builds APIs with Python.",
            [("Backend Developer", "JOB_TITLE"),
             ("Orbit Systems", "ORGANIZATION"), ("Python", "SKILL")],
        ),
        (
            "Frontend Developer at Pixel Works builds interfaces with React.",
            [("Frontend Developer", "JOB_TITLE"),
             ("Pixel Works", "ORGANIZATION"), ("React", "SKILL")],
        ),
        (
            "Database Administrator at DataCore manages PostgreSQL databases.",
            [("Database Administrator", "JOB_TITLE"),
             ("DataCore", "ORGANIZATION"), ("PostgreSQL", "SKILL")],
        ),
        (
            "DevOps Engineer at Summit Tech maintains Git workflows.",
            [("DevOps Engineer", "JOB_TITLE"),
             ("Summit Tech", "ORGANIZATION"), ("Git", "SKILL")],
        ),
        (
            "Data Scientist at Greenfield Labs analyzes data using Pandas and NumPy.",
            [("Data Scientist", "JOB_TITLE"),
             ("Greenfield Labs", "ORGANIZATION"),
             ("Pandas", "SKILL"), ("NumPy", "SKILL")],
        ),
    ]

    for text, mentions in combined:
        records.append(make_record(text, mentions))

    # Job titles in varied contexts.
    job_titles = [
        "Backend Developer", "Frontend Developer", "Data Analyst",
        "Data Scientist", "Machine Learning Engineer",
        "Software Engineer", "Cloud Engineer", "DevOps Engineer",
        "NLP Engineer", "QA Engineer", "Database Administrator",
        "Cybersecurity Analyst",
    ]

    job_templates = [
        "Role applied for: {value}.",
        "Previously worked as a {value}.",
        "Seeking a position as a {value}.",
        "Experienced {value} with project delivery skills.",
    ]

    for index, title in enumerate(job_titles):
        template = job_templates[index % len(job_templates)]
        text = template.format(value=title)
        records.append(make_record(text, [(title, "JOB_TITLE")]))

    # Organizations in different sentence positions.
    organizations = [
        "Acme Technologies", "Northstar Analytics", "Bluebird Systems",
        "Vertex Cloud", "Meridian AI", "Bright Vision", "Orbit Systems",
        "Pixel Works", "DataCore", "Summit Tech", "Greenfield Labs",
        "Cedar Innovations",
    ]

    organization_templates = [
        "Previous employer: {value}.",
        "Worked at {value} on software projects.",
        "The candidate joined {value} after graduation.",
        "A project was completed for {value}.",
    ]

    for index, organization in enumerate(organizations):
        template = organization_templates[index % len(organization_templates)]
        text = template.format(value=organization)
        records.append(
            make_record(text, [(organization, "ORGANIZATION")])
        )

    # Named degrees and qualifications.
    degrees = [
        "B.Tech in Computer Science",
        "Bachelor of Engineering",
        "Bachelor of Science in Statistics",
        "Master of Computer Applications",
        "M.Sc. in Data Science",
        "Ph.D. in Computer Science",
        "Diploma in Information Technology",
        "Bachelor of Technology in Information Technology",
        "Master of Science in Computer Science",
        "BCA",
        "MBA in Information Systems",
        "Master of Engineering in Software Systems",
    ]

    degree_templates = [
        "Completed {value}.",
        "The candidate holds a {value} qualification.",
        "Education includes {value}.",
        "Graduated with {value}.",
    ]

    for index, degree in enumerate(degrees):
        template = degree_templates[index % len(degree_templates)]
        text = template.format(value=degree)
        records.append(make_record(text, [(degree, "DEGREE")]))

    # Skills in several contexts.
    skills = [
        "Python", "Java", "C++", "SQL", "TensorFlow",
        "PyTorch", "scikit-learn", "spaCy", "Pandas", "NumPy",
        "React", "Node.js", "MongoDB", "MySQL", "Docker",
        "Git", "AWS", "PostgreSQL", "Kubernetes", "Machine Learning",
    ]

    skill_templates = [
        "Experienced in {value}.",
        "Built projects using {value}.",
        "Technical proficiency includes {value}.",
        "Applied {value} in recent projects.",
    ]

    for index, skill in enumerate(skills):
        template = skill_templates[index % len(skill_templates)]
        text = template.format(value=skill)
        records.append(make_record(text, [(skill, "SKILL")]))

    # Detect accidental duplicate sentences.
        additional_examples = [
        (
            "Acme Technologies hired a backend developer who uses Python for automation.",
            [("Acme Technologies", "ORGANIZATION"),
             ("backend developer", "JOB_TITLE"),
             ("Python", "SKILL")],
        ),
        (
            "At Northstar Analytics, a data analyst writes SQL queries.",
            [("Northstar Analytics", "ORGANIZATION"),
             ("data analyst", "JOB_TITLE"), ("SQL", "SKILL")],
        ),
        (
            "Cloudbridge Systems employs a DevOps Engineer familiar with Kubernetes.",
            [("Cloudbridge Systems", "ORGANIZATION"),
             ("DevOps Engineer", "JOB_TITLE"),
             ("Kubernetes", "SKILL")],
        ),
        (
            "Orbit Data hired a data scientist who uses Pandas and NumPy.",
            [("Orbit Data", "ORGANIZATION"),
             ("data scientist", "JOB_TITLE"),
             ("Pandas", "SKILL"), ("NumPy", "SKILL")],
        ),
        (
            "An engineer at Cedar Innovations deployed services with Docker.",
            [("engineer", "JOB_TITLE"),
             ("Cedar Innovations", "ORGANIZATION"),
             ("Docker", "SKILL")],
        ),
        (
            "Nova Labs recruited a software engineer with spaCy experience.",
            [("Nova Labs", "ORGANIZATION"),
             ("software engineer", "JOB_TITLE"),
             ("spaCy", "SKILL")],
        ),
        (
            "A graduate completed a B.Tech in Computer Science and later used Python.",
            [("B.Tech in Computer Science", "DEGREE"),
             ("Python", "SKILL")],
        ),
        (
            "Candidate completed a Master of Science in Analytics at Westlake University.",
            [("Master of Science in Analytics", "DEGREE"),
             ("Westlake University", "ORGANIZATION")],
        ),
        (
            "Education includes a Bachelor of Engineering from Eastbrook Institute.",
            [("Bachelor of Engineering", "DEGREE"),
             ("Eastbrook Institute", "ORGANIZATION")],
        ),
        (
            "An applicant with a Diploma in Information Technology joined Summit Tech as a software engineer.",
            [("Diploma in Information Technology", "DEGREE"),
             ("Summit Tech", "ORGANIZATION"),
             ("software engineer", "JOB_TITLE")],
        ),
        (
            "After earning a Ph.D. in Computer Science, the researcher joined Deepfield AI.",
            [("Ph.D. in Computer Science", "DEGREE"),
             ("Deepfield AI", "ORGANIZATION")],
        ),
        (
            "Technical skills include C++, SQL, and Docker; the desired role is backend developer.",
            [("C++", "SKILL"), ("SQL", "SKILL"),
             ("Docker", "SKILL"),
             ("backend developer", "JOB_TITLE")],
        ),
        (
            "A Data Scientist role requires NumPy and SQL experience.",
            [("Data Scientist", "JOB_TITLE"),
             ("NumPy", "SKILL"), ("SQL", "SKILL")],
        ),
        (
            "Blue Peak Group promoted its Data Analyst to Software Engineer.",
            [("Blue Peak Group", "ORGANIZATION"),
             ("Data Analyst", "JOB_TITLE"),
             ("Software Engineer", "JOB_TITLE")],
        ),
        (
            "VantageWorks hires a cloud engineer skilled in AWS and Docker.",
            [("VantageWorks", "ORGANIZATION"),
             ("cloud engineer", "JOB_TITLE"),
             ("AWS", "SKILL"), ("Docker", "SKILL")],
        ),
        (
            "A software engineer at Cedar Grove built a web service with Node.js and MongoDB.",
            [("software engineer", "JOB_TITLE"),
             ("Cedar Grove", "ORGANIZATION"),
             ("Node.js", "SKILL"), ("MongoDB", "SKILL")],
        ),
        (
            "SQL is used by a database administrator at DataCore.",
            [("SQL", "SKILL"),
             ("database administrator", "JOB_TITLE"),
             ("DataCore", "ORGANIZATION")],
        ),
        (
            "At Vertex Cloud, a cloud engineer manages AWS deployments.",
            [("Vertex Cloud", "ORGANIZATION"),
             ("cloud engineer", "JOB_TITLE"), ("AWS", "SKILL")],
        ),
        (
            "Northstar Analytics offers a Machine Learning Engineer position requiring TensorFlow.",
            [("Northstar Analytics", "ORGANIZATION"),
             ("Machine Learning Engineer", "JOB_TITLE"),
             ("TensorFlow", "SKILL")],
        ),
        (
            "An experienced backend developer at Arcadia Software built services with MySQL and Java.",
            [("backend developer", "JOB_TITLE"),
             ("Arcadia Software", "ORGANIZATION"),
             ("MySQL", "SKILL"), ("Java", "SKILL")],
        ),
        (
            "A project portfolio lists React and Node.js; the candidate seeks a Frontend Developer role.",
            [("React", "SKILL"), ("Node.js", "SKILL"),
             ("Frontend Developer", "JOB_TITLE")],
        ),
        (
            "Python and scikit-learn were used by a data analyst at Silverline Analytics.",
            [("Python", "SKILL"), ("scikit-learn", "SKILL"),
             ("data analyst", "JOB_TITLE"),
             ("Silverline Analytics", "ORGANIZATION")],
        ),
        (
            "At Summit Tech, a cybersecurity analyst reviewed networks using Python.",
            [("Summit Tech", "ORGANIZATION"),
             ("cybersecurity analyst", "JOB_TITLE"),
             ("Python", "SKILL")],
        ),
        (
            "A junior engineer from Pinecrest Labs finished a BCA program and used Git.",
            [("engineer", "JOB_TITLE"),
             ("Pinecrest Labs", "ORGANIZATION"),
             ("BCA", "DEGREE"), ("Git", "SKILL")],
        ),
        (
            "The candidate earned an MBA in Information Systems at Broadview Group and knows MySQL.",
            [("MBA in Information Systems", "DEGREE"),
             ("Broadview Group", "ORGANIZATION"),
             ("MySQL", "SKILL")],
        ),
        (
            "Bluebird Systems is seeking a QA Engineer familiar with Docker and SQL.",
            [("Bluebird Systems", "ORGANIZATION"),
             ("QA Engineer", "JOB_TITLE"),
             ("Docker", "SKILL"), ("SQL", "SKILL")],
        ),
        (
            "A cloud engineer at Alpine Networks uses AWS, Python, and Docker.",
            [("cloud engineer", "JOB_TITLE"),
             ("Alpine Networks", "ORGANIZATION"),
             ("AWS", "SKILL"), ("Python", "SKILL"),
             ("Docker", "SKILL")],
        ),
        (
            "DataCore hired a database administrator experienced with MySQL databases.",
            [("DataCore", "ORGANIZATION"),
             ("database administrator", "JOB_TITLE"),
             ("MySQL", "SKILL")],
        ),
        (
            "Cedar Innovations hired a frontend developer who builds React applications.",
            [("Cedar Innovations", "ORGANIZATION"),
             ("frontend developer", "JOB_TITLE"),
             ("React", "SKILL")],
        ),
        (
            "A Bachelor of Science in Statistics graduate joined Meridian AI as a data analyst using Pandas.",
            [("Bachelor of Science in Statistics", "DEGREE"),
             ("Meridian AI", "ORGANIZATION"),
             ("data analyst", "JOB_TITLE"),
             ("Pandas", "SKILL")],
        ),
    ]

    for text, mentions in additional_examples:
        records.append(make_record(text, mentions))
    texts = [record["text"] for record in records]
    if len(texts) != len(set(texts)):
        raise ValueError("Duplicate training sentences found.")

    return records


def main():
    records = build_dataset()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    counts = Counter(
        entity["label"]
        for record in records
        for entity in record["entities"]
    )

    print(f"Generated {len(records)} training examples.")
    print(f"Entity counts: {dict(sorted(counts.items()))}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
