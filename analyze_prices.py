from math_basics import (
    returns,
    mean,
    volatility,
    annualized_volatility,
    sharpe_ratio,
    annualized_sharpe_ratio,
    max_drawdown,
    calmar_ratio,
)

from load_prices import load_prices

prices = load_prices("prices.csv")

daily_returns = returns(prices)


print("Price Analysis Report")
print("=====================")
print()
print(f"Observations: {len(prices)}")
print()
print(f"Mean daily return: {mean(daily_returns):.2%}")
print(f"Daily volatility: {volatility(prices):.2%}")
print(f"Annualized volatility: {annualized_volatility(prices):.2%}")
print(f"Sharpe ratio: {sharpe_ratio(prices):.2f}")
print(f"Annualized Sharpe: {annualized_sharpe_ratio(prices):.2f}")
print(f"Maximum drawdown: {max_drawdown(prices):.2%}")
print(f"Calmar ratio: {calmar_ratio(prices):.2f}")
