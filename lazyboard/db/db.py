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
            type TEXT,
            score REAL DEFAULT 0.0,
            date_added TEXT,
            status TEXT DEFAULT 'pending',
            description TEXT
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
                INSERT INTO jobs (title, company, location, site, url, type, score, description, date_added, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, date('now'), 'pending')
            """,
                (
                    job.get("title"),
                    job.get("company"),
                    job.get("location"),
                    job.get("site"),
                    url,
                    job.get("job_type"),
                    job.get("score"),
                    job.get("description"),
                ),
            )
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()


def mark_job_as_applied(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status='applied' WHERE id=?", (id,))
    conn.commit()
    conn.close()


def mark_job_as_wip(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status='wip' WHERE id=?", (id,))
    conn.commit()
    conn.close()


def mark_job_as_discarded(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status='discarded' WHERE id=?", (id,))
    conn.commit()
    conn.close()


def mark_job_as_pending(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE jobs SET status='pending' WHERE id=?", (id,))
    conn.commit()
    conn.close()


def get_pending_jobs(order):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    query = f"SELECT id, title, company, site, location, url, status FROM jobs WHERE status='pending' OR status='wip' ORDER BY status {order}, score {order}, date_added {order}"
    c.execute(query)
    jobs = c.fetchall()
    conn.close()
    return jobs


def get_applied_jobs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, title, company, site, location, date_added FROM jobs WHERE status='applied' ORDER BY score ASC, date_added ASC"
    )
    jobs = c.fetchall()
    conn.close()
    return jobs


def get_all_jobs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT id, title, company, site, location, date_added, status
        FROM jobs
        WHERE status != 'discarded'
        ORDER BY
          CASE status
            WHEN 'pending' THEN 4
            WHEN 'wip' THEN 3
            WHEN 'applied' THEN 2
            ELSE 1
          END,
          score ASC, date_added ASC
        """
    )
    jobs = c.fetchall()
    conn.close()
    return jobs
