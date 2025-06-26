
# 🌐 Check Internet App – Setup & Deployment Guide

This setup guide walks through deploying the **Check Internet App** — a simple web app confirming internet access — on a **DigitalOcean Kubernetes (DOKS)** cluster. This includes provisioning infrastructure, containerizing the app, configuring autoscaling, and setting up a load balancer.

---

## 📁 Project Structure

```
.
├── check-internet-app/         # Flask app source code
├── Dockerfile                  # Image build file
├── k8s/
│   ├── deployment.yaml         # Kubernetes Deployment
│   ├── service.yaml            # LoadBalancer Service
│   ├── hpa.yaml                # Horizontal Pod Autoscaler
└── README.md                   # This guide
```

---

## 🧰 Prerequisites

Ensure you have the following tools installed and configured:

- ✅ A [DigitalOcean account](https://www.digitalocean.com/)
- ✅ [Docker](https://www.docker.com/products/docker-desktop) CLI
- ✅ [doctl](https://docs.digitalocean.com/reference/doctl/) CLI (v1.96+), authenticated
- ✅ [kubectl](https://kubernetes.io/docs/tasks/tools/) CLI

---

## 🧱 1. Provision Infrastructure

### 1.1 Login & Create Container Registry

```bash
doctl auth init
doctl registry create check-internet
doctl registry login
```

### 1.2 Create Kubernetes Cluster

```bash
doctl kubernetes cluster create check-internet-cluster --count=2 --region=sfo2 --size=s-2vcpu-2gb
doctl kubernetes cluster kubeconfig save check-internet-cluster
```

### 1.3 Connect Registry to Cluster

```bash
doctl kubernetes cluster registry connect check-internet-cluster
```

---

## 🐳 2. Build and Push Docker Image

### 2.1 Build the Image

```bash
docker build -t registry.digitalocean.com/check-internet/check-internet-app:latest .
```

### 2.2 Push the Image

```bash
docker push registry.digitalocean.com/check-internet/check-internet-app:latest
```

---

## 🚀 3. Deploy the App on Kubernetes

### 3.1 Apply Manifests

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

> ⚠️ Ensure your YAML files use the correct `imagePullSecrets` and `image` path.

---

## 🌐 4. Access the Web App

### 4.1 Get Load Balancer IP

```bash
kubectl get svc check-internet-service
```

Visit: `http://<external-ip>`

Expected Output: `✅ Yes, you're connected to the internet.`

---

## 📊 5. Optional Testing and Monitoring

### 5.1 Simulate Load

```bash
hey -z 30s -c 20 http://<external-ip>
```

### 5.2 Watch Autoscaling

```bash
kubectl get hpa
kubectl get pods -w
```

### 5.3 Check Logs

```bash
kubectl logs -l app=check-internet-app
```

---

## 📬 Contact

For support or improvements, open an issue or contact your TAM team.
