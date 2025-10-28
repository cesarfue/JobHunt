import webbrowser

from tabulate import tabulate

from src.services.job_service import JobService
from src.tui.ui_utils import (
    Colors,
    calculate_column_widths,
    colorize,
    get_status_display,
    get_terminal_size,
    print_footer,
    print_header,
    truncate_text,
)


class CommandHandler:
    def __init__(self, job_service: JobService):
        self.job_service = job_service

    def show_all_jobs(self):
        jobs = self.job_service.get_all_jobs()
        if not jobs:
            print("\nNo jobs in database!")
            return

        width, _ = get_terminal_size()

        all_columns = [
            ("id", "ID", 5, 0),
            ("title", "Title", 40, 0),
            ("company", "Company", 20, 60),
            ("site", "Site", 5, 60),
            ("location", "Location", 15, 100),
            ("date", "Date added", 12, 120),
            ("status", "Status", 12, 0),
        ]

        visible_columns = []
        headers = []

        for col_name, display_name, col_width, min_width in all_columns:
            if width >= min_width:
                visible_columns.append((col_name, col_width))
                headers.append(display_name)

        flexible_config = []
        for col_name, col_width in visible_columns:
            if col_name == "title":
                flexible_config.append((col_name, 0.5, 20))
            elif col_name == "company":
                flexible_config.append((col_name, 0.3, 10))
            elif col_name == "location":
                flexible_config.append((col_name, 0.2, 10))
            elif col_name == "site":
                flexible_config.append((col_name, 0.2, 10))
            else:
                flexible_config.append((col_name, col_width, col_width))

        widths = calculate_column_widths(width, flexible_config)

        table = []
        for job in jobs:
            row = []
            for col_name, _ in visible_columns:
                if col_name == "id":
                    row.append(job.id)
                elif col_name == "title":
                    row.append(truncate_text(job.title, widths["title"]))
                elif col_name == "company":
                    row.append(truncate_text(job.company, widths["company"]))
                elif col_name == "site":
                    row.append(truncate_text(job.site, widths["site"]))
                elif col_name == "location":
                    row.append(truncate_text(job.location, widths["location"]))
                elif col_name == "date":
                    row.append(
                        job.date_added.strftime("%Y-%m-%d") if job.date_added else ""
                    )
                elif col_name == "status":
                    row.append(get_status_display(job.status.value))

            table.append(row)

        print_header("ALL JOBS", width)
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        print(f"\n  Total: {len(jobs)} jobs")
        print_footer(width)

    def show_stats(self):
        width, _ = get_terminal_size()
        stats = self.job_service.get_statistics()

        box_width = min(50, width - 4)

        print_header("JOB STATISTICS", box_width)
        print(f"  {colorize('Pending:', Colors.YELLOW)}    {stats['pending']}")
        print(f"  {colorize('WIP:', Colors.BLUE)}        {stats['wip']}")
        print(f"  {colorize('Applied:', Colors.GREEN)}    {stats['applied']}")
        print(f"  {colorize('Discarded:', Colors.RED)}  {stats['discarded']}")
        print(f"  Total:      {stats['total']}")
        print_footer(box_width)

    def open_job_url(self, job_id: int):
        job = self.job_service.get_job(job_id)
        if job:
            webbrowser.open(job.url)
        else:
            print(f"No job found with id {job_id}")
