import pandas
import io_manager
import stockbroker
import analyzer

# reading the data
filePath = io_manager.get_file('stocks_data')
file = pandas.read_csv(filePath)

# extract probes
samples = io_manager.extract_close_column(file)
samples = io_manager.get_floats(samples)
samples = samples[::-1]

# calculate MACD & SIGNAL
macd = analyzer.macd(samples)
signal = analyzer.signal(macd)

# only last 1000 are given to analysis
samples = io_manager.limit_array(samples, 1000)
macd = io_manager.limit_array(macd, 1000)
signal = io_manager.limit_array(signal, 1000)

# simulation
money = 100000
stocks = 0

greedy = stockbroker.Broker('Default - greedy', money, stocks)
enhanced = stockbroker.Broker('Enhanced', money, stocks)


for day in range(1000):
    is_buy = analyzer.is_buy_signal(macd, signal, day)
    is_sell = analyzer.is_sell_signal(macd, signal, day)

    # Greedy
    if is_buy:
        greedy.buy_all(samples[day], day)
    if is_sell:
        greedy.sell_all(samples[day], day)

    # Enhanced
    if is_buy and macd[day] < 0 and not analyzer.false_signal(macd, signal, day):
        enhanced.buy_all(samples[day], day)

    if is_sell and macd[day] > 0 and not analyzer.false_signal(macd, signal, day):
        enhanced.sell_half(samples[day], day)

greedy.status()
enhanced.status()

# generate chart
chart = io_manager.Chart(samples, macd, signal)
chart.show_chart()
