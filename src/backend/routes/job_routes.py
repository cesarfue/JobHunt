from datetime import datetime

from config import Config
from flask import Blueprint, jsonify, request
from services.document_service import add_to_sheet, make_letter
from services.filesystem_service import create_folder, open_folder_in_explorer
from services.openai_service import OpenAIService
from services.resume_service import make_resume

bp = Blueprint("job", __name__, url_prefix="/api")


@bp.route("/job", methods=["POST", "OPTIONS"])
def handle_job():
    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.json
        openai = OpenAIService(data["content"])
        extracted = openai.job_content
        company = extracted.get("company", "Inconnue").title()
        job_title = extracted.get("job_title", data.get("title", "Poste")).title()
        platform = extracted.get("platform", "Hors Plateforme").title()

        today = datetime.now().strftime("%Y-%m-%d")
        folder_path = create_folder(company, today)

        make_resume(openai, folder_path)
        if not Config.DEBUG_MODE:
            add_to_sheet(company, platform, job_title, data["url"], today)
            make_letter(openai, folder_path)
            open_folder_in_explorer(folder_path)

        return jsonify(
            {
                "status": "success",
                "folderPath": folder_path,
                "company": company,
                "jobTitle": job_title,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
