from analyzer import detect_bugs

code = """
x = 10 / 0
y = eval('2 + 3')
z = unknown_variable
unused = 100
"""

results = detect_bugs(code)

for bug in results:
    print(bug)
from tester import run_tests

result = run_tests("sample_test.py")

print("\nTEST RESULTS:")
print(result)