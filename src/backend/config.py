from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.parent.parent
    SRC_DIR = Path(__file__).parent.parent
    PROMPTS_DIR = SRC_DIR / "backend"
    APPLICATIONS_DIR = BASE_DIR / "Applications"
    RESUME_DIR = SRC_DIR / "resume"
    RESUME_JSON = RESUME_DIR / "public" / "resume.json"
    RESUME_SCRIPT = RESUME_DIR / "exportToPDF.js"
    DEBUG_MODE = False
    LETTER_FILE = SRC_DIR / "Lettre de motivation César Fuentes.docx"
