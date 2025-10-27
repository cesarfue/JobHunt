import csv
import sqlite3

from db.db import DB_PATH


def import_jobs_from_csv(csv_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print(f"importing from : {csv_path}")

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            status = row.get("Status", "applied").strip()
            company = row.get("Company name", "").strip()
            site = row.get("Plateform", "").strip().lower()
            title = row.get("Job Title", "").strip()
            url = row.get("URL", "").strip()
            job_type = row.get("Contract", "").strip()
            date_added = row.get("Date", "").strip()

            if not url:
                continue

            c.execute("SELECT status FROM jobs WHERE url = ?", (url,))
            existing = c.fetchone()

            if existing:
                if existing[0] != status:
                    c.execute(
                        "UPDATE jobs SET status = ?, date_added = ? WHERE url = ?",
                        (status, date_added, url),
                    )
            else:
                c.execute(
                    """
                    INSERT INTO jobs (title, company, location, site, url, job_type, score, date_added, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (title, company, "", site, url, job_type, 0.0, date_added, status),
                )

    conn.commit()
    conn.close()
    print(f"CSV import completed: {csv_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m app.import_from_csv <csv_path>")
        sys.exit(1)

    csv_path = sys.argv[1]
    import_jobs_from_csv(csv_path)
