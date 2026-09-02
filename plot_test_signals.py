import matplotlib.pyplot as plt
import pandas as pd

from plot_prices import prepare_plot_data


def analyze_signals(signals):
    crossover_returns = signals.loc[
        signals["signal"] == "crossover",
        "future_return_3"
    ]

    crossunder_returns = signals.loc[
        signals["signal"] == "crossunder",
        "future_return_3"
    ]

    results = {
        "crossover_count": len(crossover_returns),
        "crossunder_count": len(crossunder_returns),

        "crossover_mean": crossover_returns.mean(),
        "crossunder_mean": crossunder_returns.mean(),

        "crossover_median": crossover_returns.median(),
        "crossunder_median": crossunder_returns.median(),

        "crossover_win_rate": (crossover_returns > 0).mean(),
        "crossunder_win_rate": (crossunder_returns > 0).mean(),

        "crossover_wins": (crossover_returns > 0).sum(),
        "crossover_losses": (crossover_returns < 0).sum(),
        "crossover_neutral": (crossover_returns == 0).sum(),

        "crossunder_wins": (crossunder_returns > 0).sum(),
        "crossunder_losses": (crossunder_returns < 0).sum(),
        "crossunder_neutral": (crossunder_returns == 0).sum(),
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

    plt.plot(df["date"], df["price"])
    plt.plot(df["date"], df["ma3"])
    plt.plot(df["date"], df["ma5"])

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

    plt.legend(["Price", "MA3", "MA5"])

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
    