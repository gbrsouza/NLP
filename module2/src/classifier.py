import random
from statistics import stdev

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from module2.src.dataset_reader import read_dataset as reader
from module2.src.preprocessor import Preprocessor


def dataset_to_list(dataset):
    preprocess = Preprocessor()
    pos = []
    neg = []
    for element in dataset:
        if element[0] == 0:
            neg.append(element)
        else:
            pos.append(element)

    random.shuffle(pos)
    random.shuffle(neg)

    x = []
    y = []
    for i in range(len(neg)):
        x.append(preprocess.process(pos[i][1]))
        y.append(pos[i][0])

        x.append(preprocess.process(neg[i][1]))
        y.append(neg[i][0])
    return x, y


if __name__ == '__main__':
    print("[1] loading dataset...", end=" ")
    data = reader()
    print("[Done]")

    roc_list = []
    acc_list = []
    pre_list = []
    rcl_list = []

    total_executions = 10
    print("[2] Starting test...")
    print("[2] total executions:", total_executions)
    for i in range(total_executions):
        print("Running step", i, "...")

        X, Y = dataset_to_list(data)

        # create converter of text to numbers
        converter = TfidfVectorizer(max_features=10000)
        X = converter.fit_transform(X).toarray()  # transform text

        # create training and testing vars
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

        #model = RandomForestClassifier(n_estimators=100, bootstrap=True, max_features="sqrt")
        #model = LinearSVC()
        model = LogisticRegression()
        model.fit(X_train, y_train)

        # Actual class predictions
        rf_predictions = model.predict(X_test)

        roc_list.append(roc_auc_score(y_test, rf_predictions))
        acc_list.append(accuracy_score(y_test, rf_predictions))
        pre_list.append(precision_score(y_test, rf_predictions))
        rcl_list.append(recall_score(y_test, rf_predictions))
        print("[Done]")

    print("acc:", min(acc_list), "&", max(acc_list), "&", sum(acc_list)/len(acc_list), "&", stdev(acc_list), "\n")
    print("acc:", min(pre_list), "&", max(pre_list), "&", sum(pre_list) / len(pre_list), "&", stdev(pre_list), "\n")
    print("acc:", min(rcl_list), "&", max(rcl_list), "&", sum(rcl_list) / len(rcl_list), "&", stdev(rcl_list), "\n")

    print("min pre:", min(pre_list))
    print("max pre:", max(pre_list))
    print("avg pre:", sum(pre_list)/len(pre_list))
    print("std pre:", stdev(pre_list), "\n")

    print("min rcl:", min(rcl_list))
    print("max rcl:", max(rcl_list))
    print("avg rcl:", sum(rcl_list)/len(rcl_list))
    print("std rcl:", stdev(rcl_list))
