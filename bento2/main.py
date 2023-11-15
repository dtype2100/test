from fastapi import FastAPI
import bentoml


iris_clf_runner1 = bentoml.sklearn.get("AdaBoostClassifier_model:latest").to_runner()
svc_ada = bentoml.Service("AdaBoostClassifier_model", runners=[iris_clf_runner1])

app = FastAPI()
svc_ada.mount_asgi_app(app)

@app.get("/")
def main():
    return 'test'

@app.post("/predict_fastapi")
def predict():
    results = iris_clf_runner1.predict.run()
    return { "prediction": results.tolist()[0] }