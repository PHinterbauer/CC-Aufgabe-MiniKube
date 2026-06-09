$ErrorActionPreference = "Stop"

Write-Host "Starting minikube..."
minikube start --driver=docker

Write-Host "Configuring Docker to use the minikube daemon..."
minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "Building image test-server:latest..."
docker build -t test-server:latest -f server/Dockerfile .

Write-Host "Deploying to Kubernetes..."
kubectl apply -f myapp.yml

Write-Host "Waiting for rollout..."
kubectl rollout status deployment/myapp

Write-Host "Port-forwarding to http://localhost:8000 ..."
kubectl port-forward deployment/myapp 8000:8000
