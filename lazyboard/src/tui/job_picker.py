import sys
import termios
import tty

from src.services.job_service import JobService
from src.tui.ui_utils import (
    Colors,
    clear_screen,
    colorize,
    get_separator,
    get_terminal_size,
    truncate_text,
)


class JobPicker:

    def __init__(self, job_service: JobService):
        self.job_service = job_service
        self.jobs = []
        self.current_index = 0
        self._last_terminal_size = None

    def _check_terminal_resize(self):
        current_size = get_terminal_size()
        if self._last_terminal_size is None:
            self._last_terminal_size = current_size
            return False
        if current_size != self._last_terminal_size:
            self._last_terminal_size = current_size
            return True
        return False

    def run(self):
        self.jobs = self.job_service.get_pending_jobs("DESC")

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

    def display_jobs(self):
        if self._check_terminal_resize():
            pass
        clear_screen()

        width, height = get_terminal_size()

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

            color_code = Colors.BOLD_YELLOW if job.is_pending else Colors.BOLD_MAGENTA

            title_display = truncate_text(job.title, title_width)
            url_display = truncate_text(job.url, url_width)
            info_display = truncate_text(
                f"{job.company} | {job.site} | {job.location}", info_width
            )

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
        current_job = self.jobs[self.current_index]
        separator = get_separator(width)

        print(separator)

        if width < 80:
            action = "Set to WIP" if current_job.is_pending else "Set to applied"
            print(f"  {'WIP' if current_job.is_wip else 'Pending'} job")
            print(f"  [a] {action}")
            if current_job.is_wip:
                print(f"  [p] Set to pending")
            print(f"  [d] Discard  [o] Open  [q] Quit")
        else:
            footer = f"  {'WIP' if current_job.is_wip else 'Pending'} job: [a] "
            footer += "Set to WIP" if current_job.is_pending else "Set to applied"
            if current_job.is_wip:
                footer += "\t[p] Set to pending"
            footer += "\t[d] Discard\t\n\t\t[o] Open in browser\t[q] Quit"
            print(footer)

        print(separator)

    def handle_action(self, action):
        if not self.jobs:
            return False

        current_job = self.jobs[self.current_index]

        if action == "a":
            if current_job.is_pending:
                self.job_service.apply_to_job(current_job)
                self.jobs[self.current_index] = self.job_service.get_job(current_job.id)
                return True
            elif current_job.is_wip:
                self.job_service.mark_as_applied(current_job.id)
                self.jobs.pop(self.current_index)
                if self.current_index >= len(self.jobs) and self.current_index > 0:
                    self.current_index -= 1
                return True

        elif action == "p" and current_job.is_wip:
            self.job_service.mark_as_pending(current_job.id)
            self.jobs[self.current_index] = self.job_service.get_job(current_job.id)
            return True

        elif action == "o":
            import webbrowser

            webbrowser.open(current_job.url)
            return True

        elif action == "d":
            self.job_service.mark_as_discarded(current_job.id)
            print(f"Job discarded")
            self.jobs.pop(self.current_index)
            if self.current_index >= len(self.jobs) and self.current_index > 0:
                self.current_index -= 1
            return True

        return False
