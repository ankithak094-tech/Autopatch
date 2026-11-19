import os
import sys
import ast
from flask import Flask, request, jsonify

app = Flask(__name__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from analyzer import detect_bugs
from repair import fix_code, save_fixed_code
from sandbox import run_in_sandbox

try:
    from .database import save_submission, get_history, get_submission
except ImportError:
    from database import save_submission, get_history, get_submission


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/", methods=["GET"])
def home():
    return jsonify(success=True, message="Welcome to AutoPatch API")


@app.route("/health", methods=["GET"])
def health():
    return jsonify(success=True, status="healthy",
                   message="AutoPatch backend is running.")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    code = data.get("code")
    if not isinstance(code, str) or not code.strip():
        return jsonify(success=False, error="Code cannot be empty."), 400

    try:
        bugs = detect_bugs(code)
        fixed_code = code
        fixes = []

        for bug in bugs:
            result = fix_code(fixed_code, bug.get("type"))
            fixed_code = result.get("fixed_code", fixed_code)
            fixes.extend(result.get("fixes", []))

        validation = run_in_sandbox(fixed_code) if fixes else None
        save_result = None

        if fixes:
            save_result = save_fixed_code(
                fixed_code, os.path.join(BACKEND_DIR, "fixed_code.py")
            )

        submission_id = save_submission(
            original_code=code,
            repair_mode="rule_based",
            bugs=bugs,
            fixed_code=fixed_code if fixes else None,
            validation=validation or {}
        )

        return jsonify(
            success=True,
            submission_id=submission_id,
            bugs_found=len(bugs),
            bugs=bugs,
            fixes=fixes,
            fixed_code=fixed_code,
            runtime_validation=validation,
            save_result=save_result,
            database_saved=True
        )
    except Exception as exc:
        app.logger.exception("Analyze failed")
        return jsonify(success=False, error=str(exc)), 500


@app.route("/ai-repair", methods=["POST"])
def ai_repair():
    data = request.get_json(silent=True) or {}
    code = data.get("code")
    if not isinstance(code, str) or not code.strip():
        return jsonify(success=False, error="Please provide Python code."), 400

    try:
        from ai_repair import (
            analyze_and_repair, retry_repair, extract_fixed_code,
            get_bug_analysis, get_explanation
        )

        bugs = detect_bugs(code)
        errors = "\n".join(b.get("message", "") for b in bugs)
        if not errors:
            errors = "No errors detected by static analysis."

        ai_response = analyze_and_repair(code, errors)
        fixed_code = extract_fixed_code(ai_response)
        bug_analysis = get_bug_analysis(ai_response)
        explanation = get_explanation(ai_response)

        ast.parse(fixed_code)
        validation = run_in_sandbox(fixed_code)

        retry_count = 0
        max_retries = 2
        while not validation.get("success") and retry_count < max_retries:
            retry_count += 1
            previous_error = validation.get("error") or "Program execution failed."
            ai_response = retry_repair(code, previous_error, fixed_code)
            fixed_code = extract_fixed_code(ai_response)
            bug_analysis = get_bug_analysis(ai_response)
            explanation = get_explanation(ai_response)
            ast.parse(fixed_code)
            validation = run_in_sandbox(fixed_code)

        save_result = None
        if validation.get("success"):
            save_result = save_fixed_code(
                fixed_code, os.path.join(BACKEND_DIR, "ai_fixed_code.py")
            )

        submission_id = save_submission(
            original_code=code,
            repair_mode="groq_ai",
            bugs=bugs,
            fixed_code=fixed_code,
            bug_analysis=bug_analysis,
            explanation=explanation,
            retry_count=retry_count,
            validation=validation
        )

        return jsonify(
            success=bool(validation.get("success")),
            submission_id=submission_id,
            repair_type="Groq AI with Automatic Retry",
            bugs_found=len(bugs),
            bugs=bugs,
            bug_analysis=bug_analysis,
            explanation=explanation,
            fixed_code=fixed_code,
            runtime_validation=validation,
            retry_count=retry_count,
            max_retries=max_retries,
            save_result=save_result,
            database_saved=True
        )
    except SyntaxError as exc:
        return jsonify(success=False,
                       error="AI generated code contains a syntax error.",
                       details=str(exc)), 422
    except ValueError as exc:
        return jsonify(success=False, error=str(exc)), 400
    except Exception as exc:
        app.logger.exception("AI repair failed")
        return jsonify(success=False, error=str(exc)), 500


@app.route("/validate", methods=["POST"])
def validate_code():
    data = request.get_json(silent=True) or {}
    code = data.get("code")
    if not isinstance(code, str) or not code.strip():
        return jsonify(success=False,
                       error="Please provide non-empty Python code."), 400
    try:
        result = run_in_sandbox(code)
        submission_id = save_submission(
            original_code=code,
            repair_mode="manual_validation",
            validation=result
        )
        return jsonify(
            success=bool(result.get("success")),
            output=result.get("output", ""),
            error=result.get("error", ""),
            submission_id=submission_id,
            database_saved=True
        )
    except Exception as exc:
        app.logger.exception("Validation failed")
        return jsonify(success=False, error=str(exc)), 500


@app.route("/history", methods=["GET"])
def history():
    try:
        records = get_history()
        return jsonify(success=True, total=len(records), history=records)
    except Exception as exc:
        app.logger.exception("History retrieval failed")
        return jsonify(success=False, error=str(exc)), 500


@app.route("/history/<int:submission_id>", methods=["GET"])
def history_detail(submission_id):
    try:
        record = get_submission(submission_id)
        if record is None:
            return jsonify(success=False, error="Submission not found."), 404
        return jsonify(success=True, record=record)
    except Exception as exc:
        app.logger.exception("History detail failed")
        return jsonify(success=False, error=str(exc)), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
