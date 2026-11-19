
import subprocess
import sys


def run_tests(test_file):
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v"],
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
