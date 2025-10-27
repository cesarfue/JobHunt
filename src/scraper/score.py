import json
import re
from pathlib import Path


def retrieve_job_score(job_title: str = "", job_description: str = "") -> float:
    resume_path = Path(__file__).resolve().parent.parent / "resume/public/resume.json"

    try:
        with open(resume_path, "r", encoding="utf-8") as f:
            resume = json.load(f)
    except Exception as e:
        print(f"Error loading resume.json: {e}")
        return 0.5

    def get_skills(key: str):
        return [
            skill["name"].lower()
            for skill in resume["resume"]["hard_skills"].get(key, [])
        ]

    main_skills = get_skills("main")
    print(main_skills)
    secondary_skills = get_skills("secondary")
    print(secondary_skills)
    all_skills = main_skills + secondary_skills

    text = f"{job_title} {job_description}".lower()

    match = False
    for skill in all_skills:
        parts = re.split(r"[/\s\-]+", skill.lower())
        for part in parts:
            if len(part) >= 3 and part in text:
                match = True
                break
        if match:
            break

    penalties = [
        "senior",
        "lead",
        "expert",
        "chef",
        "manager",
        "head",
        "principal",
        "staff",
        "qa",
    ]
    penalty = any(kw in text for kw in penalties)
    print(f"job : {text} got match : {match} and penalty : {penalty}")

    if match and not penalty:
        score = 1.0
    elif penalty:
        score = 0.0
    else:
        score = 0.5

    return score
