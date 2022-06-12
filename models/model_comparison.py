from models.feature_extraction import get_data_for_model

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB


models = {
    'KNeighborsClassifier': KNeighborsClassifier(30),
    'GaussianNB': GaussianNB(),
    'DecisionTreeClassifier': DecisionTreeClassifier(random_state=0),
    'RandomForestClassifier': RandomForestClassifier(),
    'SVC': SVC(
        kernel='rbf',
        C=1.0,
    ),
    'MLPClassifier': MLPClassifier(
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

    for key in models:
        print ("==============")
        print ("Classifier", key)

        classifier_model = models[key]
        classifier_model.fit(X_train, Y_train)

        try:
            print("feature_importances", classifier_model.feature_importances_)
        except:
            pass

        # model performance
        print("score ", classifier_model.score(X_test, Y_test))


if __name__ == '__main__':
    train()
