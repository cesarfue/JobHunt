import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RESUME_DIR = BASE_DIR.parent / "resume"

DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "jobs.db"

API_URL = os.getenv("LAZYBOARD_API_URL", "http://127.0.0.1:5000/api/job")

SCRAPE_SITES = ["indeed", "linkedin"]
SCRAPE_TERM = os.getenv("LAZYBOARD_SEARCH_TERM", "développeur")
SCRAPE_LOCATION = os.getenv("LAZYBOARD_LOCATION", "Lyon, France")
SCRAPE_RESULTS = int(os.getenv("LAZYBOARD_RESULTS", "30"))
SCRAPE_HOURS_OLD = int(os.getenv("LAZYBOARD_HOURS_OLD", "24"))

RESUME_PATH = RESUME_DIR / "public" / "resume.json"
