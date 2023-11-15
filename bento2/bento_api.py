import numpy as np
import bentoml
from bentoml.io import NumpyNdarray


# iris_clf_runner1 = bentoml.sklearn.get("AdaBoostClassifier_model:latest").to_runner()
# svc_ada = bentoml.Service("AdaBoostClassifier_model", runners=[iris_clf_runner1])

iris_clf_runner = bentoml.sklearn.get("iris_classifier:latest").to_runner()

svc = bentoml.Service("iris_classifier", runners=[iris_clf_runner])

@svc.api(input=NumpyNdarray(), output=NumpyNdarray())
def classify(input_series: np.ndarray) -> np.ndarray:
    result = iris_clf_runner.predict.run(input_series)
    return result

# iris_clf_runner2 = bentoml.sklearn.get("AdaBoostClassifier_model:latest").to_runner()
# svc_ada = bentoml.Service("AdaBoostClassifier_model", runners=[iris_clf_runner2])

# @svc_ada.api(
#     input=NumpyNdarray(),
#     output=NumpyNdarray(),
#     route="v1/models/AdaBoostClassifier_model/predict"
# )
# def any_func_name(input_series: np.ndarray) -> np.ndarray:
#     result = iris_clf_runner2.predict.run(input_series)
#     return result