
import ast
from pathlib import Path


def fix_code(code, bug_type=None):
    fixed_code = code
    fixes = []

    # Fix unsafe eval()
    if bug_type in (None, "UnsafeFunction"):
        if "eval(" in fixed_code:
            fixed_code = fixed_code.replace(
                "eval(", "ast.literal_eval("
            )

            # Add ast import if it is missing
            if "import ast" not in fixed_code:
                fixed_code = "import ast\n" + fixed_code

            fixes.append(
                "Replaced eval() with ast.literal_eval(). "
                "Validation is required."
            )

    # Fix simple division by zero
    if bug_type in (None, "DivisionByZero"):
        if "/ 0" in fixed_code:
            fixed_code = fixed_code.replace("/ 0", "/ 1")

            fixes.append(
                "Replaced division by zero with division by one. "
                "Please review the result."
            )

    # Undefined variables cannot be safely guessed
    if bug_type == "UndefinedVariable":
        fixes.append(
        "Undefined variable detected. "
        "Manual correction required: define the variable "
        "with its intended value."
    )

    return {
        "success": bool(fixes),
        "fixed_code": fixed_code,
        "fixes": fixes
    }


def save_fixed_code(fixed_code, output_file="fixed_code.py"):
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(
            fixed_code,
            encoding="utf-8"
        )

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
