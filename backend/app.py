
from flask import Flask, request, jsonify
from analyzer import detect_bugs
from repair import fix_code, save_fixed_code

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to AutoPatch API",
        "status": "running"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("code"), str):
        return jsonify({
            "success": False,
            "error": "Please provide Python code."
        }), 400

    code = data["code"]

    if not code.strip():
        return jsonify({
            "success": False,
            "error": "Code cannot be empty."
        }), 400

    # Detect bugs
    bugs = detect_bugs(code)

    # Generate repair suggestions
    fixed_code = code
    fixes = []

    for bug in bugs:
        result = fix_code(fixed_code, bug["type"])
        fixed_code = result["fixed_code"]
        fixes.extend(result["fixes"])

    # Save generated code
    save_result = None

    if fixes:
        save_result = save_fixed_code(
            fixed_code,
            "backend/fixed_code.py"
        )

    return jsonify({
        "success": True,
        "bugs_found": len(bugs),
        "bugs": bugs,
        "fixes": fixes,
        "fixed_code": fixed_code,
        "save_result": save_result
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
