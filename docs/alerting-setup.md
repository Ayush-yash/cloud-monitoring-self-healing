# Alerting Setup (Prometheus + Alertmanager)

This guide explains how to set up and test Alertmanager with Slack notifications for our Cloud Monitoring & Self-Healing App.

## 1. Configure the Webhook URL
We have created an Alertmanager configuration with a placeholder Slack Webhook URL.
To receive real alerts:
1. Create an Incoming Webhook in your Slack workspace.
2. Open `k8s/alertmanager-config.yaml`.
3. Replace the `slack_api_url` value (`https://hooks.slack.com/...`) with your actual Slack webhook URL.
4. Apply the configuration:
   ```bash
   kubectl apply -f k8s/alertmanager-config.yaml
   ```

## 2. Deploy Alertmanager & Rules
Run the following commands to deploy the new alerting components:

```bash
kubectl apply -f k8s/prometheus-rules.yaml
kubectl apply -f k8s/prometheus-config.yaml
kubectl apply -f k8s/alertmanager.yaml
kubectl apply -f k8s/prometheus.yaml
```

*(Note: We applied `prometheus.yaml` again because we updated its volume mounts to include the alert rules.)*

## 3. The Alert Rules
We have defined three critical alerts in `k8s/prometheus-rules.yaml`:
1. **HighErrorRate**: Triggers if 5xx HTTP errors exceed 0.1 req/sec for 1 minute.
2. **HighCPUUsage**: Triggers if a pod's CPU usage exceeds 80% for 2 minutes.
3. **PodDownOrCrashLoop**: Triggers if a pod fails or restarts frequently.

## 4. How to Test an Alert
You can trigger the **HighCPUUsage** alert by running the load generator we used for autoscaling testing.

1. Port-forward the Alertmanager UI so you can see alerts being fired:
   ```bash
   kubectl port-forward svc/alertmanager-service 9093:9093 -n monitoring-app
   ```
   *Open `http://localhost:9093` in your browser.*

2. Run the load generator:
   ```bash
   kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -n monitoring-app -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://cloud-monitoring-service:8000/health; done"
   ```

3. Wait for about 2 minutes. The CPU usage will spike.
4. Check the Prometheus UI (`http://localhost:9090/alerts`) to see the alert turn from `PENDING` to `FIRING`.
5. Check the Alertmanager UI to see the alert routed. If you configured the Slack Webhook correctly, you will receive a message in your Slack channel!
