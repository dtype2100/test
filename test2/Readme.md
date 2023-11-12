kubectl port-forward -n kubuflow svc/ml-pipeline-ui 8080:80

kubectl port-forward --namespace kubeflow svc/ml-pipeline-ui 8080:80
=============
# pod
kubectl get pod 
kubectl run nginx -- image=nginx --dry-run=client -o yaml > nginx-pod.yaml
kubectl apply -f nginx-pod.yaml # yaml파일을 pod에 적용
kubectl delete pod nginx 

kubectl create namespace 네임스페이스명
kubectl get namespace # namespace 조회

# deployment: pod resource를 제어
- pod을 직접 생성하는 경우는 거의 없음
- 다수의 pod을 생성할 수 있어야함
- 새로운 버전으로 업데이트 필요
- 새로운 버전에 문제가 있는 경우 롤백 필요
- Deployment가 ReplicaSet 생성
- ReplicaSet: 원하는 개수의 pod이 running하도록 관리하는 resource
- ReplicaSet이 pod를 생성

kubectl create deployment nginx --image=nginx --dry-run=client -o yaml> deploy.yaml
kubectl apply -f deploy.yaml
kubectl get replicaset -o yaml # replicaset 확인
kubectl scale deployment nginx --replicas 3

kubectl set image deployment/nginx nginx=nginx:1.25.0-alpine
kubectl  rollout undo deployment nginx

# service
- service는 pod에 접근하기 위해 사용
- pod는 비영구적이기 때문에 언제든지 종료되고 생성될 수 있음
- service는 어떤 pod이 사용 가능하지 추적하고, 접근 가능한 ip주소를 반환하는 역할
- service를 통해 어떤 pod에 접근할지 선택하는 것이 아니라, 어떤 종류의 pod에 접근하고 싶은지 명시하고 사용할 수 있음

kubectl get pod -o wide
kubectl run curl --image=curlimages/curl --command sleep infinity
kubectl exec -it curl -- /bin/sh
curl http://10.42.0.78

- 서비스 생성
kubectl expose deployment nginx --port=80 --target-port=80
kubectl get service 
kubectl exec -it curl -- /bin/sh
curl http://nginx
