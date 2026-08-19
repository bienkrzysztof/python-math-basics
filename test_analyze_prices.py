import subprocess
import sys


def test_analyze_prices():
    result = subprocess.run(
        [sys.executable, "analyze_prices.py"],
        capture_output=True,
        text=True,
    )

    output = result.stdout

    assert "Price Analysis Report" in output
    assert "Observations: 8" in output
    assert "Mean daily return:" in output
    assert "Daily volatility:" in output
    assert "Annualized volatility:" in output
    assert "Sharpe ratio:" in output
    assert "Annualized Sharpe:" in output
    assert "Maximum drawdown:" in output
    