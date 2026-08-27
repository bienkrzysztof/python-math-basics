import pandas as pd

import pytest

from price_data import load_prices, mean_return, volatility, annualized_volatility, sharpe_ratio, annualized_sharpe_ratio, max_drawdown, calmar_ratio, moving_average


def test_load_prices():
    df = load_prices("prices.csv")

    assert len(df) == 8
    assert list(df.columns) == ["date", "price", "return"]
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df["price"].tolist() == [100, 102, 101, 105, 103, 108, 104, 110]

def test_load_prices_calculates_returns():
    df = load_prices("prices.csv")

    assert df["return"].iloc[1] == pytest.approx(0.02)
    assert df["return"].iloc[2] == pytest.approx(101 / 102 - 1)

def test_mean_return():
    df = load_prices("prices.csv")

    assert mean_return(df) == pytest.approx(0.014278768536493158)

def test_volatility():
    df = load_prices("prices.csv")

    assert volatility(df) == pytest.approx(0.03392608348476773)

def test_annualized_volatility():
    df = load_prices("prices.csv")

    assert annualized_volatility(df) == pytest.approx(0.5385598791546659)

def test_sharpe_ratio():
    df = load_prices("prices.csv")

    assert sharpe_ratio(df) == pytest.approx(0.42087877732494816)

def test_annualized_sharpe_ratio():
    df = load_prices("prices.csv")

    assert annualized_sharpe_ratio(df) == pytest.approx(6.681243461440461)

def test_max_drawdown():
    df = load_prices("prices.csv")

    assert max_drawdown(df) == pytest.approx(-0.037037037037037035)

def test_calmar_ratio():
    df = load_prices("prices.csv")

    assert calmar_ratio(df) == pytest.approx(807.6423743875094)

def test_rolling_volatility():
    df = load_prices("prices.csv")

    df["return"] = df["price"].pct_change()

    df["rolling_volatility"] = (
        df["return"].rolling(window=3).std()
    )

    assert pd.isna(df["rolling_volatility"].iloc[0])
    assert pd.isna(df["rolling_volatility"].iloc[1])
    assert pd.isna(df["rolling_volatility"].iloc[2])

    assert df["rolling_volatility"].iloc[3] == pytest.approx(
        0.024878798886846264
    )

def test_moving_average():
    prices = [100, 102, 101, 105, 103, 108, 104, 110]

    result = moving_average(prices, window=3)

    assert result[:2] == [None, None]
    assert result[2] == pytest.approx(101.0)
    assert result[3] == pytest.approx(102.66666666666667)
    assert result[4] == pytest.approx(103.0)
    assert result[5] == pytest.approx(105.33333333333333)
    assert result[6] == pytest.approx(105.0)
    assert result[7] == pytest.approx(107.33333333333333)

def test_moving_average_matches_pandas():
    df = load_prices("prices.csv")

    prices = df["price"].tolist()

    ours = moving_average(prices, window=3)
    pandas_result = df["price"].rolling(window=3).mean().tolist()

    for our_value, pandas_value in zip(ours, pandas_result):
        if pd.isna(pandas_value):
            assert our_value is None
        else:
            assert our_value == pytest.approx(pandas_value)

def test_moving_average_window_5():
    prices = [100, 102, 101, 105, 103, 108, 104, 110]

    result = moving_average(prices, window=5)

    assert result[:4] == [None, None, None, None]
    assert result[4] == pytest.approx(102.2)
    assert result[5] == pytest.approx(103.8)
    