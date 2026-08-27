import pandas as pd


def load_prices(filename):
    df = pd.read_csv(filename, parse_dates=["date"])
    df["return"] = df["price"].pct_change()

    return df


def mean_return(df):
    return df["return"].mean()

def volatility(df):
    return df["return"].std(ddof=0)

def annualized_volatility(df):
    return volatility(df) * (252 ** 0.5)

def sharpe_ratio(df):
    return mean_return(df) / volatility(df)

def annualized_sharpe_ratio(df):
    return sharpe_ratio(df) * (252 ** 0.5)

def max_drawdown(df):
    drawdown = df["price"] / df["price"].cummax() - 1

    return drawdown.min()

def calmar_ratio(df):
    annualized_return = (df["price"].iloc[-1] / df["price"].iloc[0]) ** (
        252 / (len(df) - 1)
    ) - 1

    return annualized_return / abs(max_drawdown(df))

def moving_average(prices, window=3):
    result = [None] * (window - 1)

    for i in range(window - 1, len(prices)):
        window_prices = prices[i - window + 1:i + 1]
        average = sum(window_prices) / window
        result.append(average)

    return result
