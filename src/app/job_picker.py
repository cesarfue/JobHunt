import sys
import termios
import tty
from typing import List, Tuple

import requests

from db.db import (
    get_applied_jobs,
    get_pending_jobs,
    mark_job_as_applied,
    mark_job_as_discarded,
)

API_URL = "http://127.0.0.1:5000/api/job"


class JobPicker:
    def __init__(self):
        self.jobs = []
        self.current_index = 0
        self.max_display = 5

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
            if key == "\x1b":
                next_char = sys.stdin.read(1)
                if next_char == "[":
                    arrow = sys.stdin.read(1)
                    if arrow == "A":
                        return "up"
                    elif arrow == "B":
                        return "down"
            return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def clear_screen(self):
        print("\033[2J\033[H", end="")

    def display_jobs(self):
        self.clear_screen()

        print("=" * 80)
        print("  Navigate with ↑/↓ arrows")
        print("=" * 80)
        print()

        if not self.jobs:
            print("  No pending jobs available!")
            print()
            print("  Press 'q' to quit")
            return

        start_idx = max(0, self.current_index - 2)
        end_idx = min(len(self.jobs), start_idx + self.max_display)

        if (
            end_idx - start_idx < self.max_display
            and len(self.jobs) >= self.max_display
        ):
            start_idx = max(0, end_idx - self.max_display)

        visible_jobs = self.jobs[start_idx:end_idx]

        for i, job in enumerate(visible_jobs):
            actual_index = start_idx + i
            job_id, title, company, site, location, url = job

            if actual_index == self.current_index:
                print(
                    f"  → \033[1;36m[{actual_index + 1}/{len(self.jobs)}] {title}\033[0m"
                )
                print(f"    \033[1;36m{company} | {site} | {location}\033[0m")
                print(f"    \033[90m{url}\033[0m")
            else:
                print(f"    [{actual_index + 1}/{len(self.jobs)}] {title}")
                print(f"    {company} | {site} | {location}")
                print(f"    \033[90m{url}...\033[0m")
            print()

        print("=" * 80)
        print("  Commands: [a] Apply  [d] Discard  [l] Later  [q] Quit")
        print("=" * 80)

    def apply_to_job(self, job):
        job_id, title, company, site, location, url = job
        print(f"\n  Applying to {company} - {title}...")
        try:
            response = requests.post(API_URL, json={"url": url}, timeout=10)
            data = response.json()
            status = data.get("status", "unknown")
            print(f"Status: {status}")
            mark_job_as_applied(job_id)
            return True
        except Exception as e:
            print(f"Error while sending url {url}: {e}")
            return False

    def discard_job(self, job):
        job_id = job[0]
        mark_job_as_discarded(job_id)
        print(f"Job discarded")

    def handle_action(self, action):
        if not self.jobs:
            return False

        current_job = self.jobs[self.current_index]

        if action == "a":
            self.apply_to_job(current_job)
            self.jobs.pop(self.current_index)
            if self.current_index >= len(self.jobs) and self.current_index > 0:
                self.current_index -= 1
            input("\n  Press Enter to continue...")
            return True

        elif action == "d":
            self.discard_job(current_job)
            self.jobs.pop(self.current_index)
            if self.current_index >= len(self.jobs) and self.current_index > 0:
                self.current_index -= 1
            input("\n  Press Enter to continue...")
            return True

        elif action == "l":
            if self.current_index < len(self.jobs) - 1:
                self.current_index += 1
            return True

        return False

    def run(self):
        self.jobs = list(get_pending_jobs("DESC"))

        if not self.jobs:
            self.display_jobs()
            self.get_key()
            return

        while True:
            self.display_jobs()

            if not self.jobs:
                print("\n  All jobs processed!")
                input("\n  Press Enter to exit...")
                break

            key = self.get_key()

            if key == "q":
                break
            elif key == "up":
                if self.current_index > 0:
                    self.current_index -= 1
            elif key == "down":
                if self.current_index < len(self.jobs) - 1:
                    self.current_index += 1
            elif key in ["a", "d", "l"]:
                self.handle_action(key)


def list_subs():
    from tabulate import tabulate

    jobs = get_applied_jobs()

    if not jobs:
        print("\n  No applications yet!")
        return

    table = []
    for job in jobs:
        job_id, title, company, site, location, date_added = job
        table.append([job_id, title, company, site, location, date_added])

    print("\n" + "=" * 100)
    print("  SUBS ")
    print("=" * 100 + "\n")
    print(
        tabulate(
            table,
            headers=["ID", "Title", "Company", "Site", "Location", "Applied At"],
            tablefmt="fancy_grid",
        )
    )
    print()


def interactive_job_picker():
    try:
        picker = JobPicker()
        picker.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_subs()
    else:
        interactive_job_picker()
