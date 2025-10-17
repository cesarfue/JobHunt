import json
import os
from datetime import datetime
from pathlib import Path

import openai
import openpyxl
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS with proper configuration for Chrome extensions
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
        }
    },
)

# Configuration
API_KEY = os.getenv(API_KEY)
BASE_DIR = Path(__file__).parent
CANDIDATURES_DIR = BASE_DIR / "Candidatures"
PROMPTS_DIR = BASE_DIR / "prompts"
EXCEL_FILE = BASE_DIR / "Recherche Janvier 2026.xlsx"
DEBUG_MODE = False

openai.api_key = API_KEY


def query_openai(prompt):
    """Query OpenAI API"""
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def get_prompts():
    """Load prompts from text files"""
    prompts = {}
    prompt_map = {
        "prompt_1.txt": "HARD_SKILLS",
        "prompt_2.txt": "SOFT_SKILLS",
        "prompt_3.txt": "LETTER",
    }

    for filename, key in prompt_map.items():
        filepath = PROMPTS_DIR / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                prompts[key] = f.read().strip()

    return prompts


def extract_job_info(content):
    """Extract job information using OpenAI"""
    prompt = f"""
À partir du texte de page web ci-dessous, retourne uniquement en JSON, sans aucune autre information:
{{
  "company": "Nom de la société qui poste l'offre d'emploi",
  "job_title": "Intitulé du poste",
  "platform": "Plateforme d'offres d'emploi",
  "job_description": "Contenu de l'offre d'emploi"
}}
Offre d'emploi:
{content}
"""

    response = query_openai(prompt)
    return json.loads(response)


def add_to_excel(company, platform, job_title, url, date):
    """Add entry to Excel tracking sheet"""
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb["suivi"]

    new_row = ["A faire", "CDI", company, platform, job_title, url, date, ""]
    ws.append(new_row)

    # Sort by column 1 (Status) ascending, then column 8 (Date) descending
    # Note: openpyxl doesn't have built-in sort, so we do it manually
    data = list(ws.iter_rows(min_row=3, values_only=True))
    data.sort(key=lambda x: (x[0] or "", x[7] or ""), reverse=False)

    # Clear and rewrite data
    for row_idx, row_data in enumerate(data, start=3):
        for col_idx, value in enumerate(row_data, start=1):
            ws.cell(row=row_idx, column=col_idx, value=value)

    wb.save(EXCEL_FILE)


def create_letter_doc(folder_path, content):
    """Create formatted cover letter in Word"""
    doc = Document()

    # Set default font
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(11)

    # Add content
    for paragraph in content.split("\n"):
        p = doc.add_paragraph(paragraph)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.save(folder_path / "Lettre de motivation.docx")


def create_skills_doc(folder_path, company, date, results, prompts):
    """Create skills document in Word"""
    doc = Document()

    if DEBUG_MODE:
        doc.add_heading("🔍 DEBUG INFORMATION", level=1)
        for key, prompt in prompts.items():
            doc.add_heading(f"{key} Prompt", level=3)
            doc.add_paragraph(prompt)
            doc.add_paragraph("---")
        doc.add_page_break()
        doc.add_heading("📄 GENERATED CONTENT", level=1)

    # Resume section
    doc.add_heading("RESUME", level=2)
    p1 = doc.add_paragraph("Dupliquer le CV Base sur Canva")
    p1.add_run().add_break()
    doc.add_paragraph(f'→ Renommer la copie : "{company} - {date}"')
    doc.add_paragraph()

    # Hard skills
    doc.add_heading("HARD SKILLS", level=2)
    doc.add_paragraph(results["HARD_SKILLS"])

    # Soft skills
    doc.add_heading("SOFT SKILLS", level=2)
    doc.add_paragraph(results["SOFT_SKILLS"])

    doc.save(folder_path / "Compétences.docx")


def generate_job_documents(company, job_title, job_content):
    """Generate all documents for a job application"""
    prompts = get_prompts()

    # Generate content using OpenAI
    results = {}
    for key, prompt in prompts.items():
        results[key] = query_openai(f"{prompt}\n\n{job_content}")

    # Create folder
    today = datetime.now()
    formatted_date = today.strftime("%Y-%m-%d")
    folder_name = f"{company} - {formatted_date}"
    folder_path = CANDIDATURES_DIR / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    # Create documents
    create_letter_doc(folder_path, results["LETTER"])
    create_skills_doc(folder_path, company, formatted_date, results, prompts)

    return str(folder_path.absolute())


@app.route("/api/job", methods=["POST", "OPTIONS"])
def handle_job():
    """Handle job posting from Chrome extension"""
    if request.method == "OPTIONS":
        return "", 204

    try:
        data = request.json

        # Extract job information
        extracted = extract_job_info(data["content"])

        company = extracted.get("company", "Inconnue")
        job_title = extracted.get("job_title", data.get("title", "Poste"))
        job_content = extracted.get("job_description", data.get("content", ""))
        platform = extracted.get("platform", "Hors Plateforme")

        # Add to Excel
        today = datetime.now().strftime("%Y-%m-%d")
        add_to_excel(company, platform, job_title, data["url"], today)

        # Generate documents
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


if __name__ == "__main__":
    # Ensure directories exist
    CANDIDATURES_DIR.mkdir(exist_ok=True)
    PROMPTS_DIR.mkdir(exist_ok=True)

    print(f"Server starting...")
    print(f"Candidatures folder: {CANDIDATURES_DIR}")
    print(f"Prompts folder: {PROMPTS_DIR}")
    print(f"Excel file: {EXCEL_FILE}")

    app.run(debug=True, port=5000)
