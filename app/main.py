import mlflow
import pandas as pd
from fastapi import FastAPI
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from mlflow import MlflowClient
app = FastAPI()

@app.get("/run")
def run():
    data = load_iris()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target)
    model = RandomForestClassifier().fit(X, y)
    score = accuracy_score(y, model.predict(X))
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_metric("accuracy", score)
    mlflow.end_run()
    return {"accuracy": score}
