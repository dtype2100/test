import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = load_iris()
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier().fit(X_train, y_train)

joblib.dump(model, 'model.pkl')

loaded_model = joblib.load('model.pkl')

class PredictIn(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    
class PredictOut(BaseModel):
    iris_class: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.post("/predict/", response_model=PredictOut)
# def predict(data: PredictIn) -> PredictOut:
#     df = pd.DataFrame([data.dict()]) # sepal_length
#     df.columns = df.columns.str.replace("_", " ") # sepal length
#     df = df.add_suffix(" (cm)") # sepal length (cm)
#     pred = model.predict(df).item()
#     return PredictOut(iris_class=pred)

@app.post("/predict", response_model=PredictOut)
def predict(data: PredictIn) -> PredictOut:
    df = pd.DataFrame([data.dict()])
    df.columns = df.columns.str.replace("_", " ")
    df = df.add_suffix(" (cm)")
    pred = model.predict(df).item()
    return PredictOut(iris_class=pred)
