import sqlite3
import webbrowser

import requests
from app.ui_utils import (
    Colors,
    calculate_column_widths,
    colorize,
    get_status_display,
    get_terminal_size,
    print_footer,
    print_header,
    truncate_text,
)
from db.db import DB_PATH, get_all_jobs, mark_job_as_discarded, mark_job_as_wip
from tabulate import tabulate

API_URL = "http://127.0.0.1:5000/api/job"


def apply_to_job(job):
    job_id, title, company, site, location, url, status = job
    print(f"\nApplying to {company} - {title}...")

    try:
        response = requests.post(API_URL, json={"url": url}, timeout=60)
        if response.status_code != 200:
            return False

        mark_job_as_wip(job_id)
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error while sending {url}: {e}")
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

    width, _ = get_terminal_size()

    all_columns = [
        ("id", "ID", 5, 0),
        ("title", "Title", 40, 0),
        ("company", "Company", 20, 60),
        ("site", "Site", 5, 60),
        ("location", "Location", 15, 100),
        ("date", "Date added", 12, 120),
        ("status", "Status", 12, 0),
    ]

    visible_columns = []
    headers = []

    for col_name, display_name, col_width, min_width in all_columns:
        if width >= min_width:
            visible_columns.append((col_name, col_width))
            headers.append(display_name)

    flexible_config = []
    for col_name, col_width in visible_columns:
        if col_name == "title":
            flexible_config.append((col_name, 0.5, 20))
        elif col_name == "company":
            flexible_config.append((col_name, 0.3, 10))
        elif col_name == "location":
            flexible_config.append((col_name, 0.2, 10))
        elif col_name == "site":
            flexible_config.append((col_name, 0.2, 10))
        else:
            flexible_config.append((col_name, col_width, col_width))

    widths = calculate_column_widths(width, flexible_config)

    table = []
    for job in jobs:
        job_id, title, company, site, location, date_added, status = job

        row = []
        for col_name, _ in visible_columns:
            if col_name == "id":
                row.append(job_id)
            elif col_name == "title":
                row.append(truncate_text(title, widths["title"]))
            elif col_name == "company":
                row.append(truncate_text(company, widths["company"]))
            elif col_name == "site":
                row.append(truncate_text(site, widths["site"]))
            elif col_name == "location":
                row.append(truncate_text(location, widths["location"]))
            elif col_name == "date":
                row.append(date_added)
            elif col_name == "status":
                row.append(get_status_display(status))

        table.append(row)

    print_header("ALL JOBS", width)
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="fancy_grid",
        )
    )
    print(f"\n  Total: {len(jobs)} jobs")
    print_footer(width)


def show_stats():
    width, _ = get_terminal_size()
    all_jobs = get_all_jobs()

    pending = sum(1 for job in all_jobs if job[6].lower() == "pending")
    wip = sum(1 for job in all_jobs if job[6].lower() == "wip")
    applied = sum(1 for job in all_jobs if job[6].lower() == "applied")
    discarded = sum(1 for job in all_jobs if job[6].lower() == "discarded")

    box_width = min(50, width - 4)

    print_header("JOB STATISTICS", box_width)
    print(f"  {colorize('Pending:', Colors.YELLOW)}    {pending}")
    print(f"  {colorize('WIP:', Colors.BLUE)}        {wip}")
    print(f"  {colorize('Applied:', Colors.GREEN)}    {applied}")
    print(f"  {colorize('Discarded:', Colors.RED)}  {discarded}")
    print(f"  Total:      {len(all_jobs)}")
    print_footer(box_width)
