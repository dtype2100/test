# https://www.kubeflow.org/docs/components/pipelines/v2/pipelines/pipeline-basics/
# https://kubeflow-pipelines.readthedocs.io/en/stable/index.html
# https://towardsdatascience.com/how-to-create-and-deploy-a-kubeflow-machine-learning-pipeline-part-1-efea7a4b650f
# Run pipeline: https://www.kubeflow.org/docs/components/pipelines/v2/run-a-pipeline/
# https://www.kubeflow.org/docs/components/pipelines/v1/sdk/connect-api/
# pip install kfp

# kfp run create --experiment-name my-experiment --package-file ./kubeflow-pod.yaml

# kubectl port-forward --namespace kubeflow svc/ml-pipeline-ui 3000:80
# kubectl run kubeflow --image=kubeflow --dry-run=client -o yaml > kubeflow-pod.yaml
# cat kubeflow-pod.yaml
# kubectl apply -f kubeflow-pod.yaml
# kubectl delete -f kubeflow-pod.yaml

# import kfp
# kubeflow_namespace = "kubeflow"
# client = kfp.Client(host="http://localhost:3000")
# client = kfp.Client(host=f"http://ml-pipeline-ui.{kubeflow_namespace}")

# print(client.list_experiments())

# import kfp
# client = kfp.Client(host='http://127.0.0.1:3000')
# print(client.list_experiments())
import kfp
client = kfp.Client(host='http://localhost:3000')
print(client.list_experiments())
# https://v1-5-branch.kubeflow.org/docs/components/pipelines/sdk/connect-api/