
from ai_repair import analyze_and_repair

code = """
def divide(a, b):
    return a / b
"""

errors = "The function does not handle division by zero."

result = analyze_and_repair(code, errors)

print("\n===== GROQ AI REPAIR RESULT =====\n")
print(result)
