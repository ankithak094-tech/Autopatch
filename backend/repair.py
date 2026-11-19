
import ast
import builtins
import difflib
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

    # Fix undefined variable names
    if bug_type == "UndefinedVariable":
        try:
            tree = ast.parse(fixed_code)

            defined_variables = {
                node.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Name)
                and isinstance(node.ctx, ast.Store)
            }

            used_variables = {
                node.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Name)
                and isinstance(node.ctx, ast.Load)
            }

            undefined_variables = (
                used_variables
                - defined_variables
                - set(dir(builtins))
            )

            for undefined in undefined_variables:
                matches = difflib.get_close_matches(
                    undefined,
                    defined_variables,
                    n=1,
                    cutoff=0.8
                )

                if len(matches) == 1:
                    correct_name = matches[0]

                    fixed_code = fixed_code.replace(
                        undefined, correct_name
                    )

                    fixes.append(
                        f"Corrected variable typo: "
                        f"{undefined} -> {correct_name}"
                    )
                else:
                    fixes.append(
                        f"Undefined variable detected: {undefined}. "
                        "Manual correction required."
                    )

        except SyntaxError:
            fixes.append(
                "Cannot correct variable names because "
                "the code has a syntax error."
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
