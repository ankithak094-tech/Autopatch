from pathlib import Path

from repair import save_fixed_code


def test_save_fixed_code():
    result = save_fixed_code(
        "print('Hello AutoPatch')",
        "test_fixed_code.py"
    )

    assert result["success"] is True
    assert Path("test_fixed_code.py").exists()
