from prompt_toolkit import PromptSession
from tabulate import tabulate

from app.commands import open_job_url, show_all_jobs, show_stats
from app.job_picker import interactive_job_picker
from app.web_parser import add_job_entry
from scraper.scrape import run_scraper


def main():
    session = PromptSession()

    print("\n" + "=" * 60)
    print("  OverengineeredJobSearch Interactive Shell!")
    print("=" * 60)
    print("\n  Available commands:")
    print("    start          - Start reviewing pending jobs")
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
                "Unknown command. Type 'start', 'list', 'stats', 'add', 'open' or 'exit'."
            )


if __name__ == "__main__":
    main()
