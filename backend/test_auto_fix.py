
from repair import fix_code


def test_fix_eval():
    code = "result = eval('10 + 20')"
    result = fix_code(code)

    assert "ast.literal_eval(" in result["fixed_code"]


def test_fix_division_by_zero():
    code = "result = 10 / 0"
    result = fix_code(code)

    assert "10 / 1" in result["fixed_code"]


def test_undefined_variable():
    code = "print(unknown_variable)"
    result = fix_code(code, "UndefinedVariable")

    assert "Undefined variable detected" in result["fixes"][0]
    assert result["fixed_code"] == code


def test_known_undefined_variable():
    code = """
unknown_variable = 100
print(unknown_variable)
"""
    result = fix_code(code, "UndefinedVariable")

    assert result["success"] is False
    assert result["fixed_code"] == code
    assert result["fixes"] == []


def test_fix_variable_typo():
    code = """
total = 100
print(totla)
"""

    result = fix_code(code, "UndefinedVariable")

    assert "print(total)" in result["fixed_code"]
    assert "print(totla)" not in result["fixed_code"]
