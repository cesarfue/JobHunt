import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

from src.config import DB_PATH
from src.models.job import Job, JobStatus


class JobRepository:

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = DB_PATH
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
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
                    status TEXT DEFAULT 'pending',
                    description TEXT
                )
            """
            )
            conn.commit()

    def save(self, job: Job) -> Job:
        with self.get_connection() as conn:
            c = conn.cursor()

            if job.id is None:
                try:
                    c.execute(
                        """
                        INSERT INTO jobs 
                        (title, company, location, site, url, job_type, score, 
                         description, date_added, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            job.title,
                            job.company,
                            job.location,
                            job.site,
                            job.url.rstrip("/"),
                            job.job_type,
                            job.score,
                            job.description,
                            job.date_added.isoformat(),
                            job.status.value,
                        ),
                    )
                    job.id = c.lastrowid
                    conn.commit()
                except sqlite3.IntegrityError:
                    return self.find_by_url(job.url)
            else:
                c.execute(
                    """
                    UPDATE jobs 
                    SET title=?, company=?, location=?, site=?, job_type=?, 
                        score=?, description=?, status=?, date_added=?
                    WHERE id=?
                """,
                    (
                        job.title,
                        job.company,
                        job.location,
                        job.site,
                        job.job_type,
                        job.score,
                        job.description,
                        job.status.value,
                        job.date_added.isoformat(),
                        job.id,
                    ),
                )
                conn.commit()

        return job

    def save_many(self, jobs: List[Job]) -> List[Job]:
        saved_jobs = []
        for job in jobs:
            saved_jobs.append(self.save(job))
        return saved_jobs

    def find_by_id(self, job_id: int) -> Optional[Job]:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                SELECT id, title, company, site, location, url, 
                       job_type, score, date_added, status, description
                FROM jobs WHERE id = ?
            """,
                (job_id,),
            )
            row = c.fetchone()

            if row:
                return Job(
                    id=row[0],
                    title=row[1],
                    company=row[2],
                    site=row[3],
                    location=row[4],
                    url=row[5],
                    job_type=row[6],
                    score=row[7],
                    date_added=row[8],
                    status=row[9],
                    description=row[10] if len(row) > 10 else "",
                )
            return None

    def find_by_url(self, url: str) -> Optional[Job]:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                SELECT id, title, company, site, location, url, 
                       job_type, score, date_added, status, description
                FROM jobs WHERE url = ?
            """,
                (url.rstrip("/"),),
            )
            row = c.fetchone()

            if row:
                return Job(
                    id=row[0],
                    title=row[1],
                    company=row[2],
                    site=row[3],
                    location=row[4],
                    url=row[5],
                    job_type=row[6],
                    score=row[7],
                    date_added=row[8],
                    status=row[9],
                    description=row[10] if len(row) > 10 else "",
                )
            return None

    def find_pending_and_wip(self, order_by: str = "DESC") -> List[Job]:
        with self.get_connection() as conn:
            c = conn.cursor()
            query = f"""
                SELECT id, title, company, site, location, url, status, description
                FROM jobs 
                WHERE status IN ('pending', 'wip')
                ORDER BY status {order_by}, score {order_by}, date_added {order_by}
            """
            c.execute(query)
            rows = c.fetchall()

            jobs = []
            for row in rows:
                jobs.append(
                    Job(
                        id=row[0],
                        title=row[1],
                        company=row[2],
                        site=row[3],
                        location=row[4],
                        url=row[5],
                        status=row[6],
                        description=row[7] if len(row) > 7 else "",
                    )
                )
            return jobs

    def find_all(self, include_discarded: bool = False) -> List[Job]:
        with self.get_connection() as conn:
            c = conn.cursor()

            if include_discarded:
                query = """
                    SELECT id, title, company, site, location, date_added, status
                    FROM jobs
                    ORDER BY
                      CASE status
                        WHEN 'pending' THEN 4
                        WHEN 'wip' THEN 3
                        WHEN 'applied' THEN 2
                        ELSE 1
                      END,
                      score ASC, date_added ASC
                """
            else:
                query = """
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

            c.execute(query)
            rows = c.fetchall()
            return [Job.from_row(row) for row in rows]

    def count_by_status(self) -> dict:
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(
                """
                SELECT status, COUNT(*) 
                FROM jobs 
                GROUP BY status
            """
            )
            rows = c.fetchall()
            return {row[0]: row[1] for row in rows}
