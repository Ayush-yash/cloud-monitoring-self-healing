# Cloud Monitoring & Self-Healing Infrastructure
> A production-ready Kubernetes infrastructure featuring self-healing, auto-scaling, and a full observability stack.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=flat&logo=django)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Native-326CE5?style=flat&logo=kubernetes)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C?style=flat&logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?style=flat&logo=grafana)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🏗️ Architecture

```text
User 
 └──▶ NGINX Ingress (cert-manager HTTPS)
       └──▶ K8s Service (NodePort)
             ├──▶ Django Pod 1 (Gunicorn)
             ├──▶ Django Pod 2 (Gunicorn) ◀── HPA (Auto-Scaling)
             └──▶ Django Pod 3 (Gunicorn)
                    │
                    ├──▶ Prometheus (Scrapes /metrics) ──▶ Alertmanager (Slack/Email Alerts)
                    │       └──▶ Grafana (Visualizes metrics)
                    │
                    └──▶ Promtail (Reads container logs)
                            └──▶ Loki (Centralized logging)
```

## ✨ Features

- [x] **Self-Healing:** Kubernetes automatically replaces crashed pods using liveness/readiness probes.
- [x] **Auto-Scaling:** HPA scales pods from 2 to 5 based on CPU utilization (target 50%).
- [x] **Full Observability Stack:** Prometheus metrics, Grafana dashboards, and Loki centralized logs.
- [x] **Proactive Alerting:** Alertmanager sends Slack notifications for pod crashes, high CPU, and high error rates.
- [x] **CI/CD Pipeline:** GitHub Actions auto-tests, builds the Docker image, and deploys to K8s on every push.
- [x] **Security:** Kubernetes Secrets, ConfigMaps, HTTPS via cert-manager, and env-based configuration.
- [x] **Chaos Engineering:** Included `chaos-test.sh` script to demonstrate self-healing in real-time.
- [x] **Structured JSON Logging:** `python-json-logger` for machine-parseable, easily searchable logs.
- [x] **Production-Ready:** Gunicorn WSGI server, strict resource limits, and multi-replica deployments.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Backend** | Python 3.10, Django 5.0, Gunicorn |
| **Containerization** | Docker, `python:3.10-slim` |
| **Orchestration** | Kubernetes (Minikube), HPA |
| **Observability** | Prometheus, Grafana, Loki, Promtail |
| **Alerting** | Alertmanager (Slack/Email) |
| **Routing & TLS** | cert-manager, NGINX Ingress |
| **CI/CD** | GitHub Actions |

## 🚀 Quick Start

### 1. Local Development
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

### 2. Docker
```bash
docker build -t cloud-monitoring-app .
docker run -p 8000:8000 cloud-monitoring-app
```

### 3. Kubernetes (Minikube)
```bash
minikube start --addons=ingress,metrics-server
kubectl apply -k k8s/
kubectl get pods -w
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Dashboard UI |
| `GET` | `/health` | Application health status (`{"status": "healthy"}`) |
| `GET` | `/health/live` | Kubernetes Liveness Probe (`{"status": "alive"}`) |
| `GET` | `/health/ready` | Kubernetes Readiness Probe (`{"status": "ready"}`) |
| `GET` | `/metrics` | Exposes Prometheus metrics |

## 🌪️ Self-Healing Demo (Chaos Engineering)

To demonstrate the self-healing capabilities of the infrastructure, run the chaos testing script:

```bash
./chaos-test.sh
```
This script intentionally terminates random pods. Watch Kubernetes instantly detect the failure via Liveness Probes and automatically spin up replacement pods to maintain the desired replica count.

## 📂 Project Structure

```text
cloud-monitoring-self-healing/
├── app/                          # Django Application
├── k8s/                          # Kubernetes Manifests
├── docs/                         # Documentation
├── .github/workflows/ci-cd.yml   # GitHub Actions Pipeline
├── Dockerfile
├── chaos-test.sh                 # Chaos engineering demo script
├── grafana-dashboard.json
├── requirements.txt
└── README.md
```

## 📚 Documentation

Detailed setup guides for each component:

- [AWS EC2 Setup](docs/aws-ec2-setup.md)
- [Monitoring Setup (Prometheus & Grafana)](docs/monitoring-setup.md)
- [Logging Setup (Loki & Promtail)](docs/logging-setup.md)
- [Alerting Setup (Alertmanager)](docs/alerting-setup.md)
- [Autoscaling Setup (HPA)](docs/autoscaling-setup.md)
- [Ingress & HTTPS Setup](docs/ingress-https-setup.md)
- [CI/CD Pipeline Setup](docs/ci-cd-setup.md)

## 🧪 Testing

Run the automated test suite:

```bash
python manage.py test
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).
