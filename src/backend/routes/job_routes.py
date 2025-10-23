from datetime import datetime

from flask import Blueprint, jsonify, request
from services.excel_service import add_to_excel
from services.job_service import generate_job_documents
from services.openai_service import extract_job_info

bp = Blueprint("job", __name__, url_prefix="/api")


@bp.route("/job", methods=["POST", "OPTIONS"])
def handle_job():
    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.json
        extracted = extract_job_info(data["content"])
        company = extracted.get("company", "Inconnue").title()
        job_title = extracted.get("job_title", data.get("title", "Poste")).title()
        job_content = extracted.get("job_description", data.get("content", ""))
        platform = extracted.get("platform", "Hors Plateforme").title()

        today = datetime.now().strftime("%Y-%m-%d")
        add_to_excel(company, platform, job_title, data["url"], today)
        folder_path = generate_job_documents(company, job_title, job_content)

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
