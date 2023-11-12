# https://www.kubeflow.org/docs/components/pipelines/v1/sdk/connect-api/
# kubeflow 실행 명령어: kubectl port-forward --namespace kubeflow svc/ml-pipeline-ui 3000:80
import kfp

client = kfp.Client(host="http://localhost:3000")

print(client.list_experiments())