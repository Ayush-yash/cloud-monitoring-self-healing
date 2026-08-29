# Monitoring Setup (Prometheus + Grafana)

This guide explains how to deploy and configure Prometheus and Grafana to monitor the Django application running in Kubernetes.

## 1. Apply Monitoring Configurations
We have created Kubernetes manifests for Prometheus and Grafana. Run the following command to deploy them to the `monitoring-app` namespace:

```bash
kubectl apply -f k8s/prometheus-config.yaml
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/grafana.yaml
```

Wait a minute for the pods to spin up:
```bash
kubectl get pods -n monitoring-app
```

## 2. Access Prometheus
Prometheus scrapes the `/metrics` endpoint of the Django app every 15 seconds.
You can access the Prometheus UI via port-forwarding:

```bash
kubectl port-forward svc/prometheus-service 9090:9090 -n monitoring-app
```
Then open `http://localhost:9090` in your browser. You can go to **Status -> Targets** to verify that it is successfully scraping the `django-app` target.

## 3. Access Grafana
Grafana is used to visualize the Prometheus data.
Port-forward to the Grafana service:

```bash
kubectl port-forward svc/grafana-service 3000:3000 -n monitoring-app
```
Then open `http://localhost:3000` in your browser.
* **Username**: admin
* **Password**: admin (Configured via deployment env vars)

## 4. Configure Grafana Dashboard
1. Once logged into Grafana, go to **Data Sources** and add a new **Prometheus** data source.
2. Set the HTTP URL to `http://prometheus-service.monitoring-app.svc.cluster.local:9090` and save.
3. Go to **Dashboards -> Import**.
4. Upload the `grafana-dashboard.json` file located in the root of this project repository.
5. Select the Prometheus data source you just created and click Import.

You will now see a dashboard displaying the Request Rate and Error Rate for your Django application!
