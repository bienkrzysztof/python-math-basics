def norm(point):
    square_sum = 0
    for x in point:
        square_sum += x ** 2
    return square_sum ** 0.5


def mean(x):
    return sum(x) / len(x)


def variance(x):
    m = mean(x)
    return sum((value - m) ** 2 for value in x) / len(x)


def is_prime(n):
    if n < 2:
        return False
    for w in range(2, int(n ** 0.5) + 1):
        if n % w == 0:
            return False
    return True
