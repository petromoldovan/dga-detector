import time

from models.feature_extraction import get_data_for_model

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np
from sklearn.model_selection import KFold


models = {
    'KNeighbors': KNeighborsClassifier(30),
    'GaussianNB': GaussianNB(),
    'DecisionTree': DecisionTreeClassifier(random_state=0),
    'RandomForest': RandomForestClassifier(),
    'SVC': SVC(
        kernel='rbf',
        C=1.0,
    ),
    'MLP': MLPClassifier(
        hidden_layer_sizes=(150, 100, 50),
        max_iter=300,
        activation='relu',
        solver='adam',
        random_state=1
    ),
}


def train():
    labels, features = get_data_for_model()

    # convert labels
    X = features
    Y = [0 if lab == 'benign' else 1 for lab in labels]

    X = np.array(X)
    Y = np.array(Y)

    results = {}

    for split in [5, 10, 15]:
        print ("----------------------------------- split ", split)
        kf = KFold(n_splits=split, shuffle=True)
        for train_index, test_index in kf.split(X):
            # print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = X[train_index], X[test_index]
            Y_train, Y_test = Y[train_index], Y[test_index]

            for key in models:
                if not key in results:
                    results[key] = {}

                if not split in results[key]:
                    results[key][split] = {}
                    results[key][split]['accuracy'] = []
                    results[key][split]['precision'] = []
                    results[key][split]['recall'] = []
                    results[key][split]['f1_score'] = []
                    results[key][split]['time'] = []

                print ("==============")
                print ("Classifier", key)
                start = time.time()

                classifier_model = models[key]
                classifier_model.fit(X_train, Y_train)
                end = time.time()

                predictions = classifier_model.predict(X_test)
                confusion_matrix_result = confusion_matrix(Y_test, predictions)
                # print(confusion_matrix_result)

                TN = confusion_matrix_result[0][0]
                FP = confusion_matrix_result[0][1]
                FN = confusion_matrix_result[1][0]
                TP = confusion_matrix_result[1][1]

                accuracy = (TP + TN) / (TP + FP + TN + FN)
                precision = TP / (TP + FP)
                recall = TP / (TP + FN)
                f1_score = (2 * precision * recall) / (precision + recall)
                accuracy = round(accuracy, 2)
                precision = round(precision, 2)
                recall = round(recall, 2)
                f1_score = round(f1_score, 2)
                time_elapsed = round(end - start, 2)

                # aggregate results
                results[key][split]['accuracy'].append(accuracy)
                results[key][split]['precision'].append(precision)
                results[key][split]['recall'].append(recall)
                results[key][split]['f1_score'].append(f1_score)
                results[key][split]['time'].append(time_elapsed)


    # report results
    for model in results:
        print ("==============")
        print("Model", model)
        for split in results[model]:
            print("---------split: ", split)
            print("accuracy", round(np.mean(results[model][split]['accuracy']), 2))
            print("precision", round(np.mean(results[model][split]['precision']), 2))
            print("recall", round(np.mean(results[model][split]['recall']), 2))
            print("f1_score", round(np.mean(results[model][split]['f1_score']), 2))
            print("time", round(np.mean(results[model][split]['time']), 2))


if __name__ == '__main__':
    train()
