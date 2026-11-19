
from pathlib import Path


def save_fixed_code(fixed_code, output_file="fixed_code.py"):
    try:
        output_path = Path(output_file)
        output_path.write_text(fixed_code, encoding="utf-8")

        return {
            "success": True,
            "file": str(output_path),
            "message": "Fixed code saved successfully."
        }

    except OSError as error:
        return {
            "success": False,
            "file": None,
            "message": str(error)
        }
