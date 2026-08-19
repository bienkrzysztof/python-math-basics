import pytest

from math_basics import norm, is_prime, mean, variance, std, returns, volatility, annualized_volatility, sharpe_ratio, annualized_sharpe_ratio


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


def test_returns():
    result = returns([100, 110, 105])

    assert result[0] == pytest.approx(0.10)
    assert result[1] == pytest.approx(-5 / 110)

    with pytest.raises(ValueError):
        returns([0, 100])


def test_norm():
    assert norm([3, 4]) == pytest.approx(5)


def test_volatility():
    prices = [100, 110, 105]

    expected = std(returns(prices))

    assert volatility(prices) == pytest.approx(expected)

    with pytest.raises(ValueError):
        volatility([])

    with pytest.raises(ValueError):
        volatility([100])


def test_annualized_volatility():
    prices = [100, 110, 105]

    expected = volatility(prices) * (252 ** 0.5)

    assert annualized_volatility(prices) == pytest.approx(expected)


def test_sharpe_ratio():
    prices = [100, 110, 105]

    daily_returns = returns(prices)
    expected = mean(daily_returns) / std(daily_returns)

    assert sharpe_ratio(prices) == pytest.approx(expected)

    expected_with_rf = (mean(daily_returns) - 0.01) / std(daily_returns)

    assert sharpe_ratio(prices, risk_free_rate=0.01) == pytest.approx(expected_with_rf)

    with pytest.raises(ValueError):
        sharpe_ratio([100, 100, 100])


def test_annualized_sharpe_ratio():
    prices = [100, 110, 105]

    expected = sharpe_ratio(prices) * (252 ** 0.5)

    assert annualized_sharpe_ratio(prices) == pytest.approx(expected)
    