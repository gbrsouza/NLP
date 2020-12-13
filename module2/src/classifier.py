import random

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

from module2.src.dataset_reader import read_dataset as reader
from module2.src.preprocessor import Preprocessor
import xgboost as xgb


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
    data = reader()
    X, Y = dataset_to_list(data)

    pos =0
    neg = 0
    for i in Y:
        if i == 0:
            neg +=1
        else:
            pos +=1
    print('neg', neg)
    print('pos', pos)


    # create converter of text to numbers
    converter = TfidfVectorizer(max_features=10000)
    X = converter.fit_transform(X).toarray()  # transform text

    # create training and testing vars
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

    model = RandomForestClassifier(n_estimators=100, bootstrap=True, max_features="sqrt")
    model.fit(X_train, y_train)

    # Actual class predictions
    rf_predictions = model.predict(X_test)

    # Calculate roc auc
    print('roc', roc_auc_score(y_test, rf_predictions))
    print('acc', accuracy_score(y_test, rf_predictions))
    print('pre', precision_score(y_test, rf_predictions))
    print('rcl', recall_score(y_test, rf_predictions))
    # classifier = xgb.train(_params, d_train, num_round)
    # classifier.predict(d_test)
