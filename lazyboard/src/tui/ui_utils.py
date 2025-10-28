import os


def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except (AttributeError, OSError):
        return 80, 24


def truncate_text(text, max_length):
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def get_separator(width=None, char="="):
    if width is None:
        width, _ = get_terminal_size()
    return char * width


def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


class Colors:
    YELLOW = "93"  # Pending
    BLUE = "94"  # WIP
    GREEN = "92"  # Applied
    RED = "91"  # Discarded
    GRAY = "90"  # Muted text
    BOLD_YELLOW = "1;33"
    BOLD_MAGENTA = "1;35"
    RESET = "0"


def get_status_display(status):
    status_lower = status.lower()
    if status_lower == "pending":
        return colorize(status.upper(), Colors.YELLOW)
    elif status_lower == "wip":
        return colorize(status.upper(), Colors.BLUE)
    elif status_lower == "applied":
        return colorize(status.upper(), Colors.GREEN)
    else:
        return colorize(status.upper(), Colors.RED)


def clear_screen():
    print("\033[2J\033[H", end="")


def calculate_column_widths(terminal_width, columns_config):
    fixed_total = 0
    flexible_columns = []

    for name, width_spec, min_width in columns_config:
        if isinstance(width_spec, int):
            fixed_total += width_spec
        else:
            flexible_columns.append((name, width_spec, min_width))

    reserved = 40
    remaining = max(terminal_width - fixed_total - reserved, 30)

    widths = {}
    for name, width_spec, min_width in columns_config:
        if isinstance(width_spec, int):
            widths[name] = width_spec
        else:
            widths[name] = max(int(remaining * width_spec), min_width)

    return widths


def print_header(title, width=None):
    if width is None:
        width, _ = get_terminal_size()

    separator = get_separator(width)
    print("\n" + separator)
    print(f"  {title}")
    print(separator + "\n")


def print_footer(width=None):
    if width is None:
        width, _ = get_terminal_size()
    print(get_separator(width) + "\n")
