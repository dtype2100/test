import numpy as np
import bentoml
from bentoml.io import NumpyNdarray
# import mlflow
# 첫 번째 모델을 추가합니다.
# iris_clf_runner = bentoml.sklearn.get("random_forest_model:latest").to_runner()
runner1 = bentoml.mlflow.get("random_forest_model:latest").to_runner()
# 두 번째 모델을 추가합니다.
runner2 = bentoml.mlflow.get("random_forest_model:latest").to_runner()

# BentoService를 생성하고 위에서 추가한 모델들을 runners에 포함시킵니다.
svc = bentoml.Service("multi_model_classifier", runners=[runner1]) # , another_model_runner

@svc.api(
    input=NumpyNdarray(),
    output=NumpyNdarray(),
    route="v1/models/multi_model_classifier/predict"
)
def any_func_name(input_series: np.ndarray) -> np.ndarray:
    # 모델 선택 및 예측을 수행합니다.
    result1 = runner1.predict.run(input_series)  # 원하는 모델로 변경 가능
    # result2 = runner2.predict.run(input_series)
    return result1 # {1:result1, 2:result2} 
