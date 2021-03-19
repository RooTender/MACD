from os import listdir
import re
import analyzer
import matplotlib.pyplot as plot


def get_file(directory):
    files = listdir(directory)

    if len(files) > 1:
        for i, file in enumerate(files):
            print("{0}. {1}".format(i + 1, file))
            files[i] = directory + '/' + file

        print()
        choice = input('Choose file to read (enter number): ')
        return files[int(choice) - 1]

    else:
        return directory + '/' + files[0]


def get_column(file, column):
    for col in file.columns:
        if column.lower() in col.lower():
            return file[col]
    return None

def extract_close_column(file):
    column = get_column(file, 'close')
    if (column is None):
        column = get_column(file, 'zamkniecie')

    # if still not found, then it's custom
    if  (column is None):
        columnName = input('Enter column name to extract: ')
        column = get_column(file, columnName)

    # Still not found
    if  (column is None):
        print('Given column does not exist!')
        exit(1)
    return column


def limit_array(arr, limit):
    if len(arr) > limit:
        arr = arr[-limit:]
    return arr


def get_floats(data):
    arr = []

    if data is None:
        print('The given column does not exist!')
        exit(1)

    for p in data:
        arr.append(float(re.findall(r'\d+(?:\.\d+)?', str(p))[0]))
    return arr


def get_sell_signals(x_axis, samples, macd, signal):
    days = []
    values = []
    for day in range(len(x_axis)):
        if analyzer.is_sell_signal(macd, signal, day):
            days.append(day)
            values.append(samples[day - 1])
    return days, values


def get_buy_signals(x_axis, samples, macd, signal):
    days = []
    values = []

    for day in range(len(x_axis)):
        if analyzer.is_buy_signal(macd, signal, day):
            days.append(day)
            values.append(samples[day - 1])

    return days, values


class Chart:

    def set_histogram(self, x_axis, macd, signals):
        positive = []
        negative = []

        for i in range(1000):
            difference = macd[i] - signals[i]

            if difference > 0:
                positive.append(difference)
                negative.append(0)
            else:
                negative.append(difference)
                positive.append(0)

        self.charts[1].bar(x_axis, positive, color="limegreen", width=1)
        self.charts[1].bar(x_axis, negative, color="firebrick", width=1)

    def set_macd_signal_chart(self, x_axis, macd, signal):
        self.set_histogram(x_axis, macd, signal)

        self.charts[1].plot(x_axis, macd, label="MACD", color="dodgerblue")
        self.charts[1].plot(x_axis, signal, label="SIGNAL", color="red")
        self.charts[1].legend(loc=2)

    def set_money_chart(self, x_axis, samples, buys, sells):
        self.charts[0].plot(x_axis, samples, label="Chart", color="dodgerblue")

        self.charts[0].scatter(buys[0], buys[1], label="Buy", color="firebrick", s=14)
        self.charts[0].scatter(sells[0], sells[1], label="Sell", color="limegreen", s=14)
        self.charts[0].legend(loc=2)

    def __init__(self, samples, macd, signal):
        x_axis = list(range(1, 1001))  # x_axis = [1:1000]

        # Title and subplots init
        self.table, self.charts = plot.subplots(2)
        self.table.suptitle('Stock data analysis based on MACD algorithm')

        buy_signals = get_buy_signals(x_axis, samples, macd, signal)
        sell_signals = get_sell_signals(x_axis, samples, macd, signal)

        self.set_money_chart(x_axis, samples, buy_signals, sell_signals)
        self.set_macd_signal_chart(x_axis, macd, signal)

    @staticmethod
    def show_chart():
        plot.show()
