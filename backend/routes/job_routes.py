from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify, request
from services.document_service import make_letter
from services.filesystem_service import create_folder, open_folder_in_explorer
from services.openai_service import OpenAIService
from services.resume_service import make_resume

bp = Blueprint("job", __name__, url_prefix="/api")


def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


@bp.route("/job", methods=["POST", "OPTIONS"])
def handle_job():
    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.json or {}
        openai = OpenAIService()

        if data.get("description"):
            openai.job_content = data.get("description")
            print(f"giving description : {openai.job_content}")
        else:
            url = data.get("url")
            response = requests.get(url, timeout=10)
            if not response.ok:
                return (
                    jsonify({"status": "error", "message": f"Failed to fetch: {url}"}),
                    400,
                )
            openai.extract_job_info(extract_visible_text(response.text))

        company = data.get("company", "")
        today = datetime.now().strftime("%Y-%m-%d")

        folder_path = create_folder(company, today)
        make_resume(openai, folder_path)
        make_letter(folder_path)
        open_folder_in_explorer(folder_path)

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
