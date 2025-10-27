import sys

from prompt_toolkit import PromptSession
from tabulate import tabulate

from app.job_picker import interactive_job_picker, list_applications
from db.db import get_all_jobs, get_applied_jobs, get_pending_jobs


def show_all_jobs():
    jobs = get_all_jobs()
    if not jobs:
        print("\nNo jobs in database!")
        return

    table = []
    for job in jobs:
        job_id, title, company, site, location, status, score = job
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
                score,
                status_display,
            ]
        )

    print("\n" + "=" * 120)
    print("  ALL JOBS")
    print("=" * 120 + "\n")
    print(
        tabulate(
            table,
            headers=["ID", "Title", "Company", "Site", "Location", "Score", "Status"],
            tablefmt="fancy_grid",
        )
    )
    print(f"\n  Total: {len(jobs)} jobs\n")


def show_stats():
    all_jobs = get_all_jobs()
    applied = sum(1 for job in all_jobs if job[5] == "applied")
    discarded = sum(1 for job in all_jobs if job[5] == "discarded")
    pending = sum(1 for job in all_jobs if job[5] == "pending")

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
    print("  Welcome to JobHunter Interactive Shell!")
    print("=" * 60)
    print("\n  Available commands:")
    print("    start          - Start reviewing pending jobs")
    print("    applications   - List all applied jobs")
    print("    list           - Show all jobs with status")
    print("    stats          - Show job statistics")
    print("    exit           - Quit the application")
    print()

    while True:
        try:
            cmd = session.prompt("> ").strip().lower()
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        if cmd == "exit":
            print("Goodbye!")
            break

        elif cmd == "start":
            interactive_job_picker()

        elif cmd == "applications":
            list_applications()

        elif cmd == "list":
            show_all_jobs()

        elif cmd == "stats":
            show_stats()

        else:
            print(
                "Unknown command. Type 'start', 'applications', 'list', 'stats', or 'exit'."
            )


if __name__ == "__main__":
    main()
