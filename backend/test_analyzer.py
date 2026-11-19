
from analyzer import detect_bugs

# Test 1: Division by zero
code1 = """
x = 10 / 0
"""

# Test 2: Unsafe eval()
code2 = """
x = eval('2 + 3')
"""

# Test 3: Undefined variable
code3 = """
x = unknown_variable
"""

# Test 4: Unused variable
code4 = """
def calculate():
    unused = 100
    return 10
"""

# Test 5: Correct Python code
code5 = """
def add(a, b):
    return a + b

result = add(10, 20)
print(result)
"""

test_cases = [
    ("Division by zero", code1),
    ("Unsafe eval", code2),
    ("Undefined variable", code3),
    ("Unused variable", code4),
    ("Correct code", code5)
]

for name, code in test_cases:
    print("\n" + "=" * 45)
    print("TEST:", name)
    print("=" * 45)

    results = detect_bugs(code)

    if results:
        for bug in results:
            print(bug)
    else:
        print("No bugs detected.")
