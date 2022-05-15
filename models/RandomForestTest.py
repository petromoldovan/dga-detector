from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

dataset_iris = datasets.load_iris()
print(dataset_iris.feature_names)
print(dataset_iris.target_names)

print(dataset_iris.data)
print(dataset_iris.target)

# Test 1: whole dataset
X = dataset_iris.data
Y = dataset_iris.target
classifier_model = RandomForestClassifier()
# train on whole dataset
classifier_model.fit(X, Y)
print("feature_importances")
print(classifier_model.feature_importances_)

# Test 2: split dataset
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

classifier_model = RandomForestClassifier()
# train
classifier_model.fit(X_train, Y_train)
print("predict to which class it belongs the item", X[[0]])
print(classifier_model.predict_proba(X[[0]]))

print("feature_importances")
print(classifier_model.feature_importances_)

# predict values from group that was left for testing
print(classifier_model.predict(X_test))


# model performance
print(classifier_model.score(X_test, Y_test))
