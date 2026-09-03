import matplotlib.pyplot as plt
import pandas as pd

from plot_prices import prepare_plot_data


def calculate_win_rate(returns):
    wins = (returns > 0).sum()
    losses = (returns < 0).sum()

    if wins + losses == 0:
        return float("nan")

    return wins / (wins + losses)


def calculate_profit_factor(returns):
    gross_profit = returns[returns > 0].sum()
    gross_loss = returns[returns < 0].sum()

    if gross_loss == 0:
        if gross_profit > 0:
            return float("inf")

        return float("nan")

    return gross_profit / abs(gross_loss)


def calculate_expectancy(returns):
    wins = returns[returns > 0]
    losses = returns[returns < 0]

    total = len(wins) + len(losses)

    if total == 0:
        return float("nan")

    win_probability = len(wins) / total
    loss_probability = len(losses) / total

    average_win = wins.mean() if len(wins) > 0 else 0
    average_loss = abs(losses.mean()) if len(losses) > 0 else 0

    return (
        win_probability * average_win
        - loss_probability * average_loss
    )


def calculate_max_drawdown(returns):
    if len(returns) == 0:
        return float("nan")

    equity = pd.concat([pd.Series([1.0]), 1 + returns]).cumprod()

    running_max = equity.cummax()

    drawdown = equity / running_max - 1

    return abs(drawdown.min())


def calculate_average_win(returns):
    wins = returns[returns > 0]

    if len(wins) == 0:
        return float("nan")

    return wins.mean()


def calculate_average_loss(returns):
    losses = returns[returns < 0]

    if len(losses) == 0:
        return float("nan")

    return abs(losses.mean())


def calculate_payoff_ratio(returns):
    average_win = calculate_average_win(returns)
    average_loss = calculate_average_loss(returns)

    if pd.isna(average_win):
        return float("nan")

    if pd.isna(average_loss):
        return float("inf")

    return average_win / average_loss


def analyze_signals(signals):
    crossover_returns = signals.loc[
        (signals["signal"] == "crossover")
        & signals["future_return_3"].notna(),
        "future_return_3"
    ]

    crossunder_returns = signals.loc[
        (signals["signal"] == "crossunder")
        & signals["future_return_3"].notna(),
        "future_return_3"
    ]

    results = {
        "crossover_count": len(crossover_returns),
        "crossunder_count": len(crossunder_returns),

        "crossover_mean": crossover_returns.mean(),
        "crossunder_mean": crossunder_returns.mean(),

        "crossover_median": crossover_returns.median(),
        "crossunder_median": crossunder_returns.median(),

        "crossover_win_rate": calculate_win_rate(crossover_returns),
        "crossunder_win_rate": calculate_win_rate(crossunder_returns),

        "crossover_profit_factor": calculate_profit_factor(
            crossover_returns
        ),
        "crossunder_profit_factor": calculate_profit_factor(
            crossunder_returns
        ),

        "crossover_expectancy": calculate_expectancy(
            crossover_returns
        ),
        "crossunder_expectancy": calculate_expectancy(
            crossunder_returns
        ),

        "crossover_max_drawdown": calculate_max_drawdown(
            crossover_returns
        ),
        "crossunder_max_drawdown": calculate_max_drawdown(
            crossunder_returns
        ),

        "crossover_wins": (crossover_returns > 0).sum(),
        "crossover_losses": (crossover_returns < 0).sum(),
        "crossover_neutral": (crossover_returns == 0).sum(),

        "crossunder_wins": (crossunder_returns > 0).sum(),
        "crossunder_losses": (crossunder_returns < 0).sum(),
        "crossunder_neutral": (crossunder_returns == 0).sum(),

        "crossover_average_win": calculate_average_win(
            crossover_returns
        ),
        "crossover_average_loss": calculate_average_loss(
            crossover_returns
        ),

        "crossunder_average_win": calculate_average_win(
            crossunder_returns
        ),
        "crossunder_average_loss": calculate_average_loss(
            crossunder_returns
        ),
        "crossover_payoff_ratio": calculate_payoff_ratio(
            crossover_returns
        ),
        "crossunder_payoff_ratio": calculate_payoff_ratio(
            crossunder_returns
        ),
    }

    return results


def create_signal_report(results):
    report = pd.DataFrame({
        "signal": ["crossover", "crossunder"],
        "count": [
            results["crossover_count"],
            results["crossunder_count"],
        ],
        "mean_return": [
            results["crossover_mean"],
            results["crossunder_mean"],
        ],
        "median_return": [
            results["crossover_median"],
            results["crossunder_median"],
        ],
        "win_rate": [
            results["crossover_win_rate"],
            results["crossunder_win_rate"],
        ],
        "wins": [
            results["crossover_wins"],
            results["crossunder_wins"],
        ],
        "losses": [
            results["crossover_losses"],
            results["crossunder_losses"],
        ],
        "neutral": [
            results["crossover_neutral"],
            results["crossunder_neutral"],
        ],
    })

    return report


def format_signal_report(report):
    formatted_report = report.copy()

    formatted_report["mean_return"] = formatted_report[
        "mean_return"
    ].map(lambda value: f"{value:.2%}")

    formatted_report["median_return"] = formatted_report[
        "median_return"
    ].map(lambda value: f"{value:.2%}")

    formatted_report["win_rate"] = formatted_report[
        "win_rate"
    ].map(lambda value: f"{value:.2%}")

    return formatted_report


def create_test_data():
    return pd.DataFrame({
        "date": range(30),
        "price": [
            100, 110, 90, 80, 120, 130, 70, 60, 140, 150,
            100, 90, 80, 70, 60, 50, 70, 90, 110, 130,
            120, 110, 100, 90, 80, 100, 120, 140, 160, 180,
        ],
    })


def plot_signals(df):
    plt.figure(figsize=(10, 5))

    plt.plot(df["date"], df["price"], label="Price")
    plt.plot(df["date"], df["ma3"], label="MA3")
    plt.plot(df["date"], df["ma5"], label="MA5")

    plt.scatter(
        df.loc[df["crossover"], "date"],
        df.loc[df["crossover"], "ma3"],
        marker="^",
    )

    plt.scatter(
        df.loc[df["crossunder"], "date"],
        df.loc[df["crossunder"], "ma3"],
        marker="v",
    )

    plt.legend()

    plt.title("Crossover / Crossunder")
    plt.xlabel("Observation")
    plt.ylabel("Price")

    plt.tight_layout()

    return plt.gcf()


def main():
    df = create_test_data()

    df = prepare_plot_data(df)

    signals = df[df["signal"] != ""]

    results = analyze_signals(signals)

    report = create_signal_report(results)

    formatted_report = format_signal_report(report)

    print()
    print("Signal report:")
    print(formatted_report)


    print()
    print("Individual signals")
    print("-----------------")
    print(
        signals[
            ["price", "ma3", "ma5", "signal", "future_return_3"]
        ]
    )

    fig = plot_signals(df)
    plt.show()


if __name__ == "__main__":
    main()
    