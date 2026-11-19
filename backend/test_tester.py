
from tester import run_tests

result = run_tests("sample_test.py")

print("\nTESTER RESULTS")
print("=" * 40)

print("Success:", result["success"])

if result["success"]:
    print("Summary: All tests passed.")
else:
    print("Summary: Some tests failed.")

print("Output:")
print(result["output"])

print("Error:", result["error"])
