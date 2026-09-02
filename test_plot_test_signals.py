import pandas as pd
import matplotlib.pyplot as plt
import pytest

from plot_prices import prepare_plot_data

from plot_test_signals import (
    analyze_signals,
    create_signal_report,
    format_signal_report,
    create_test_data,
    plot_signals,
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
    assert result["crossunder_win_rate"] == 1.0


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


def test_create_test_data():
    result = create_test_data()

    assert len(result) == 30
    assert list(result.columns) == ["date", "price"]

    assert result["date"].iloc[0] == 0
    assert result["date"].iloc[-1] == 29

    assert result["price"].iloc[0] == 100
    assert result["price"].iloc[-1] == 180


def test_plot_signals():
    df = create_test_data()
    df = prepare_plot_data(df)

    fig = plot_signals(df)

    assert len(fig.axes) == 1

    ax = fig.axes[0]

    assert len(ax.lines) == 3

    assert ax.get_title() == "Crossover / Crossunder"
    assert ax.get_xlabel() == "Observation"
    assert ax.get_ylabel() == "Price"

    assert [line.get_label() for line in ax.get_lines()] == [
        "Price",
        "MA3",
        "MA5",
    ]

    assert ax.collections[0].get_offsets().shape == (4, 2)
    assert ax.collections[1].get_offsets().shape == (3, 2)

    plt.close(fig)


def test_analyze_signals_ignores_missing_future_returns():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
            "crossunder",
        ],
        "future_return_3": [
            0.10,
            float("nan"),
            -0.05,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_count"] == 1
    assert result["crossunder_count"] == 1

    assert result["crossover_mean"] == pytest.approx(0.10)
    assert result["crossunder_mean"] == pytest.approx(-0.05)

    assert result["crossover_median"] == pytest.approx(0.10)
    assert result["crossunder_median"] == pytest.approx(-0.05)

    assert result["crossover_win_rate"] == pytest.approx(1.0)
    assert result["crossunder_win_rate"] == pytest.approx(0.0)

    assert result["crossover_wins"] == 1
    assert result["crossover_losses"] == 0
    assert result["crossover_neutral"] == 0

    assert result["crossunder_wins"] == 0
    assert result["crossunder_losses"] == 1
    assert result["crossunder_neutral"] == 0


def test_analyze_signals_win_loss_neutral():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            0.10,
            0.0,
            -0.05,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_count"] == 3
    assert result["crossover_wins"] == 1
    assert result["crossover_losses"] == 1
    assert result["crossover_neutral"] == 1
    assert result["crossover_win_rate"] == pytest.approx(1 / 2)


def test_analyze_signals_no_wins_or_losses():
    signals = pd.DataFrame({
        "signal": ["crossover"],
        "future_return_3": [0.0],
    })

    result = analyze_signals(signals)

    assert pd.isna(result["crossover_win_rate"])


def test_analyze_signals_profit_factor():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            0.10,
            0.05,
            -0.04,
            -0.03,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_profit_factor"] == pytest.approx(15 / 7)


def test_analyze_signals_profit_factor_without_losses():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            0.10,
            0.05,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_profit_factor"] == float("inf")


def test_analyze_signals_profit_factor_without_wins():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            -0.05,
            -0.10,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_profit_factor"] == pytest.approx(0.0)


def test_analyze_signals_profit_factor_only_neutral():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            0.0,
            0.0,
        ],
    })

    result = analyze_signals(signals)

    assert pd.isna(result["crossover_profit_factor"])


def test_analyze_signals_expectancy():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            0.10,
            0.05,
            -0.04,
            -0.03,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_expectancy"] == pytest.approx(0.02)


def test_analyze_signals_expectancy_without_wins():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            -0.05,
            -0.10,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_expectancy"] == pytest.approx(-0.075)


def test_analyze_signals_expectancy_without_losses():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            0.10,
            0.05,
        ],
    })

    result = analyze_signals(signals)

    assert result["crossover_expectancy"] == pytest.approx(0.075)


def test_analyze_signals_expectancy_only_neutral():
    signals = pd.DataFrame({
        "signal": [
            "crossover",
            "crossover",
        ],
        "future_return_3": [
            0.0,
            0.0,
        ],
    })

    result = analyze_signals(signals)

    assert pd.isna(result["crossover_expectancy"])
