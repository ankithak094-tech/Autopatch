
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
