# ==============================================
# Django URL Configuration
# Cloud Monitoring & Self-Healing Application
# ==============================================

from django.urls import path, include
from app import views

urlpatterns = [
    # Dashboard UI
    path('', views.index, name='index'),

    # Health Check Endpoints (used by Kubernetes probes)
    path('health', views.health, name='health'),
    path('health/live', views.health_live, name='health_live'),
    path('health/ready', views.health_ready, name='health_ready'),

    # Prometheus Metrics Endpoint (/metrics)
    path('', include('django_prometheus.urls')),
]
