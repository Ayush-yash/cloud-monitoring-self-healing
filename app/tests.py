"""
Unit Tests for Cloud Monitoring & Self-Healing Application.
Tests all health check endpoints used by Kubernetes probes.
"""

from django.test import TestCase, Client
import json


class DashboardTests(TestCase):
    """Tests for the main dashboard UI."""

    def setUp(self):
        self.client = Client()

    def test_dashboard_loads(self):
        """Dashboard should return 200 and render HTML."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CloudMonitor')


class HealthEndpointTests(TestCase):
    """Tests for all health check API endpoints."""

    def setUp(self):
        self.client = Client()

    def test_health_returns_healthy(self):
        """GET /health should return status=healthy with app info."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('version', data)

    def test_liveness_probe(self):
        """GET /health/live is used by Kubernetes liveness probe."""
        response = self.client.get('/health/live')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'alive')

    def test_readiness_probe(self):
        """GET /health/ready is used by Kubernetes readiness probe."""
        response = self.client.get('/health/ready')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'ready')

    def test_health_content_type_is_json(self):
        """All health endpoints should return application/json."""
        for endpoint in ['/health', '/health/live', '/health/ready']:
            response = self.client.get(endpoint)
            self.assertEqual(
                response['Content-Type'],
                'application/json',
                f"{endpoint} did not return JSON"
            )
