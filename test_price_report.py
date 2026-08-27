import subprocess
import sys


def test_price_report():
    result = subprocess.run(
        [sys.executable, "price_report.py"],
        capture_output=True,
        text=True,
    )

    output = result.stdout

    assert "Price Analysis Report" in output
    assert "Observations: 8" in output
    assert "Mean daily return: 1.43%" in output
    assert "Daily volatility: 3.39%" in output
    assert "Annualized volatility: 53.86%" in output
    assert "Sharpe ratio: 0.42" in output
    assert "Annualized Sharpe: 6.68" in output
    assert "Maximum drawdown: -3.70%" in output
    assert "Calmar ratio: 807.64" in output