
import ast
from pathlib import Path


def fix_code(code):
    fixed_code = code
    fixes = []

    # Fix 1: Replace eval() with a safer literal_eval()
    if "eval(" in fixed_code:
        fixed_code = fixed_code.replace(
            "eval(", "ast.literal_eval("
        )
        fixes.append("Replaced eval() with ast.literal_eval()")

    # Fix 2: Fix simple division by zero
    if "/ 0" in fixed_code:
        fixed_code = fixed_code.replace(
            "/ 0", "/ 1"
        )
        fixes.append("Replaced division by zero with division by 1")

    return {
        "success": True,
        "fixed_code": fixed_code,
        "fixes": fixes
    }


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
