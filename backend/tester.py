
import subprocess
import sys
import tempfile
import os
from pathlib import Path


# Function 1: Run automated test files
def run_tests(test_file):
    try:
        test_path = Path(test_file)

        if not test_path.is_absolute():
            test_path = Path(__file__).parent / test_path

        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_path), "-v"],
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Tests timed out after 30 seconds."
        }

    except Exception as error:
        return {
            "success": False,
            "output": "",
            "error": str(error)
        }


# Function 2: Validate repaired Python code
def validate_fixed_code(code):
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

        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Code execution timed out."
        }

    except Exception as error:
        return {
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
