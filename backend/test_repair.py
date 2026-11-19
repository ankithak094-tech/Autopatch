from repair import save_fixed_code

fixed_code = """
def add(a, b):
    return a + b

print(add(10, 20))
"""

result = save_fixed_code(fixed_code)

print("\nREPAIR RESULTS")
print("=" * 40)
print("Success:", result["success"])
print("File:", result["file"])
print("Message:", result["message"])