import sys
import termios
import tty

from app.commands import apply_to_job, discard_job, open_job_url
from app.ui_utils import (
    Colors,
    clear_screen,
    colorize,
    get_separator,
    get_terminal_size,
    truncate_text,
)
from db.db import get_pending_jobs, mark_job_as_applied, mark_job_as_pending


class JobPicker:
    def __init__(self):
        self.jobs = []
        self.current_index = 0
        self._last_terminal_size = None

    def _check_terminal_resize(self):
        current_size = self.get_terminal_size()
        if self._last_terminal_size is None:
            self._last_terminal_size = current_size
            return False
        if current_size != self._last_terminal_size:
            self._last_terminal_size = current_size
            return True
        return False

    @staticmethod
    def get_terminal_size():
        return get_terminal_size()

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
            elif key in ("up", "k"):
                if self.current_index > 0:
                    self.current_index -= 1
            elif key in ("down", "j"):
                if self.current_index < len(self.jobs) - 1:
                    self.current_index += 1
            elif key in ["a", "d", "p", "o"]:
                self.handle_action(key)

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

    def update_status(self, status):
        current_job = list(self.jobs[self.current_index])
        current_job[6] = status
        self.jobs[self.current_index] = current_job

    def display_jobs(self):

        if self._check_terminal_resize():
            pass
        clear_screen()

        width, height = self.get_terminal_size()

        available_lines = max(height - 10, 5)
        max_display = min(available_lines // 4, 7)

        separator = get_separator(width)
        print(separator)
        print("  Navigate with ↑/↓ arrows")
        print(separator)
        print()

        if not self.jobs:
            print("  No pending jobs available!")
            print()
            print("  Press 'q' to quit")
            return

        start_idx = max(0, self.current_index - 2)
        end_idx = min(len(self.jobs), start_idx + max_display)

        if end_idx - start_idx < max_display and len(self.jobs) >= max_display:
            start_idx = max(0, end_idx - max_display)

        visible_jobs = self.jobs[start_idx:end_idx]

        url_width = max(width - 10, 30)
        title_width = max(width - 20, 40)
        info_width = max(width - 10, 50)

        for i, job in enumerate(visible_jobs):
            actual_index = start_idx + i
            id, title, company, site, location, url, status = job

            color_code = (
                Colors.BOLD_YELLOW if status == "pending" else Colors.BOLD_MAGENTA
            )

            title_display = truncate_text(title, title_width)
            url_display = truncate_text(url, url_width)
            info_display = truncate_text(f"{company} | {site} | {location}", info_width)

            if actual_index == self.current_index:
                print(
                    f"  → {colorize(f'[{actual_index + 1}/{len(self.jobs)}] {title_display}', color_code)}"
                )
                print(f"    {colorize(info_display, color_code)}")
                print(f"    {colorize(url_display, Colors.GRAY)}")
            else:
                print(f"    [{actual_index + 1}/{len(self.jobs)}] {title_display}")
                print(f"    {info_display}")
                print(f"    {colorize(url_display, Colors.GRAY)}")
            print()

        self._display_footer(width)

    def _display_footer(self, width):
        _, _, _, _, _, _, status = self.jobs[self.current_index]
        separator = get_separator(width)

        print(separator)

        if width < 80:
            action = "Set to WIP" if status == "pending" else "Set to applied"
            print(f"  {'WIP' if status == 'wip' else 'Pending'} job")
            print(f"  [a] {action}")
            if status == "wip":
                print(f"  [p] Set to pending")
            print(f"  [d] Discard  [o] Open  [q] Quit")
        else:
            footer = f"  {'WIP' if status == 'wip' else 'Pending'} job: [a] "
            footer += "Set to WIP" if status == "pending" else "Set to applied"
            if status == "wip":
                footer += "\t[p] Set to pending"
            footer += "\t[d] Discard\t\n\t\t[o] Open in browser\t[q] Quit"
            print(footer)

        print(separator)

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


def interactive_job_picker():
    try:
        picker = JobPicker()
        picker.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    interactive_job_picker()
