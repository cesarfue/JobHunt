import shutil
import traceback
from pathlib import Path

from config import Config


def make_letter(folder_path):
    folder_path = Path(folder_path)
    try:
        source_path = Config.LETTER_FILE
        output_path = folder_path

        print(f"source : {source_path}, output: {output_path}")
        if not source_path.exists():
            print(f"Error: Letter file not found: {source_path}")
            return

        if source_path != output_path:
            shutil.copy2(source_path, output_path)

    except Exception as e:
        print(f"Error: failed to copy letter: {e}")
        traceback.print_exc()
