import pytest

from math_basics import is_prime, mean, variance, std


def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(7) is True
    assert is_prime(10) is False
    assert is_prime(97) is True


def test_mean():
    assert mean([1, 2, 3]) == 2
    assert mean([10, 20, 30, 40]) == 25


def test_variance():
    assert variance([1, 2, 3]) == pytest.approx(2 / 3)
    assert variance([5, 5, 5, 5]) == 0


def test_std():
    assert std([1, 2, 3]) == pytest.approx((2 / 3) ** 0.5)
    assert std([5, 5, 5, 5]) == 0
