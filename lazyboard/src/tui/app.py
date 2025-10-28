from prompt_toolkit import PromptSession

from src.scrapers.scraper_commands import run_scraper
from src.scrapers.url_importer import add_job_from_url
from src.services.job_service import JobService
from src.tui.commands import CommandHandler
from src.tui.job_picker import JobPicker
from src.tui.ui_utils import get_separator, get_terminal_size


def display_welcome():
    width, _ = get_terminal_size()
    separator = get_separator(min(width, 60))

    print("\n" + separator)
    print("  Lazyboard - Job Application Tracker")
    print(separator)
    print("\n  Available commands:")
    print("    start          - Start reviewing pending jobs")
    print("    list           - Show all jobs with status")
    print("    stats          - Show job statistics")
    print("    fetch          - Fetch new jobs")
    print("    open <id>      - Open job page in browser")
    print("    add <url>      - Add a job from URL")
    print("    exit           - Quit the application")
    print()


def main():
    job_service = JobService()
    command_handler = CommandHandler(job_service)

    session = PromptSession()
    display_welcome()

    while True:
        try:
            cmd = session.prompt("> ").strip()
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        if not cmd:
            continue

        if cmd == "exit":
            break

        elif cmd == "start":
            picker = JobPicker(job_service)
            try:
                picker.run()
            except KeyboardInterrupt:
                pass

        elif cmd == "list":
            command_handler.show_all_jobs()

        elif cmd == "stats":
            command_handler.show_stats()

        elif cmd == "fetch":
            run_scraper(job_service)

        elif cmd.startswith("add"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 2:
                add_job_from_url(parts[1], job_service)
            else:
                print("Usage: add <url>")

        elif cmd.startswith("open"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 2:
                try:
                    job_id = int(parts[1])
                    command_handler.open_job_url(job_id)
                except ValueError:
                    print("Invalid job ID. Must be a number.")
            else:
                print("Usage: open <job_id>")

        else:
            print(
                "Unknown command. Available: start, list, stats, fetch, add, open, exit"
            )


if __name__ == "__main__":
    main()
