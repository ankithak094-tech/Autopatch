
from analyzer import detect_bugs
from repair import fix_code, save_fixed_code
from tester import validate_fixed_code


def run_autopatch(code):

    original_code = code

    # Step 1: Detect bugs
    bugs = detect_bugs(code)

    print("\nDETECTED BUGS:")

    if bugs:
        for bug in bugs:
            print(bug)
    else:
        print("No bugs detected.")

    # Step 2: Generate repair candidates
    fixed_code = code
    all_fixes = []

    for bug in bugs:
        result = fix_code(fixed_code, bug["type"])
        fixed_code = result["fixed_code"]
        all_fixes.extend(result["fixes"])

    print("\nSUGGESTED FIXES:")

    if all_fixes:
        for fix in all_fixes:
            print("-", fix)
    else:
        print("No fixes required.")

    # Step 3: Validate candidate code
    print("\nVALIDATING REPAIRED CODE:")

    validation = validate_fixed_code(fixed_code)

    print("Validation successful:", validation["success"])

    # Step 4: Save only if validation succeeds
    if all_fixes and validation["success"]:

        save_result = save_fixed_code(
            fixed_code,
            "backend/fixed_code.py"
        )

        print("\nSAVE RESULT:")
        print(save_result)

    else:
        fixed_code = original_code
        save_result = None

        print("\nRepair was not saved.")
        print("Original code has been preserved.")

    return {
        "bugs": bugs,
        "fixed_code": fixed_code,
        "fixes": all_fixes,
        "validation": validation,
        "save_result": save_result
    }


if __name__ == "__main__":

    sample_code = """
total=100
print(totla)
"""

    print("\nCODE BEING TESTED:")
    print(sample_code)

    run_autopatch(sample_code)
