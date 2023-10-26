import cv2
import ray
from fastapi import FastAPI


app = FastAPI()

path = '.'

@ray.remote
def prepro(data):
    resized_data = cv2.resize(data, (224, 224))
    gray_data = cv2.cvtColor(resized_data, cv2.COLOR_BGR2GRAY) 
    return gray_data

@app.get("/")
async def test():
    data = await cv2.imread(path, cv2.IMREAD_COLOR)
    prepro_data = prepro.remote(data)
    return prepro_data