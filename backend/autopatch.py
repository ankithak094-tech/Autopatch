
from analyzer import detect_bugs
from repair import fix_code, save_fixed_code


def run_autopatch(code):
    # Step 1: Detect bugs
    bugs = detect_bugs(code)

    print("\nDETECTED BUGS:")
    for bug in bugs:
        print(bug)

    # Step 2: Generate fixes
    fixed_code = code
    all_fixes = []

    for bug in bugs:
        result = fix_code(fixed_code, bug["type"])
        fixed_code = result["fixed_code"]
        all_fixes.extend(result["fixes"])

    # Step 3: Display suggested fixes
    print("\nSUGGESTED FIXES:")
    if all_fixes:
        for fix in all_fixes:
            print("-", fix)
    else:
        print("No fixes required.")

    # Step 4: Save corrected code
    if all_fixes:
        save_result = save_fixed_code(
            fixed_code,
            "backend/fixed_code.py"
        )
        print("\nSAVE RESULT:")
        print(save_result)

    return {
        "bugs": bugs,
        "fixed_code": fixed_code,
        "fixes": all_fixes
    }


if __name__ == "__main__":
    sample_code = """
x = 10 / 0
print(unknown_variable)
"""

    run_autopatch(sample_code)
