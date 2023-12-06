# wsl에 도커 엔진을 설치했더라도, 윈도우 로컬에서 도커 빌드할 때 Docker Desktop 설치 필요

from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
