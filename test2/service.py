# https://www.kubeflow.org/docs/components/pipelines/v1/sdk/connect-api/
# kubeflow 실행 명령어: kubectl port-forward --namespace kubeflow svc/ml-pipeline-ui 3000:80
# kubeflow 실행 명령어: kubectl port-forward --namespace mlops svc/ml-pipeline-ui 3000:80
# import kfp

# client = kfp.Client(host="http://localhost:3000")
# # run the pipeline in v2 compatibility mode

# from kfp import dsl
# from kfp import compiler

# @dsl.component
# def comp(message: str) -> str:
#     print(message)
#     return message

# @dsl.pipeline
# def my_pipeline(message: str) -> str:
#     """My ML pipeline."""
#     return comp(message=message).output

# compiler.Compiler().compile(my_pipeline, package_path='pipeline.yaml')
from kfp import dsl
import kfp
@dsl.component
def add(a: float, b: float) -> float:
    '''Calculates sum of two arguments'''
    return a + b


@dsl.pipeline(
    name='Addition pipeline',
    description='An example pipeline that performs addition calculations.')
def add_pipeline(
    a: float = 1.0,
    b: float = 7.0,
):
    first_add_task = add(a=a, b=4.0)
    second_add_task = add(a=first_add_task.output, b=b)


client = kfp.Client()
client.create_run_from_pipeline_func(
    add_pipeline, arguments={
        'a': 7.0,
        'b': 8.0
    })

# kfp run create --name add_pipeline_run --pipeline-function add_pipeline --arguments a=7.0,b=8.0