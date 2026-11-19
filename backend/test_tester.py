from tester import run_tests

result = run_tests("sample_test.py")

print("\nTESTER RESULTS")
print("=" * 40)

print("Success:", result["success"])
print("Summary:", result["summary"])
print("Output:")
print(result["output"])
print("Error:", result["error"])