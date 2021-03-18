def ema(n, data, index):
    factor = 1
    alpha = 2 / (n + 1)
    nominator = 0
    denominator = 0

    for i in range(n, -1, -1):
        p = data[index - i]
        nominator += p * factor
        denominator += factor

        factor *= (1 - alpha)
    return nominator / denominator


def macd(data):
    n = len(data)
    output = []

    for i in range(26, n):
        output.append(ema(12, data, i) - ema(26, data, i))
    return output


def signal(macd):
    n = len(macd)
    output = []

    for i in range(9, n):
        output.append(ema(9, macd, i))
    return output