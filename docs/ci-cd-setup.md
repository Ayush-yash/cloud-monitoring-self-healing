# CI/CD Setup with GitHub Actions

This guide explains how the Continuous Integration and Continuous Deployment (CI/CD) pipeline is set up for the Cloud Monitoring application.

## 1. How the Pipeline Works
We have created a GitHub Actions workflow (`.github/workflows/ci-cd.yml`).
Whenever you push code to the `main` branch, the pipeline will automatically:
1. Checkout your code.
2. Setup Python and run a basic Django syntax check (`python manage.py check`).
3. Build a new Docker image and push it to Docker Hub (tagged with the unique commit SHA).
4. Connect to your Kubernetes cluster and update the `cloud-monitoring-app` deployment to use the newly built image.

## 2. Setting Up GitHub Secrets
For the pipeline to work, it needs permission to push to your Docker Hub and connect to your Kubernetes cluster. You must add these credentials securely in GitHub.

1. Go to your GitHub Repository.
2. Click on **Settings** -> **Secrets and variables** -> **Actions**.
3. Click **New repository secret**.

Add the following three secrets exactly as named:

* `DOCKER_USERNAME`: Your Docker Hub username.
* `DOCKER_PASSWORD`: Your Docker Hub password or Personal Access Token (PAT).
* `KUBECONFIG`: The raw contents of your `.kube/config` file (this allows GitHub Actions to talk to your live Kubernetes cluster).

*(Note: If you are using Minikube locally, a cloud runner cannot reach your local IP. To fully test the deploy step, your Kubernetes cluster must be publicly accessible, like on an AWS EKS/EC2 instance with an exposed API server).*

## 3. Customizing the Workflow
Open `.github/workflows/ci-cd.yml` and modify the following block to match your actual Docker Hub repository name:

```yaml
env:
  DOCKER_IMAGE: your-dockerhub-username/cloud-monitoring-app
```

## 4. Triggering the Pipeline
The pipeline is completely automated. To trigger it:
1. Make a change to the code (e.g., update the version number in `app/views.py`).
2. Commit your changes.
3. Push to the `main` branch.
4. Go to the **Actions** tab in your GitHub repository to watch the pipeline run!
