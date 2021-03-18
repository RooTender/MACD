from os import listdir
import re

def get_file(directory):
    files = listdir(directory)

    if len(files) > 1:
        for i, file in enumerate(files):
            print("{0}. {1}".format(i + 1, file))
            files[i] = directory + '/' + file

        print("Choose file to read (enter number):")
        return files[int(input()) - 1]

    else:
        return directory + '/' + files[0]


def extract_column(file, column):
    for col in file.columns:
        if column.lower() in col.lower():
            return file[col]


def limit_array(arr, limit):
    if len(arr) > limit:
        arr = arr[-limit:]
    return arr


def get_floats(data):
    arr = []

    for p in data:
        arr.append(float(re.findall(r'\d+(?:\.\d+)?', p)[0]))
    return arr