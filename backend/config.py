from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.parent
    BACKEND_DIR = Path(__file__).parent
    APPLICATIONS_DIR = BASE_DIR / "Applications"
    RESUME_DIR = BASE_DIR / "resume"
    RESUME_JSON = RESUME_DIR / "public" / "resume.json"
    RESUME_SCRIPT = RESUME_DIR / "exportToPDF.js"
    DEBUG_MODE = False
    LETTER_FILE = BACKEND_DIR / "Lettre de motivation César Fuentes.docx"
