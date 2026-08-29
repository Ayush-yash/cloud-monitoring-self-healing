"""
Health check and monitoring views for the Cloud Monitoring & Self-Healing Application.

These endpoints are used by:
- Kubernetes Liveness Probe  → /health/live
- Kubernetes Readiness Probe → /health/ready
- Prometheus scraping        → /metrics (via django_prometheus)
- Dashboard UI               → /
"""

import logging
import time
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    """Render the Cloud Monitoring Dashboard UI."""
    return render(request, 'index.html')


def health(request):
    """
    Basic health check endpoint.
    Returns the overall application status.
    """
    logger.info("Health check requested")
    return JsonResponse({
        "status": "healthy",
        "app": "Cloud Monitoring & Self-Healing App",
        "version": "1.0.0"
    })


def health_live(request):
    """
    Kubernetes Liveness Probe endpoint.
    If this fails, Kubernetes will restart the container.
    """
    return JsonResponse({"status": "alive"})


def health_ready(request):
    """
    Kubernetes Readiness Probe endpoint.
    If this fails, Kubernetes stops routing traffic to this pod.
    """
    return JsonResponse({"status": "ready"})
