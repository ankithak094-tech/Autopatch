
import subprocess
import sys
from pathlib import Path


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
