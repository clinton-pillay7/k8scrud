#!/usr/bin/env bash
# deploy.sh — build image inside Minikube and apply all manifests
set -euo pipefail

echo "==> Pointing Docker CLI at Minikube's Docker daemon..."
eval $(minikube docker-env)

echo "==> Building Docker image: flask-contacts:latest"
docker build -t flask-contacts:latest .

echo "==> Applying Kubernetes manifests..."
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/mysql-pvc.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/flask-deployment.yaml

echo "==> Waiting for MySQL to be ready (this can take ~60s)..."
kubectl rollout status deployment/mysql --timeout=120s

echo "==> Waiting for Flask app to be ready..."
kubectl rollout status deployment/flask-app --timeout=90s

echo ""
echo "✅  Deployment complete!"
echo ""
echo "Access the app at:"
minikube service flask-service --url
