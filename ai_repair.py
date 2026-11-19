
import os
import re
from groq import Groq
from dotenv import load_dotenv

# =====================================
# 1. GROQ API CONFIGURATION
# =====================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-120b"


# =====================================
# 2. AI CODE ANALYSIS AND REPAIR
# =====================================

def analyze_and_repair(code, errors="No errors provided"):

    prompt = f"""
You are AutoPatch, an expert Python debugging AI.

Analyze the following Python code.

ORIGINAL CODE:
{code}

DETECTED ERRORS:
{errors}

Your tasks:
1. Identify all possible bugs.
2. Explain why each bug occurs.
3. Generate complete corrected Python code.
4. Preserve original functionality.
5. Do not invent requirements.
6. If expected behavior is unclear, mention your assumptions.

Return ONLY valid JSON in this format:

{{
    "bug_analysis": "Explain detected bugs",
    "fixed_code": "Complete corrected Python code",
    "explanation": "Explain all corrections"
}}

IMPORTANT:
- fixed_code must contain only Python source code.
- Do not put Markdown code fences inside fixed_code.
- Always include all three fields.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are AutoPatch, an expert Python code repair assistant. Return valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content


# =====================================
# 3. EXTRACT FIXED CODE
# =====================================

def extract_fixed_code(ai_response):

    import json

    try:
        data = json.loads(ai_response)

        fixed_code = data.get("fixed_code", "")

        if fixed_code.strip():
            return fixed_code.strip()

    except (json.JSONDecodeError, AttributeError):
        pass

    # Fallback: Extract Python markdown code block

    pattern = r"```(?:python)?\s*([\s\S]*?)```"

    matches = re.findall(
        pattern,
        ai_response,
        re.IGNORECASE
    )

    if matches:
        for code in matches:
            if code.strip():
                return code.strip()

    raise ValueError("Fixed Python code not found in AI response.")


# =====================================
# 4. EXTRACT BUG ANALYSIS
# =====================================

def get_bug_analysis(ai_response):

    import json

    try:
        data = json.loads(ai_response)
        return data.get("bug_analysis", "No analysis available.")

    except (json.JSONDecodeError, AttributeError):
        return "Unable to extract bug analysis."


# =====================================
# 5. EXTRACT EXPLANATION
# =====================================

def get_explanation(ai_response):

    import json

    try:
        data = json.loads(ai_response)
        return data.get("explanation", "No explanation available.")

    except (json.JSONDecodeError, AttributeError):
        return "Unable to extract explanation."


# =====================================
# 6. SAVE REPAIRED CODE
# =====================================

def save_fixed_code(fixed_code):

    with open(
        "repaired_code.py",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(fixed_code)

    print("\nFixed code saved as repaired_code.py")


# =====================================
# 7. EXPLAIN BUG
# =====================================

def explain_bug(code, error):

    prompt = f"""
Explain this Python bug in simple language.

CODE:
{code}

ERROR:
{error}

Explain:
1. What is the error?
2. Why did it happen?
3. How can it be fixed?
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# =====================================
# 8. RETRY CODE REPAIR
# =====================================

def retry_repair(code, error, previous_fix):

    prompt = f"""
The previous AI repair failed testing.

ORIGINAL CODE:
{code}

ERROR:
{error}

PREVIOUS REPAIR:
{previous_fix}

Generate an improved complete corrected Python solution.

Return valid JSON:
{{
    "bug_analysis": "Analysis",
    "fixed_code": "Complete Python code",
    "explanation": "Corrections made"
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content


# =====================================
# 9. MAIN TESTING
# =====================================

if __name__ == "__main__":

    sample_code = """
def divide(a, b):
    return a / b

print(divide(10, 0))
"""

    detected_errors = "Division by zero error"

    print("\n================================")
    print("       AUTOPATCH AI")
    print("================================")

    print("\nAnalyzing Python code...")

    # Get Groq AI response
    result = analyze_and_repair(
        sample_code,
        detected_errors
    )

    # Display bug analysis
    print("\n========== BUG ANALYSIS ==========")
    print(get_bug_analysis(result))

    # Extract corrected code
    fixed_code = extract_fixed_code(result)

    print("\n========== FIXED CODE ==========")
    print(fixed_code)

    # Display explanation
    print("\n========== EXPLANATION ==========")
    print(get_explanation(result))

    # Save corrected code
    save_fixed_code(fixed_code)

    print("\n================================")
    print("       REPAIR COMPLETED")
    print("================================")
