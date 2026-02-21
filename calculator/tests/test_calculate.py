import pytest
from calculate import divide


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_divide_positive_numbers():
    assert divide(10, 2) == 5


def test_divide_negative_numbers():
    assert divide(-10, 2) == -5


def test_divide_float_numbers():
    assert divide(10.0, 3.0) == pytest.approx(3.33333)
