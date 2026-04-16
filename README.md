# Flask Contacts CRUD App — Kubernetes / Minikube

A Python Flask REST API + Web UI for managing contacts (name, phone, address), backed by MySQL, deployed on Minikube.

---

## Project Structure

```
flask-crud-app/
├── app.py                      # Flask application
├── requirements.txt
├── Dockerfile
├── deploy.sh                   # One-command deploy
├── teardown.sh                 # One-command teardown
├── templates/
│   └── index.html              # Web UI
└── k8s/
    ├── secret.yaml             # MySQL credentials (base64)
    ├── mysql-pvc.yaml          # Persistent Volume Claim
    ├── mysql-deployment.yaml   # MySQL Deployment + Service
    └── flask-deployment.yaml   # Flask Deployment + NodePort Service
```

---

## Prerequisites

- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed and running
- `kubectl` configured
- Docker installed

```bash
minikube start
```

---

## Quick Deploy

```bash
chmod +x deploy.sh teardown.sh
./deploy.sh
```

The script will:
1. Point your Docker CLI at Minikube's internal Docker daemon
2. Build the `flask-contacts:latest` image inside Minikube
3. Apply all Kubernetes manifests in order
4. Wait for rollouts to complete
5. Print the URL to access the app

---

## Manual Deploy (step-by-step)

```bash
# 1. Use Minikube's Docker
eval $(minikube docker-env)

# 2. Build the image
docker build -t flask-contacts:latest .

# 3. Apply manifests
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/mysql-pvc.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/flask-deployment.yaml

# 4. Check status
kubectl get pods
kubectl get services

# 5. Get the URL
minikube service flask-service --url
```

---

## REST API Reference

| Method | Endpoint                  | Description          |
|--------|---------------------------|----------------------|
| GET    | `/api/contacts`           | List all contacts    |
| GET    | `/api/contacts/<id>`      | Get one contact      |
| POST   | `/api/contacts`           | Create a contact     |
| PUT    | `/api/contacts/<id>`      | Update a contact     |
| DELETE | `/api/contacts/<id>`      | Delete a contact     |
| GET    | `/health`                 | Health check         |

### Example: Create a contact

```bash
curl -X POST http://<MINIKUBE_URL>/api/contacts \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","phone":"+1 555 123 4567","address":"123 Main St"}'
```

### Example: Update a contact

```bash
curl -X PUT http://<MINIKUBE_URL>/api/contacts/1 \
  -H "Content-Type: application/json" \
  -d '{"phone":"+1 555 999 0000"}'
```

---

## Changing Credentials

The default credentials in `k8s/secret.yaml` are:

| Key              | Default value  |
|------------------|----------------|
| mysql-root-password | rootpassword |
| mysql-password   | flaskpassword  |
| mysql-user       | flaskuser      |
| mysql-database   | contactsdb     |

To use different values, base64-encode them:

```bash
echo -n 'mynewpassword' | base64
```

Then update `k8s/secret.yaml` before deploying.

---

## Scaling the Flask App

```bash
kubectl scale deployment flask-app --replicas=3
```

---

## Teardown

```bash
./teardown.sh
```

---

## Troubleshooting

```bash
# Check pod logs
kubectl logs deployment/flask-app
kubectl logs deployment/mysql

# Describe a failing pod
kubectl describe pod <pod-name>

# Shell into the Flask container
kubectl exec -it deployment/flask-app -- /bin/bash

# Shell into MySQL
kubectl exec -it deployment/mysql -- mysql -u flaskuser -pflaskpassword contactsdb
```
