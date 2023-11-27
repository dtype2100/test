from sklearn.model_selection import train_test_split, cross_validate
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data = load_iris()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)

score = cross_validate(clf, X_test, y_test, return_train_score=True, scoring='accuracy')

print('train_score: ', score['train_score'].mean())
print('test_score: ', score['test_score'].mean())

y_pred = clf.predict(X_test)
print(f'accuracy_score: {accuracy_score(y_test, y_pred)}')

