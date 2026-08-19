def norm(point):
    square_sum = 0
    for x in point:
        square_sum += x ** 2
    return square_sum ** 0.5


def mean(x):
    return sum(x) / len(x)


def variance(x):
    m = mean(x)
    return sum((value - m) ** 2 for value in x) / len(x)


def std(x):
    return variance(x) ** 0.5


def is_prime(n):
    if n < 2:
        return False
    for w in range(2, int(n ** 0.5) + 1):
        if n % w == 0:
            return False
    return True


def returns(prices):
    result = []

    for i in range(1, len(prices)):
        previous = prices[i - 1]
        current = prices[i]

        if previous == 0:
            raise ValueError("Previous price cannot be zero")

        result.append((current - previous) / previous)

    return result


def volatility(prices):
    if len(prices) < 2:
        raise ValueError("At least two prices are required")
    
    return std(returns(prices))


def annualized_volatility(prices):
    return volatility(prices) * (252 ** 0.5)


def sharpe_ratio(prices, risk_free_rate = 0):
    daily_returns = returns(prices)
    volatility_value = std(daily_returns)

    if volatility_value == 0:
        raise ValueError("Volatility cannot be zero")
    
    return (mean(daily_returns) - risk_free_rate) / volatility_value
