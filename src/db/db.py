import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "jobs.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            site TEXT,
            url TEXT UNIQUE,
            job_type TEXT,
            score REAL DEFAULT 0.0,
            date_added TEXT,
            status TEXT DEFAULT 'pending'
        )
    """
    )
    conn.commit()
    conn.close()


def insert_jobs(jobs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for job in jobs:
        url = job.get("job_url").rstrip("/")
        try:
            c.execute(
                """
                INSERT INTO jobs (title, company, location, site, url, job_type, score, date_added, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, date('now'), 'pending')
            """,
                (
                    job.get("title"),
                    job.get("company"),
                    job.get("location"),
                    job.get("site"),
                    url,
                    job.get("job_type"),
                    job.get("score"),
                ),
            )
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()


def mark_job_as_applied(job_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status='applied' WHERE id=?", (job_id,))
    conn.commit()
    conn.close()


def mark_job_as_discarded(job_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status='discarded' WHERE id=?", (job_id,))
    conn.commit()
    conn.close()


def get_pending_jobs(order):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = f"SELECT id, title, company, site, location, url FROM jobs WHERE status='pending' ORDER BY score {order}, date_added {order}"
    c.execute(query)
    jobs = c.fetchall()
    conn.close()
    return jobs


def get_applied_jobs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, title, company, site, location, url FROM jobs WHERE status='applied' ORDER BY score ASC, date_added ASC"
    )
    jobs = c.fetchall()
    conn.close()
    return jobs


def get_all_jobs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT id, title, company, site, location, url, status
        FROM jobs
        WHERE status != 'discarded'
        ORDER BY status ASC, score ASC, date_added ASC
        """
    )
    jobs = c.fetchall()
    conn.close()
    return jobs
