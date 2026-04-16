#!/usr/bin/env bash
# teardown.sh — remove all resources from the cluster
set -euo pipefail

echo "==> Deleting Flask and MySQL deployments..."
kubectl delete -f k8s/flask-deployment.yaml --ignore-not-found
kubectl delete -f k8s/mysql-deployment.yaml --ignore-not-found
kubectl delete -f k8s/mysql-pvc.yaml        --ignore-not-found
kubectl delete -f k8s/secret.yaml           --ignore-not-found

echo "✅  All resources removed."
