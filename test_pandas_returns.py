import pytest
import pandas as pd

from math_basics import returns


def test_returns_match_pandas():
    prices = [100, 102, 101, 105, 103, 108, 104, 110]

    our_returns = returns(prices)
    pandas_returns = pd.Series(prices).pct_change().dropna().tolist()

    assert our_returns == pytest.approx(pandas_returns)