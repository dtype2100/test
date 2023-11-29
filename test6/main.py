from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# 입력 데이터를 정의하는 Pydantic 모델
class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    # 이하 필요한 특성들을 추가

class OutputData(BaseModel):
    result: str

# /predict 엔드포인트
@app.post("/predict")
def predict(data: InputData):
    # 모델 로드
    loaded_model = joblib.load('./clf_joblib.pkl')

    # 입력 데이터를 Pandas DataFrame으로 변환
    # df = pd.DataFrame([[data.feature1, data.feature2, data.feature3, data.feature4]])  # 필요한 특성들을 추가
    df = pd.DataFrame(data.model_dump)
    # 예측 수행
    print(df)
    pred = loaded_model.predict(df).item()
    df = df.add_suffix(" (cm)")
    print(df)
    # 예측 결과 반환
    return OutputData(result=pred)
