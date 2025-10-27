import sys
import termios
import tty

from app.commands import apply_to_job, discard_job, open_job_url
from db.db import get_pending_jobs, mark_job_as_applied, mark_job_as_pending


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
            job_id, title, company, site, location, url, status = job

            if status == "pending":
                color_code = "\033[1;33m"
            else:
                color_code = "\033[1;35m"

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
        footer += "\t[d] Discard\t\n\t\t[o] Open in browser\t[q] Quit"

        print(footer)
        print("=" * 80)

    def handle_action(self, action):
        if not self.jobs:
            return False

        current_job = self.jobs[self.current_index]
        _, _, _, _, _, _, status = self.jobs[self.current_index]

        if status == "pending":
            if action == "a":
                apply_to_job(current_job)
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

        if action == "o":
            open_job_url(current_job[0])
            return True

        elif action == "d":
            discard_job(current_job)
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
                break

            key = self.get_key()

            if key == "q":
                break
            elif key == "up" or key == "k":
                if self.current_index > 0:
                    self.current_index -= 1
            elif key == "down" or key == "j":
                if self.current_index < len(self.jobs) - 1:
                    self.current_index += 1
            elif key in ["a", "d", "p", "o"]:
                self.handle_action(key)


def interactive_job_picker():
    try:
        picker = JobPicker()
        picker.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    interactive_job_picker()
