from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.parent
    CANDIDATURES_DIR = BASE_DIR / "Applications"
    PROMPTS_DIR = BASE_DIR / "prompts"
    EXCEL_FILE = BASE_DIR / "Recherche Janvier 2026.xlsx"
    RESUME_DIR = BASE_DIR / "resume"
    RESUME_JSON = RESUME_DIR / "public" / "resume.json"
    RESUME_SCRIPT = RESUME_DIR / "exportToPDF.js"
    PHOTO_PATH = RESUME_DIR / "src" / "assets" / "photo.jpeg"
    RESUME_OVERRIDES_DIR = RESUME_DIR / "public" / "resume_overrides"
    DEBUG_MODE = False
