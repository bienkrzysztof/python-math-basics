import subprocess
import sys

from load_prices import load_prices


def test_load_prices():
    result = subprocess.run(
        [sys.executable, "load_prices.py"],
        capture_output=True,
        text=True,
    )

    output = result.stdout

    assert "[100.0, 102.0, 101.0, 105.0, 103.0, 108.0, 104.0, 110.0]" in output


def test_load_prices_function():
    prices = load_prices("prices.csv")

    assert prices == [
        100.0,
        102.0,
        101.0,
        105.0,
        103.0,
        108.0,
        104.0,
        110.0,
    ]
    