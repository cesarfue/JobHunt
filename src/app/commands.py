import sqlite3
import webbrowser

import requests
from tabulate import tabulate

from db.db import DB_PATH, get_all_jobs, mark_job_as_discarded

API_URL = "http://127.0.0.1:5000/api/job"


def apply_to_job(job):
    job_id, title, company, site, location, url, status = job
    print(f"\n  Applying to {company} - {title}...")
    try:
        requests.post(API_URL, json={"url": url}, timeout=60)
        mark_job_as_wip(job_id)
        return True
    except Exception as e:
        print(f"Error while sending url {url}: {e}")
        return False


def discard_job(job):
    job_id = job[0]
    mark_job_as_discarded(job_id)
    print(f"Job discarded")


def open_job_url(job_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url FROM jobs WHERE id = ?", (job_id,))
    row = c.fetchone()
    conn.close()

    if row:
        url = row[0]
        webbrowser.open(url)
    else:
        print(f"No job found with id {job_id}")


def show_all_jobs():
    jobs = get_all_jobs()
    if not jobs:
        print("\nNo jobs in database!")
        return

    table = []
    for job in jobs:
        job_id, title, company, site, location, date_added, status = job
        if status == "pending":
            status_display = f"\033[93m{status.upper()}\033[0m"
        elif status == "wip":
            status_display = f"\033[94m{status.upper()}\033[0m"
        elif status == "applied":
            status_display = f"\033[92m{status.upper()}\033[0m"
        else:
            status_display = f"\033[91m{status.upper()}\033[0m"

        table.append(
            [
                job_id,
                title[:40],
                company[:20],
                site,
                location[:20],
                date_added,
                status_display,
            ]
        )

    print("\n" + "=" * 120)
    print("  ALL JOBS")
    print("=" * 120 + "\n")
    print(
        tabulate(
            table,
            headers=[
                "ID",
                "Title",
                "Company",
                "Site",
                "Location",
                "Date added",
                "Status",
            ],
            tablefmt="fancy_grid",
        )
    )
    print(f"\n  Total: {len(jobs)} jobs\n")


def show_stats():
    all_jobs = get_all_jobs()
    pending = sum(1 for job in all_jobs if job[6].lower() == "pending")
    wip = sum(1 for job in all_jobs if job[6].lower() == "wip")
    applied = sum(1 for job in all_jobs if job[6].lower() == "applied")
    discarded = sum(1 for job in all_jobs if job[6].lower() == "discarded")

    print("\n" + "=" * 50)
    print("  JOB STATISTICS")
    print("=" * 50)
    print(f"  \033[93mPending:\033[0m    {pending}")
    print(f"  \033[94mWIP:\033[0m        {wip}")
    print(f"  \033[92mApplied:\033[0m    {applied}")
    print(f"  \033[91mDiscarded:\033[0m  {discarded}")
    print(f"  Total:      {len(all_jobs)}")
    print("=" * 50 + "\n")
