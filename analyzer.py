fastLength = 12
slowLength = 26
macdLength = 9

def ema(n, data, index):
    alpha = 2 / (n + 1)

    nominator = 0
    denominator = 0

    for i in range(n, -1, -1):
        p = data[index - i]
        nominator += p * (1 - alpha) ** i
        denominator += (1 - alpha) ** i

    return nominator / denominator


def macd(data):
    n = len(data)
    output = []

    for i in range(slowLength, n):
        output.append(ema(fastLength, data, i) - ema(slowLength, data, i))

    return output


def signal(macd):
    n = len(macd)
    output = []

    for i in range(macdLength, n):
        output.append(ema(macdLength, macd, i))

    return output


def get_signals(macd, signal, day):
    prev_macd = (macd[day - 1], macd[day])[day == 0]
    prev_signal = (signal[day - 1], signal[day])[day == 0]

    previous = (prev_macd / prev_signal) - 1
    current = (macd[day] / signal[day]) - 1

    return previous, current


def is_sell_signal(macd, signal, day):
    previous, current = get_signals(macd, signal, day)

    if previous < 0 <= current:
        return True
    return False


def is_buy_signal(macd, signal, day):
    previous, current = get_signals(macd, signal, day)

    if previous > 0 >= current:
        return True
    return False


def false_signal(macd, signal, day):
    previous, current = get_signals(macd, signal, day)

    if abs(previous) < 0.05:
        return True
    return False
