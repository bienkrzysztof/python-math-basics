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

df = pd.DataFrame({
    "date": range(30),
    "price": [
        100, 110, 90, 80, 120, 130, 70, 60, 140, 150,
        100, 90, 80, 70, 60, 50, 70, 90, 110, 130,
        120, 110, 100, 90, 80, 100, 120, 140, 160, 180,
    ],
})

df = prepare_plot_data(df)

signals = df[df["signal"] != ""]

results = analyze_signals(signals)

print("Signal analysis")
print("--------------")

print("Crossover")
print(
    f"  Mean return: {results['crossover_mean']:.2%}"
)
print(
    f"  Median return: {results['crossover_median']:.2%}"
)
print(
    f"  Win rate:    {results['crossover_win_rate']:.2%}"
)
print(
    f"  Wins:         {results['crossover_wins']}"
)
print(
    f"  Losses:       {results['crossover_losses']}"
)
print(
    f"  Neutral:      {results['crossover_neutral']}"
)

print("Crossunder")
print(
    f"  Mean return: {results['crossunder_mean']:.2%}"
)
print(
    f"  Median return: {results['crossunder_median']:.2%}"
)
print(
    f"  Win rate:    {results['crossunder_win_rate']:.2%}"
)
print(
    f"  Wins:         {results['crossunder_wins']}"
)
print(
    f"  Losses:       {results['crossunder_losses']}"
)
print(
    f"  Neutral:      {results['crossunder_neutral']}"
)

print(
    signals[
        ["price", "ma3", "ma5", "signal", "future_return_3"]
    ]
)

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
plt.show()
