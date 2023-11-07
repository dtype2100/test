import bentoml
import optuna
import mlflow
from sklearn import svm
from sklearn import datasets
from sklearn.model_selection import cross_val_score
from mlflow import MlflowClient

server_uri = 'http://127.0.0.1:5000'

client = MlflowClient(server_uri)

iris = datasets.load_iris()
X, y = iris.data, iris.target

def objective(trial):
    with mlflow.start_run():
        C = trial.suggest_float("C", 0.1, 10.0)
        gamma = trial.suggest_float("gamma", 0.1, 10.0)
        clf = svm.SVC(C=C, gamma=gamma).fit(X, y)
        score = cross_val_score(clf, X, y, n_jobs=-1, cv=5, scoring='f1_weighted').mean()
        mlflow.log_metric("f1", score)
        return score
    
mlflow.set_tracking_uri(server_uri)
mlflow.set_experiment("iris_clf")
experiment_name = 'hpo-experiment'
study = optuna.create_study(study_name=experiment_name, direction="maximize", load_if_exists=True)
study.optimize(lambda trial: objective(trial), n_trials=10)
best_params = study.best_params

with mlflow.start_run():
    mlflow.log_params(best_params)
    clf = svm.SVC(**best_params).fit(X, y)
    score = cross_val_score(clf, X, y, cv=3, scoring='f1_weighted')
    mlflow.log_metric("f1", score.mean())
    saved_model_path = bentoml.sklearn.save_model("iris_clf", clf)
    mlflow.end_run()
