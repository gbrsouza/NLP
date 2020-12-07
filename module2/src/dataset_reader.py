import os
import csv

DATASET = os.path.join(os.path.realpath('..'), 'dataset', 'labeled_data.csv')


def read_dataset():
    data = []
    with open(DATASET) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        for row in read_csv:
            tweet = row[len(row) - 1]
            label = 0 if row[len(row) - 2] == '2' else 1

            data.append([label, tweet])
        return data
