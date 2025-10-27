import sys
import termios
import tty

import requests

from db.db import (
    get_pending_jobs,
    mark_job_as_applied,
    mark_job_as_discarded,
    mark_job_as_pending,
    mark_job_as_wip,
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

    def update_status(self, status):
        current_job = list(self.jobs[self.current_index])
        current_job[6] = status
        self.jobs[self.current_index] = current_job

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
            job_id, title, company, site, location, url, status = job  # include id

            if status == "pending":
                color_code = "\033[1;33m"  # yellow
            else:
                color_code = "\033[1;35m"  # purple

            if actual_index == self.current_index:
                print(
                    f"  → {color_code}[{actual_index + 1}/{len(self.jobs)}] {title}\033[0m"
                )
                print(f"    {color_code}{company} | {site} | {location}\033[0m")
                print(f"    \033[90m{url}\033[0m")
            else:
                print(f"    [{actual_index + 1}/{len(self.jobs)}] {title}")
                print(f"    {company} | {site} | {location}")
                print(f"    \033[90m{url}\033[0m")
            print()

        _, _, _, _, _, _, status = self.jobs[self.current_index]
        print("=" * 80)
        footer = f"  {'WIP' if status == 'wip' else 'Pending'} job: [a] "
        footer += "Set to WIP" if status == "pending" else "Set to applied"
        if status == "wip":
            footer += "\t[p] Set to pending"
        footer += "\t[d] Discard \t[q] Quit"

        print(footer)
        print("=" * 80)

    def apply_to_job(self, job):
        job_id, title, company, site, location, url, status = job
        print(f"\n  Applying to {company} - {title}...")
        try:
            requests.post(API_URL, json={"url": url}, timeout=60)
            mark_job_as_wip(job_id)
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
        _, _, _, _, _, _, status = self.jobs[self.current_index]

        if status == "pending":
            if action == "a":
                self.apply_to_job(current_job)
                self.update_status("wip")
                return True

        elif status == "wip":
            if action == "a":
                mark_job_as_applied(current_job[0])
                self.update_status("applied")
                self.jobs.pop(self.current_index)
                if self.current_index >= len(self.jobs) and self.current_index > 0:
                    self.current_index -= 1
                return True
            elif action == "p":
                mark_job_as_pending(current_job[0])
                self.update_status("pending")

        elif action == "d":
            self.discard_job(current_job)
            self.jobs.pop(self.current_index)
            if self.current_index >= len(self.jobs) and self.current_index > 0:
                self.current_index -= 1
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
            elif key == "up" or key == "j":
                if self.current_index > 0:
                    self.current_index -= 1
            elif key == "down" or key == "k":
                if self.current_index < len(self.jobs) - 1:
                    self.current_index += 1
            elif key in ["a", "d", "p"]:
                self.handle_action(key)


def interactive_job_picker():
    try:
        picker = JobPicker()
        picker.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    interactive_job_picker()
