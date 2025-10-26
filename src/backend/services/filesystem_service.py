import platform
import subprocess

from config import Config


def create_folder(company, today):
    base_folder_name = f"{company} - {today}"
    folder_path = Config.APPLICATIONS_DIR / base_folder_name
    counter = 1
    while folder_path.exists():
        folder_name = f"{base_folder_name} ({counter})"
        folder_path = Config.APPLICATIONS_DIR / folder_name
        counter += 1

    folder_path.mkdir(parents=True, exist_ok=True)
    return str(folder_path.absolute())


def open_folder_in_explorer(folder_path):
    try:
        system = platform.system()
        if system == "Windows":
            subprocess.run(["explorer", str(folder_path)])
        elif system == "Darwin":
            subprocess.run(["open", str(folder_path)])
        else:
            subprocess.run(["xdg-open", str(folder_path)])
        return True
    except Exception as e:
        print(f"Error opening folder: {e}")
        return False
