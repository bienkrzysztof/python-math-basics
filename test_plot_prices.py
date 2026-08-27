import pandas as pd
import pytest

from price_data import load_prices
from plot_prices import prepare_plot_data


def test_prepare_plot_data():
    df = load_prices("prices.csv")

    result = prepare_plot_data(df)

    assert "return" in result.columns
    assert "drawdown" in result.columns
    assert "rolling_volatility" in result.columns

    assert result["return"].iloc[1] == pytest.approx(0.02)
    assert result["drawdown"].iloc[6] == pytest.approx(-0.03703703703703709)
    assert result["rolling_volatility"].iloc[3] == pytest.approx(
        0.024878798886846264
    )
    assert pd.isna(result["ma3"].iloc[0])
    assert pd.isna(result["ma3"].iloc[1])

    assert result["ma3"].iloc[2] == pytest.approx(101.0)
    assert result["ma3"].iloc[3] == pytest.approx(102.66666666666667)

def test_ma3_above_ma5():
    df = load_prices("prices.csv")

    result = prepare_plot_data(df)

    assert result["ma3_above_ma5"].iloc[4] 
    assert result["ma3_above_ma5"].iloc[5] 
    assert result["ma3_above_ma5"].iloc[6] 
    assert result["ma3_above_ma5"].iloc[7]    

def test_crossover_and_crossunder():
    df = pd.DataFrame({
        "price": [100, 110, 90, 80, 120, 130, 70, 60, 140, 150]
    })

    result = prepare_plot_data(df)

    assert result["crossover"].tolist() == [
        False, False, False, False, False,
        True, False, False, False, True
    ]

    assert result["crossunder"].tolist() == [
        False, False, False, False, False,
        False, False, True, False, False
    ]

    assert result.loc[result["crossover"], "price"].tolist() == [130, 150]
    assert result.loc[result["crossunder"], "price"].tolist() == [60]
