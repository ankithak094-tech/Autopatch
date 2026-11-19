
from analyzer import detect_bugs
from repair import fix_code, save_fixed_code
from tester import validate_fixed_code


def run_autopatch(code):

    # Step 1: Detect bugs
    bugs = detect_bugs(code)

    print("\nDETECTED BUGS:")
    if bugs:
        for bug in bugs:
            print(bug)
    else:
        print("No bugs detected.")

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

    # Step 4: Validate the generated code
    print("\nVALIDATING FIXED CODE:")

    validation = validate_fixed_code(fixed_code)

    print("Validation successful:", validation["success"])

    if validation["output"]:
        print("Program output:")
        print(validation["output"])

    if validation["error"]:
        print("Validation error:")
        print(validation["error"])

    # Step 5: Save generated code for review
    save_result = None

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
        "fixes": all_fixes,
        "validation": validation,
        "save_result": save_result
    }


if __name__ == "__main__":

    sample_code = """
x = 10 / 0
print(unknown_variable)
"""

    run_autopatch(sample_code)
