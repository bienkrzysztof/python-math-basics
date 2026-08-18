from math_basics import is_prime


def test_is_prime():
    assert is_prime(2) is True
    assert is_prime(7) is True
    assert is_prime(10) is False
    assert is_prime(97) is True