
from pathlib import Path

from repair import save_fixed_code


def test_save_fixed_code(tmp_path):
    output_file = tmp_path / "test_fixed_code.py"

    result = save_fixed_code(
        "print('Hello AutoPatch')",
        str(output_file)
    )

    assert result["success"] is True
    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == "print('Hello AutoPatch')"
