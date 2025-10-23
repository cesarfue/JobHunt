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
    for key, prompt in prompts.items():
        results[key] = query_openai(f"{prompt}\n\n## Job content\n{job_content}")

    today = datetime.now()
    formatted_date = today.strftime("%Y-%m-%d")
    folder_name = f"{company} - {formatted_date}"
    folder_path = Config.CANDIDATURES_DIR / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    if "letter" in results:
        create_letter_doc(folder_path, results["letter"])

    create_overrides_json(folder_path, results)
    generate_resume_pdf(folder_path, company, formatted_date)

    return str(folder_path.absolute())
