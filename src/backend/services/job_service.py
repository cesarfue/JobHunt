from datetime import datetime

from config import Config
from services.document_service import (
    create_letter_doc,
    create_overrides_json,
    generate_resume_pdf,
)
from services.openai_service import get_prompts, query_openai


def generate_job_documents(company, job_title, job_content):
    prompts = get_prompts()

    results = {}
    debug_log = []

    for key, prompt in prompts.items():
        full_prompt = f"{prompt}\n\n## Job content\n{job_content}"
        answer = query_openai(full_prompt)
        results[key] = answer

        if Config.DEBUG_MODE:
            debug_log.append(
                {
                    "key": key,
                    "prompt": full_prompt,
                    "answer": answer,
                    "timestamp": datetime.now().isoformat(),
                }
            )

    today = datetime.now()
    formatted_date = today.strftime("%Y-%m-%d")

    base_folder_name = f"{company} - {formatted_date}"
    folder_path = Config.APPLICATIONS_DIR / base_folder_name

    counter = 1
    while folder_path.exists():
        folder_name = f"{base_folder_name} ({counter})"
        folder_path = Config.APPLICATIONS_DIR / folder_name
        counter += 1

    folder_path.mkdir(parents=True, exist_ok=True)

    if "letter" in results:
        create_letter_doc(folder_path, results["letter"])

    create_overrides_json(folder_path, results)
    generate_resume_pdf(folder_path, company, formatted_date)

    if Config.DEBUG_MODE and debug_log:
        import json

        debug_file = folder_path / "debug_log.json"
        with open(debug_file, "w", encoding="utf-8") as f:
            json.dump(debug_log, f, ensure_ascii=False, indent=2)
        print(f"Debug log created: {debug_file}")

    return str(folder_path.absolute())
