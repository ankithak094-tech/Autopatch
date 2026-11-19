import ast
import os
import tempfile
from pylint.lint import Run
from pylint.reporters import CollectingReporter


def detect_bugs(code):
    bugs = []

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return [{
            "line": error.lineno or 0,
            "type": "SyntaxError",
            "message": error.msg
        }]

    # AST-based checks
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, (ast.Div, ast.FloorDiv)):
                if (
                    isinstance(node.right, ast.Constant)
                    and node.right.value == 0
                ):
                    bugs.append({
                        "line": node.lineno,
                        "type": "DivisionByZero",
                        "message": "Division by zero detected."
                    })

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "eval":
                bugs.append({
                    "line": node.lineno,
                    "type": "UnsafeFunction",
                    "message": "Use of eval() can execute unsafe code."
                })

    # Pylint-based checks
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            encoding="utf-8",
            delete=False
        ) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name

        reporter = CollectingReporter()

        Run(
            [
                temp_path,
                "--disable=all",
                "--enable=undefined-variable,unused-variable",
                "--reports=n",
                "--score=n"
            ],
            reporter=reporter,
            exit=False
        )

        for message in reporter.messages:
            if message.symbol == "undefined-variable":
                bug_type = "UndefinedVariable"
            elif message.symbol == "unused-variable":
                bug_type = "UnusedVariable"
            else:
                continue

            bugs.append({
                "line": message.line,
                "type": bug_type,
                "message": message.msg
            })

    except Exception as error:
        print("Pylint error:", error)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    return bugs