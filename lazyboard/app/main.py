from prompt_toolkit import PromptSession

from app.commands import open_job_url, show_all_jobs, show_stats
from app.job_picker import interactive_job_picker
from app.ui_utils import get_separator, get_terminal_size
from app.web_parser import add_job_entry
from scraper.scrape import run_scraper


def display_welcome():
    width, _ = get_terminal_size()
    separator = get_separator(min(width, 60))

    print("\n" + separator)
    print("  OverengineeredJobSearch Interactive Shell!")
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
            interactive_job_picker()

        elif cmd == "list":
            show_all_jobs()

        elif cmd == "stats":
            show_stats()

        elif cmd == "fetch":
            run_scraper()

        elif cmd.startswith("add"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 2:
                add_job_entry(parts[1])
            else:
                print("Usage: add <url>")

        elif cmd.startswith("open"):
            parts = cmd.split(maxsplit=1)
            if len(parts) == 2:
                try:
                    job_id = int(parts[1])
                    open_job_url(job_id)
                except ValueError:
                    print("Invalid job ID. Must be a number.")
            else:
                print("Usage: open <job_id>")

        else:
            print("Unknown command. Type 'exit' for available commands or see above.")


if __name__ == "__main__":
    main()
