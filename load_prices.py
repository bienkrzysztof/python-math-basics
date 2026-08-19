import csv


def load_prices(filename):
    prices = []

    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            prices.append(float(row["price"]))

    return prices


if __name__ == "__main__":
    prices = load_prices("prices.csv")
    print(prices)
