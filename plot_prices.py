import matplotlib.pyplot as plt
from price_data import load_prices, moving_average


def prepare_plot_data(df):
    df = df.copy()

    df["drawdown"] = df["price"] / df["price"].cummax() - 1
    df["return"] = df["price"].pct_change()
    df["future_price_3"] = df["price"].shift(-3)
    
    df["future_return_3"] = (
    df["future_price_3"] / df["price"] - 1
    )

    df["rolling_volatility"] = (
        df["return"].rolling(window=3).std()
    )

    prices = df["price"].tolist()
    df["ma3"] = moving_average(prices, window=3)
    df["ma5"] = moving_average(prices, window=5)

    df["both_ma_available"] = (
        df["ma3"].notna()
        & df["ma5"].notna()
    )

    df["previous_both_ma_available"] = (
        df["both_ma_available"].shift(1).fillna(False)
    )

    df["ma3_above_ma5"] = df["ma3"] > df["ma5"]

    df["ma3_below_ma5"] = df["ma3"] < df["ma5"]

    df["previous_ma3_above_ma5"] = (
        df["ma3_above_ma5"].shift(1)
    )

    df["previous_ma3_below_ma5"] = (
        df["ma3_below_ma5"].shift(1)
    )

    df["crossover"] = (
        df["ma3_above_ma5"]
        & df["previous_ma3_above_ma5"].eq(False)
        & df["previous_both_ma_available"]
    )

    df["crossunder"] = (
        df["ma3_below_ma5"]
        & df["previous_ma3_below_ma5"].eq(False)
        & df["previous_both_ma_available"]
    )

    df["signal"] = ""

    df.loc[df["crossover"], "signal"] = "crossover"
    df.loc[df["crossunder"], "signal"] = "crossunder"

    return df

if __name__ == "__main__":
    df = load_prices("prices.csv")
    df = prepare_plot_data(df)

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.plot(df["date"], df["price"])
    plt.plot(df["date"], df["ma3"])
    plt.plot(df["date"], df["ma5"])

    plt.scatter(
        df.loc[df["crossover"], "date"],
        df.loc[df["crossover"], "ma3"],
    )

    plt.scatter(
        df.loc[df["crossunder"], "date"],
        df.loc[df["crossunder"], "ma3"],
    )

    plt.legend(["Price", "MA3", "MA5"])

    plt.title("Price History")
    plt.ylabel("Price")
    plt.xticks(rotation=45)

    plt.subplot(2, 1, 2)
    plt.plot(df["date"], df["drawdown"])

    plt.axhline(0, linestyle="--")

    max_dd_idx = df["drawdown"].idxmin()

    plt.scatter(
        df.loc[max_dd_idx, "date"],
        df.loc[max_dd_idx, "drawdown"],
    )

    plt.title("Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))

    plt.plot(df["date"], df["rolling_volatility"])

    plt.title("Rolling Volatility (3 observations)")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
   