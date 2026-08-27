from price_data import (
    load_prices,
    mean_return,
    volatility,
    annualized_volatility,
    sharpe_ratio,
    annualized_sharpe_ratio,
    max_drawdown,
    calmar_ratio,
)


def generate_report(df):
    print("Price Analysis Report")
    print("=====================")
    print()
    print(f"Observations: {len(df)}")
    print()
    print(f"Mean daily return: {mean_return(df):.2%}")
    print(f"Daily volatility: {volatility(df):.2%}")
    print(f"Annualized volatility: {annualized_volatility(df):.2%}")
    print(f"Sharpe ratio: {sharpe_ratio(df):.2f}")
    print(f"Annualized Sharpe: {annualized_sharpe_ratio(df):.2f}")
    print(f"Maximum drawdown: {max_drawdown(df):.2%}")
    print(f"Calmar ratio: {calmar_ratio(df):.2f}")

if __name__ == "__main__":
    df = load_prices("prices.csv")
    generate_report(df)