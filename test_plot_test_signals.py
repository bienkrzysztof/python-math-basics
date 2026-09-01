import pandas as pd

from plot_test_signals import (
    analyze_signals,
    create_signal_report,
    format_signal_report,
)


def test_analyze_signals():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
            "crossunder",
            "crossunder",
        ],
        "future_return_3": [
            0.10,
            -0.05,
            0.20,
            0.00,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_count"] == 2
    assert result["crossunder_count"] == 2

    assert result["crossover_mean"] == 0.025
    assert result["crossunder_mean"] == 0.10

    assert result["crossover_wins"] == 1
    assert result["crossover_losses"] == 1
    assert result["crossover_neutral"] == 0

    assert result["crossunder_wins"] == 1
    assert result["crossunder_losses"] == 0
    assert result["crossunder_neutral"] == 1

    assert result["crossover_win_rate"] == 0.5
    assert result["crossunder_win_rate"] == 0.5


def test_create_signal_report():
    results = {
        "crossover_count": 4,
        "crossunder_count": 3,
        "crossover_mean": 0.10,
        "crossunder_mean": 0.20,
        "crossover_median": 0.15,
        "crossunder_median": 0.05,
        "crossover_win_rate": 0.75,
        "crossunder_win_rate": 0.33,
        "crossover_wins": 3,
        "crossunder_wins": 1,
        "crossover_losses": 1,
        "crossunder_losses": 1,
        "crossover_neutral": 0,
        "crossunder_neutral": 1,
    }

    result = create_signal_report(results)

    assert result["signal"].tolist() == [
        "crossover",
        "crossunder",
    ]

    assert result["count"].tolist() == [4, 3]

    assert result["mean_return"].tolist() == [
        0.10,
        0.20,
    ]

    assert result["median_return"].tolist() == [
        0.15,
        0.05,
    ]

    assert result["win_rate"].tolist() == [
        0.75,
        0.33,
    ]

    assert result["wins"].tolist() == [3, 1]
    assert result["losses"].tolist() == [1, 1]
    assert result["neutral"].tolist() == [0, 1]


def test_format_signal_report():
    report = pd.DataFrame({
        "signal": ["crossover", "crossunder"],
        "count": [4, 3],
        "mean_return": [0.110897, 0.097222],
        "median_return": [0.205128, 0.0],
        "win_rate": [0.75, 0.333333],
        "wins": [3, 1],
        "losses": [1, 1],
        "neutral": [0, 1],
    })

    result = format_signal_report(report)

    assert result["mean_return"].tolist() == [
        "11.09%",
        "9.72%",
    ]

    assert result["median_return"].tolist() == [
        "20.51%",
        "0.00%",
    ]

    assert result["win_rate"].tolist() == [
        "75.00%",
        "33.33%",
    ]
