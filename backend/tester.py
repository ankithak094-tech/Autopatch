
import subprocess
import sys
from pathlib import Path


def run_tests(test_file, timeout=30):
    try:
        test_path = Path(test_file)

        if not test_path.is_absolute():
            test_path = Path(__file__).parent / test_path

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(test_path),
                "-v",
                "--tb=short"
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = result.stdout + "\n" + result.stderr

        summary = ""
        for line in output.splitlines():
            if " passed" in line or " failed" in line:
                summary = line.strip()

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "summary": summary,
            "output": output,
            "error": ""
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "return_code": -1,
            "summary": "Tests timed out",
            "output": "",
            "error": f"Tests exceeded the {timeout}-second time limit."
        }

    except Exception as error:
        return {
            "success": False,
            "return_code": -1,
            "summary": "Test execution error",
            "output": "",
            "error": str(error)
        }
