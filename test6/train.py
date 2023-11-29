from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.ensemble import RandomForestClassifier

data = load_iris()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier(n_estimators=100).fit(X_train, y_train)

score = cross_validate(clf, X, y, cv=5, scoring='accuracy', return_train_score=True)

print(score['train_score'].mean())
print(score['test_score'].mean())

import joblib
joblib.dump(clf, "clf_joblib.pkl")

loaded_clf = joblib.load("clf_joblib.pkl")

prediction1 = loaded_clf.predict(X_test)

print(prediction1)

import pickle

with open("clf_pickle.pkl", "wb") as f:
    pickle.dump(clf, f)

with open("clf_pickle.pkl", "rb") as f:
    loaded_clf2 = pickle.load(f)

prediction2 = loaded_clf2.predict(X_test)

print(prediction2)