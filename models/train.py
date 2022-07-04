from models.feature_extraction import get_data_for_model
from sklearn.neural_network import MLPClassifier
import pickle


TRAINED_MODEL_FILE = 'data/calculated-model.joblib'

def train():
    labels, features = get_data_for_model()

    # convert labels
    X = features
    Y = [0 if lab == 'benign' else 1 for lab in labels]

    classifier_model = MLPClassifier(
        hidden_layer_sizes=(150, 100, 50),
        max_iter=300,
        activation='relu',
        solver='adam',
        random_state=1
    )
    classifier_model.fit(X, Y)

    with open(TRAINED_MODEL_FILE, 'wb') as f:
        pickle.dump(classifier_model, f)

    # test if loaded model works
    with open(TRAINED_MODEL_FILE, 'rb') as f:
        clf2 = pickle.load(f)
        print("Test: ", clf2.predict(X[0:1]))
        print("model was successfully trained")


if __name__ == '__main__':
    train()
