import pandas
import importer
import algs
import matplotlib.pyplot as plot

# reading the data
filePath = importer.get_file('stocks_data')
file = pandas.read_csv(filePath)

# extract probes
probes = importer.extract_column(file, "close")
probes = importer.get_floats(probes)
probes = probes[::-1]

# calculate MACD & SIGNAL
macd = algs.macd(probes)
signal = algs.signal(macd)

probes = importer.limit_array(probes, 1000)
macd = importer.limit_array(macd, 1000)
signal = importer.limit_array(signal, 1000)

# Generate charts
x_axis = list(range(1, 1001))   # x_axis = [1:1000]


plot.plot(x_axis, probes, label="Chart", color="dodgerblue")
plot.plot(x_axis, macd, label="MACD", color="dodgerblue")
plot.plot(x_axis, signal, label="SIGNAL", color="red")

plot.legend(bbox_to_anchor=(0.01, 0.99), loc='upper left', borderaxespad=0.)
plot.show()
