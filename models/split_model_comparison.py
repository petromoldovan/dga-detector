import time

from models.feature_extraction import get_data_for_model

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler


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

    # split data into train and test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    # TODO: only for MPL and SVC?
    # add scaler
    # scaler = StandardScaler()
    # # # fit only to the training data
    # scaler.fit(X_train)
    # X_train = scaler.transform(X_train)
    # X_test = scaler.transform(X_test)

    for key in models:
        print ("==============")
        print ("Classifier", key)
        start = time.time()

        classifier_model = models[key]
        classifier_model.fit(X_train, Y_train)
        end = time.time()

        try:
            print("feature_importances", classifier_model.feature_importances_)
        except:
            pass

        predictions = classifier_model.predict(X_test)
        confusion_matrix_result = confusion_matrix(Y_test, predictions)
        print(confusion_matrix_result)

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
        print("accuracy", accuracy)
        print("precision", precision)
        print("recall", recall)
        print("f1_score", f1_score)
        time_elapsed = round(end - start, 2)
        print("time (s)", time_elapsed)

        # print(classification_report(Y_test, predictions))
        # return


if __name__ == '__main__':
    train()
