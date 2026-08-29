#!/bin/bash
# Chaos Engineering Demo: Testing Kubernetes Self-Healing
# This script deletes a random pod to simulate a failure and observes Kubernetes replacing it.

NAMESPACE="monitoring-app"
APP_LABEL="app=cloud-monitoring"

echo "=== Kubernetes Self-Healing Chaos Demo ==="
echo ""

# 1. Get the current running pods
echo "[1] Fetching currently running pods..."
kubectl get pods -n $NAMESPACE -l $APP_LABEL
echo ""

# 2. Select a pod to kill
POD_TO_KILL=$(kubectl get pods -n $NAMESPACE -l $APP_LABEL -o jsonpath='{.items[0].metadata.name}')

if [ -z "$POD_TO_KILL" ]; then
    echo "Error: No pods found for label $APP_LABEL in namespace $NAMESPACE!"
    exit 1
fi

echo "[2] Selecting pod for chaos testing: $POD_TO_KILL"
echo ""

# 3. Kill the pod
echo "[3] Deleting pod $POD_TO_KILL to simulate a crash..."
kubectl delete pod $POD_TO_KILL -n $NAMESPACE

echo ""
echo "[4] Pod deleted! Watching Kubernetes automatically recreate the replacement pod."
echo "Press Ctrl+C to exit the watch screen when you are satisfied."
echo "--------------------------------------------------------"

# 4. Watch the pods get recreated
kubectl get pods -n $NAMESPACE -l $APP_LABEL -w
