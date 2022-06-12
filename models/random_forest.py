from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from models.feature_extraction import get_data_for_model


def train():
    labels, features = get_data_for_model()

    # convert labels
    X = features
    Y = [0 if lab == 'benign' else 1 for lab in labels]

    classifier_model = RandomForestClassifier()

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    classifier_model.fit(X_train, Y_train)

    print("feature_importances")
    print(classifier_model.feature_importances_)

    # predict values from group that was left for testing
    # print(classifier_model.predict(X_test))

    # model performance
    print(classifier_model.score(X_test, Y_test))

    import pdb
    pdb.set_trace()

    return


if __name__ == '__main__':
    train()
