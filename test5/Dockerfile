FROM amd/python:3.9-slim

WORKDIR /usr/app

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U pip &&\
    pip install scikit-learn==1.2.2 pandas==2.0.2

COPY train.py train.py

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

ENTRYPOINT "bin/bash"