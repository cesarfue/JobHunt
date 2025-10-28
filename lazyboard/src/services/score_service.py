import json
import re
from pathlib import Path
from typing import List, Optional

DEFAULT_SKILL_KEYS = ["main", "secondary"]
DEFAULT_PENALTIES = [
    "senior",
    "lead",
    "expert",
    "chef",
    "manager",
    "head",
    "principal",
    "staff",
    "qa",
    ".net",
    "c#",
]


def load_resume() -> dict:
    resume_path = (
        Path(__file__).resolve().parent.parent.parent.parent
        / "resume/public/resume.json"
    )
    try:
        with open(resume_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading resume.json: {e}")
        return {}


def extract_skills(
    resume: dict, skill_keys: List[str] = DEFAULT_SKILL_KEYS
) -> List[str]:
    skills = []
    for key in skill_keys:
        skills += [
            skill["name"].lower()
            for skill in resume.get("resume", {}).get("hard_skills", {}).get(key, [])
        ]
    return skills


def has_match(text: str, skills: List[str]) -> bool:
    text = text.lower()
    for skill in skills:
        parts = re.split(r"[/\s\-]+", skill.lower())
        for part in parts:
            if len(part) >= 3 and part in text:
                return True
    return False


def has_penalty(text: str, penalties: List[str] = DEFAULT_PENALTIES) -> bool:
    text = text.lower()
    return any(kw.lower() in text for kw in penalties)


def retrieve_job_score(
    job_title: str = "",
    job_description: str = "",
    skills: Optional[List[str]] = None,
    penalties: List[str] = DEFAULT_PENALTIES,
) -> float:
    text = f"{job_title} {job_description}".lower()
    if skills is None:
        resume = load_resume()
        skills = extract_skills(resume)

    match = has_match(text, skills)
    penalty = has_penalty(text, penalties)

    if match and not penalty:
        return 1.0
    elif penalty:
        return 0.0
    else:
        return 0.5
