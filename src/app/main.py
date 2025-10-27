import sqlite3
import webbrowser

from prompt_toolkit import PromptSession
from tabulate import tabulate

from app.job_picker import interactive_job_picker, list_subs
from app.web_parser import add_job_entry
from db.db import DB_PATH, get_all_jobs
from scraper.scrape import run_scraper


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
        job_id, title, company, site, location, url, status = job
        if status == "applied":
            status_display = f"\033[92m{status.upper()}\033[0m"  # Green
        elif status == "discarded":
            status_display = f"\033[91m{status.upper()}\033[0m"  # Red
        else:
            status_display = f"\033[93m{status.upper()}\033[0m"  # Yellow

        table.append(
            [
                job_id,
                title[:40],
                company[:20],
                site,
                location[:20],
                url[:20],
                status_display,
            ]
        )

    print("\n" + "=" * 120)
    print("  ALL JOBS")
    print("=" * 120 + "\n")
    print(
        tabulate(
            table,
            headers=["ID", "Title", "Company", "Site", "Location", "URL", "Status"],
            tablefmt="fancy_grid",
        )
    )
    print(f"\n  Total: {len(jobs)} jobs\n")


def show_stats():
    all_jobs = get_all_jobs()
    applied = sum(1 for job in all_jobs if job[6].lower() == "applied")
    discarded = sum(1 for job in all_jobs if job[6].lower() == "discarded")
    pending = sum(1 for job in all_jobs if job[6].lower() == "pending")

    print("\n" + "=" * 50)
    print("  JOB STATISTICS")
    print("=" * 50)
    print(f"  \033[93mPending:\033[0m    {pending}")
    print(f"  \033[92mApplied:\033[0m    {applied}")
    print(f"  \033[91mDiscarded:\033[0m  {discarded}")
    print(f"  Total:      {len(all_jobs)}")
    print("=" * 50 + "\n")


def main():
    session = PromptSession()

    print("\n" + "=" * 60)
    print("  OverengineeredJobSearch Interactive Shell!")
    print("=" * 60)
    print("\n  Available commands:")
    print("    start          - Start reviewing pending jobs")
    print("    subs           - List all applied jobs")
    print("    list           - Show all jobs with status")
    print("    stats          - Show job statistics")
    print("    fetch          - Fetch new jobs")
    print("    open           - Open job page in browser")
    print("    exit           - Quit the application")
    print()

    while True:
        try:
            cmd = session.prompt("> ").strip()
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        if cmd == "exit":
            break

        elif cmd == "start":
            interactive_job_picker()

        elif cmd == "subs":
            list_subs()

        elif cmd == "list":
            show_all_jobs()

        elif cmd == "stats":
            show_stats()

        elif cmd == "fetch":
            run_scraper()

        elif cmd.startswith("add"):
            parts = cmd.split()
            if len(parts) == 2:
                add_job_entry(parts[1])

        elif cmd.startswith("open"):
            parts = cmd.split()
            if len(parts) == 2:
                try:
                    job_id = int(parts[1])
                    open_job_url(job_id)
                except ValueError:
                    print("Invalid job ID. Must be a number.")
            else:
                print("Usage: open <job_id>")

        else:
            print(
                "Unknown command. Type 'start', 'subs', 'list', 'stats', 'add', 'open' or 'exit'."
            )


if __name__ == "__main__":
    main()
