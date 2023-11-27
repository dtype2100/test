FROM python
RUN pip install -U pip &&\
    pip install mlflow

CMD ["mlflow", "server", "--host", "127.0.0.1"]