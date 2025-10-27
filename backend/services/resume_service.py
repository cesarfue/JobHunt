import json
import subprocess
from pathlib import Path

from config import Config
from services.json_helper import clean_json

SCORE_THRESHOLD = 0.3


def make_resume(openai, folder_path):
    scores = query_scores(openai)
    overrides = create_sorted_overrides(scores)
    save_overrides_file(overrides, folder_path)
    if not Config.DEBUG_MODE:
        generate_resume_pdf(folder_path)


def query_scores(openai):
    score_prompt = """
## Instructions
À partir de l'offre d'emploi ci-dessous, adapte le score de chacun des éléments de mon CV en JSON en fonction de sa pertinence, sur une note de 0 à 1.
Ne réponds que par le JSON valide, sans aucune autre information.
- 0,75-1.00 : Très pertinent / indispensable
- 0,50-0,74 : Plutôt pertinent
- 0,25-0.49 : Pas très pertinent, peut quand même servir
- 0,00-0,24 : Pas du tout pertinent

Retourne UNIQUEMENT un objet JSON avec la même structure que celle fournie ci-dessous, en ajoutant le score de chaque élément.
"""

    query = flatten_resume_for_query()
    prompt = f"{score_prompt}\n\n## Éléments à noter :\n{json.dumps(query, ensure_ascii=False, indent=2)}"
    result = openai.query(prompt, True)

    try:
        cleaned_result = clean_json(result)
        scores = json.loads(cleaned_result)
        return scores
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from OpenAI: {e}")
        print(f"Raw response: {result}")
        raise


def flatten_resume_for_query():
    try:
        with open(Config.RESUME_JSON, "r", encoding="utf-8") as f:
            json_resume = json.load(f)

        overrides_list = json_resume["overrides"]
        resume_data = json_resume["resume"]

        query = {}

        for override in overrides_list:
            key = override.get("name")
            if not key:
                continue

            section = resume_data.get(key)
            if not section:
                continue

            if isinstance(section, dict) and all(
                isinstance(v, list) for v in section.values()
            ):
                query[key] = {}
                for subkey, items in section.items():
                    query[key][subkey] = []
                    for item in items:
                        if isinstance(item, dict):
                            query[key][subkey].append(
                                {**item, "score": item.get("score", 0)}
                            )
                        else:
                            query[key][subkey].append({"name": item, "score": 0})

            elif isinstance(section, list):
                query[key] = []
                for item in section:
                    if isinstance(item, dict):
                        query[key].append({**item, "score": item.get("score", 0)})
                    else:
                        query[key].append({"name": item, "score": 0})

        return query

    except Exception as e:
        print(f"Error reading resume.json: {e}")
        raise


def create_sorted_overrides(scores):
    instructions = load_override_instructions()
    overrides = {}

    for key, value in scores.items():
        section_instructions = instructions.get(key)

        if isinstance(value, dict) and all(isinstance(v, list) for v in value.values()):
            overrides[key] = {}
            all_items_by_subsection = value
            promoted_names = set()

            for subkey, items in value.items():
                sorted_items = sort_items(items)
                subsection_instructions = (
                    section_instructions.get(subkey) if section_instructions else None
                )
                filtered_items = filter_items(
                    sorted_items,
                    subsection_instructions,
                    category_name=subkey,
                    all_items_by_category=all_items_by_subsection,
                    promoted_names=promoted_names,
                )
                overrides[key][subkey] = filtered_items

            if "secondary" in overrides[key]:
                overrides[key]["secondary"] = [
                    i
                    for i in overrides[key]["secondary"]
                    if i.get("name") not in promoted_names
                ]

        elif isinstance(value, list):
            sorted_items = sort_items(value)
            filtered_items = filter_items(sorted_items, section_instructions)
            overrides[key] = filtered_items

    return overrides


def load_override_instructions():
    try:
        with open(Config.RESUME_JSON, "r", encoding="utf-8") as f:
            resume_data = json.load(f)

        overrides_list = resume_data.get("overrides", [])
        instructions_dict = {}

        for override in overrides_list:
            if isinstance(override, dict) and "name" in override:
                instructions_dict[override["name"]] = override.get("instructions", {})

        return instructions_dict
    except Exception as e:
        print(f"Error loading override instructions: {e}")
        return {}


def filter_items(
    items,
    instructions,
    category_name=None,
    all_items_by_category=None,
    promoted_names=None,
):
    if not instructions or not items:
        return items

    min_items = instructions.get("min", 0)
    max_items = instructions.get("max", len(items))

    mandatory = [item for item in items if item.get("mandatory", False)]
    non_mandatory = [item for item in items if not item.get("mandatory", False)]

    result = mandatory.copy()
    remaining_slots = max_items - len(mandatory)

    for item in non_mandatory:
        if len(result) >= max_items:
            break
        score = item.get("score", 0)
        if score >= SCORE_THRESHOLD:
            result.append(item)

    if category_name == "main" and all_items_by_category:
        secondary_items = all_items_by_category.get("secondary", [])
        for item in secondary_items:
            score = item.get("score", 0)
            if score > 0.9 and item.get("name") not in [i.get("name") for i in result]:
                result.append(item)
                if promoted_names is not None:
                    promoted_names.add(item.get("name"))
        if len(result) > max_items:
            result.sort(key=lambda x: x.get("score", 0), reverse=True)
            result = result[:max_items]

    if len(result) < min_items:
        remaining_items = [i for i in non_mandatory if i not in result]
        items_needed = min(min_items - len(result), max_items - len(result))
        result.extend(remaining_items[:items_needed])

    result = result[:max_items]
    return result


def sort_items(items):
    return sorted(
        items,
        key=lambda x: (
            int(x.get("is_last", False)),
            -x.get("score", 0),
            -int(x.get("mandatory", False)),
        ),
    )


def save_overrides_file(overrides, folder_path):
    job_override_file = Path(folder_path) / "overrides.json"
    public_override_file = Config.RESUME_DIR / "public" / "overrides.json"

    try:
        if Config.DEBUG_MODE:
            with open(job_override_file, "w", encoding="utf-8") as f:
                json.dump(overrides, f, ensure_ascii=False, indent=2)
            print(f"Created job overrides file: {job_override_file}")

        if not Config.DEBUG_MODE:
            with open(public_override_file, "w", encoding="utf-8") as f:
                json.dump(overrides, f, ensure_ascii=False, indent=2)
            print(f"Created public overrides file: {public_override_file}")
    except Exception as e:
        print(f"Error creating overrides.json: {e}")
        raise


def generate_resume_pdf(folder_path):
    folder_path = Path(folder_path)
    output_pdf = folder_path / "CV César Fuentes.pdf"

    try:
        result = subprocess.run(
            [
                "node",
                str(Config.RESUME_SCRIPT),
                str(output_pdf),
            ],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(Config.RESUME_DIR),
        )

        print(result.stdout)
        if result.stderr:
            print(f"Warnings: {result.stderr}")

        print(f"Resume PDF generated: {output_pdf}")
        return str(output_pdf)

    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e.stderr}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise
