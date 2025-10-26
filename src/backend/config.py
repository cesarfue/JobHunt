from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.parent.parent
    SRC_DIR = Path(__file__).parent.parent
    PROMPTS_DIR = SRC_DIR / "backend"
    APPLICATIONS_DIR = BASE_DIR / "Applications"
    EXCEL_FILE = BASE_DIR / "Recherche Janvier 2026.xlsx"
    RESUME_DIR = SRC_DIR / "resume"
    RESUME_JSON = RESUME_DIR / "public" / "resume.json"
    RESUME_SCRIPT = RESUME_DIR / "exportToPDF.js"
    PHOTO_PATH = RESUME_DIR / "src" / "assets" / "photo.jpeg"
    RESUME_OVERRIDES_DIR = RESUME_DIR / "public" / "resume_overrides"
    LOG_FOLDER = SRC_DIR / "backend" / "log"
    DEBUG_MODE = False
