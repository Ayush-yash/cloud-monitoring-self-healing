# Kubernetes Autoscaling Setup & Testing

This guide explains how to enable Horizontal Pod Autoscaling (HPA) in Minikube for our Cloud Monitoring & Self-Healing App.

## 1. Enable Metrics Server
Kubernetes requires metrics data to know when to scale pods up or down. In Minikube, you can easily enable the built-in metrics server:

```bash
# Enable the metrics server addon
minikube addons enable metrics-server

# Verify it is running
kubectl get pods -n kube-system | grep metrics-server
```

## 2. Apply HPA Configuration
Apply the `hpa.yaml` file to create the Horizontal Pod Autoscaler. It is configured to maintain an average CPU utilization of 50% across all pods, scaling between a minimum of 2 and a maximum of 5 pods.

```bash
kubectl apply -f k8s/hpa.yaml

# Check the HPA status
kubectl get hpa -n monitoring-app
```
*(Note: Initially, under "TARGETS", you might see `<unknown>/50%`. It takes a minute or two for the metrics server to collect the first data points. Once collected, it will show something like `2%/50%`.)*

## 3. Testing the Autoscaler (Generating Load)
To see the autoscaler in action, we need to artificially generate CPU load so that it breaches the 50% target.

Open a new terminal window and run a temporary pod that continually sends requests to your service:

```bash
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -n monitoring-app -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://cloud-monitoring-service:8000/health; done"
```

## 4. Watch the Scaling Event
Go back to your primary terminal window and watch the HPA status and pod counts update:

```bash
# Watch the HPA metrics (CPU utilization will climb)
kubectl get hpa -n monitoring-app -w

# Watch new pods being spun up
kubectl get pods -n monitoring-app -w
```

Once CPU utilization goes above 50%, you will see Kubernetes automatically provision new replica pods (up to 5 maximum) to handle the load.

## 5. Scaling Down
Stop the load generator (press `Ctrl+C` in that terminal). Watch the HPA again. After a cooldown period (usually 5 minutes), Kubernetes will gracefully scale the pods back down to the minimum of 2 replicas as CPU usage returns to near 0%.
