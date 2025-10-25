import platform
import subprocess
from datetime import datetime

from config import Config
from services.document_service import create_letter_doc, generate_resume_pdf
from services.json_service import create_overrides_json
from services.openai_service import submit_prompts


def open_folder_in_explorer(folder_path):
    try:
        system = platform.system()
        if system == "Windows":
            subprocess.run(["explorer", str(folder_path)])
        elif system == "Darwin":
            subprocess.run(["open", str(folder_path)])
        else:
            subprocess.run(["xdg-open", str(folder_path)])
        return True
    except Exception as e:
        print(f"Error opening folder: {e}")
        return False


def create_folder(folder_path, base_folder_name):
    counter = 1
    while folder_path.exists():
        folder_name = f"{base_folder_name} ({counter})"
        folder_path = Config.APPLICATIONS_DIR / folder_name
        counter += 1

    folder_path.mkdir(parents=True, exist_ok=True)


def generate_job_documents(company, job_content):
    today = datetime.now()
    formatted_date = today.strftime("%Y-%m-%d")
    base_folder_name = f"{company} - {formatted_date}"
    folder_path = Config.APPLICATIONS_DIR / base_folder_name

    create_folder(folder_path, base_folder_name)

    results = submit_prompts(job_content, folder_path)

    if "letter" in results:
        create_letter_doc(folder_path, results["letter"])

    create_overrides_json(folder_path, results)
    generate_resume_pdf(folder_path, company, formatted_date)

    open_folder_in_explorer(folder_path)

    return str(folder_path.absolute())
