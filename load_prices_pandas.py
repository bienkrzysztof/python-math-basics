import pandas as pd

from math_basics import returns

df = pd.read_csv("prices.csv", parse_dates=["date"])

print(df)
print()
print(df.dtypes)

print()
print("Price column:")
print(df["price"])

print()
print("First 3 rows:")
print(df.head(3))

print()
print("Returns:")
print(df["price"].pct_change())

prices = df["price"].tolist()

print()
print("Our returns:")
print(returns(prices))

print()
print("Pandas returns:")
print(df["price"].pct_change().tolist())
