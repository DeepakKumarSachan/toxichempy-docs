# tests/test_sum_module.py

import pytest

from toxichempy.chemoinformatics import add_numbers


def test_add_numbers():
    """
    Test cases for add_numbers function.
    """
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
    assert add_numbers(100, 200) == 300
    assert add_numbers(-10, -20) == -30


if __name__ == "__main__":
    pytest.main()
