import os
import joblib
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

MODEL = os.path.join(os.path.realpath('..'), 'models')
TABLE = {}


def mapping(data):
    values = data.split(' ')
    value = values[1]
    value = re.sub(r'[0-9]+', '<number>', value)
    value = re.sub(r'[,.`´\'\"!?;:*&#@%$()=+\\/_-]+', '', value)

    tag = values[0]
    tag = re.sub(r'[0-9]+', '', tag)
    tag = re.sub(r'[,.`´\'\"!?;:*&#@%$()=+\\/_-]+', '', tag)
    if value == '' or tag == '':
        return ''
    else:
        return tag + ' ' + value


def read_dataset(path_dataset):
    print("Reading dataset from path", path_dataset)
    file = open(path_dataset, 'r')
    data = {}

    for s in file:
        for c in range(len(s)):
            if s[c] == '(':
                value = []
                c += 1
                while s[c] != ')' and c < len(s) - 1:

                    if s[c] == '(':
                        value.clear()
                        break
                    else:
                        value.append(s[c])
                    c += 1
                if s[c] == ')':
                    str1 = ''.join(value)
                    str1 = mapping(str1)
                    if str1 != '':
                        if str1 in data:
                            data[str1] += 1
                        else:
                            data[str1] = 1

    file.close()
    return data


def classify(value):
    candidates = []
    for key in TABLE:
        values = key.split(" ")
        if values[1] == value:
            candidates.append([values[0], TABLE[key]])

    # Se não houver candidados retornar a tag mais comum
    best_candidate = ''
    value_best_candidate = -1
    if len(candidates) == 0:
        for key in TABLE:
            values = key.split(" ")
            if TABLE[key] > value_best_candidate:
                value_best_candidate = TABLE[key]
                best_candidate = values[0]
        return best_candidate
    else:
        for candidate in candidates:
            if candidate[1] > value_best_candidate:
                best_candidate = candidate[0]
                value_best_candidate = candidate[1]
        return best_candidate


def print_confusion_matrix(tags, confusion_matrix):

    matrix = "    "
    for i in range(len(tags)):
        matrix = matrix + tags[i] + " "
    matrix += "\n"

    for i in range(len(tags)):
        line = tags[i] + " "
        for j in range(len(tags)):
            print(i, j)
            line += str(confusion_matrix[i][j])
            line += " "
        matrix = matrix + line + "\n"
    print(matrix)

if __name__ == '__main__':
    path = os.path.join(os.path.realpath('..'), 'data', 'traindata')

    if 'table.joblib' in os.listdir(MODEL):
        TABLE = joblib.load(os.path.join(MODEL, '{}.joblib'.format('table')))
    else:
        TABLE = read_dataset(path)
        joblib.dump(TABLE, os.path.join(MODEL, '{}.joblib'.format('table')))

    path_test = os.path.join(os.path.realpath('..'), 'data', 'test')
    test_data = read_dataset(path_test)

    total = 0
    acertos = 0
    erros = 0

    tags = {}
    count = 0
    for key in test_data:
        values = key.split(" ")
        if values[0] not in tags:
            tags[values[0]] = count
            count += 1
    for key in TABLE:
        values = key.split(" ")
        if values[0] not in tags:
            tags[values[0]] = count
            count += 1
    print(tags)

    tags_list = []
    for key in tags:
        tags_list.append(key)

    confusion_matrix = np.full((len(tags_list), len(tags_list)), 0)
    for key in test_data:
        values = key.split(" ")
        word = values[1]
        classified = classify(word)
        total += test_data[key]

        index_classified = tags[classified]
        index_original = tags[values[0]]
        confusion_matrix[index_classified][index_original] += 1

        if classified == values[0]:
            acertos += test_data[key]
        else:
            erros += test_data[key]

    print_confusion_matrix(tags_list, confusion_matrix)
    print('total:', total)
    print('acertos:', acertos)
    print('erros:', erros)
    print('accuracia:', acertos/total)

    df_cm = pd.DataFrame(confusion_matrix, index=[i for i in tags_list],
                         columns=[i for i in tags_list])
    plt.figure(figsize=(len(tags_list), len(tags_list)))
    sns_plot = sns.heatmap(df_cm, annot=True, cmap='coolwarm', linecolor='white', linewidths=1)
    figure = sns_plot.get_figure()
    figure.savefig('output.png', dpi=100)
    # fig, ax = plt.subplots()
    # im = ax.imshow(confusion_matrix)
    #
    # # We want to show all ticks...
    # ax.set_xticks(np.arange(len(tags_list)))
    # ax.set_yticks(np.arange(len(tags_list)))
    # # ... and label them with the respective list entries
    # ax.set_xticklabels(tags_list)
    # ax.set_yticklabels(tags_list)
    #
    # # Rotate the tick labels and set their alignment.
    # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
    #          rotation_mode="anchor")
    #
    # # Loop over data dimensions and create text annotations.
    # for i in range(len(tags_list)):
    #     for j in range(len(tags_list)):
    #         text = ax.text(j, i, confusion_matrix[i, j],
    #                        ha="center", va="center", color="w")
    #
    # ax.set_title("Confusion Matrix")
    # fig.tight_layout()
    # plt.savefig("confusion_matrix.png")



