# Centralized Logging Setup (Loki + Promtail)

This guide explains how to deploy Loki and Promtail to collect structured JSON logs from your Django application and view them in Grafana.

## 1. Apply Logging Configurations
We have created Kubernetes manifests for Loki (Log Aggregator) and Promtail (Log Agent). Run the following commands:

```bash
kubectl apply -f k8s/loki.yaml
kubectl apply -f k8s/promtail-config.yaml
kubectl apply -f k8s/promtail.yaml
```

Wait a minute for the pods to spin up:
```bash
kubectl get pods -n monitoring-app
```
*(You should see `loki` and `promtail` pods running.)*

## 2. Configure Grafana
Now that Loki is collecting logs, you need to add it to Grafana.

1. Port-forward the Grafana service (if not already running):
   ```bash
   kubectl port-forward svc/grafana-service 3000:3000 -n monitoring-app
   ```
2. Open `http://localhost:3000` (Login: admin / admin).
3. Go to **Connections -> Data Sources -> Add data source**.
4. Select **Loki**.
5. Set the HTTP URL to `http://loki-service.monitoring-app.svc.cluster.local:3100`.
6. Click **Save & Test**. You should see a success message.

## 3. Querying Logs in Grafana (LogQL)
To view and analyze your structured JSON logs:
1. Go to **Explore** (compass icon on the left menu).
2. Select **Loki** from the dropdown at the top.
3. You can use the Label Browser to select `{app="cloud-monitoring"}`.

### Example Queries
* **View all logs from the Django app:**
  ```logql
  {app="cloud-monitoring"}
  ```
* **Parse JSON logs and filter for warnings/errors:**
  ```logql
  {app="cloud-monitoring"} | json | level=~"WARNING|ERROR"
  ```
* **Filter by a specific API endpoint (e.g., /health/live):**
  ```logql
  {app="cloud-monitoring"} | json | message=~".*/health/live.*"
  ```
