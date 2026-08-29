# AWS EC2 Setup for Cloud Monitoring & Self-Healing App

This guide provides simple steps for provisioning and configuring an Ubuntu EC2 instance on AWS to run the application and prepare for Kubernetes deployments using Minikube.

## 1. Creating the EC2 Instance (AWS Console)
1. Go to **EC2 Dashboard** -> **Launch Instances**.
2. **Name**: `cloud-monitoring-host` (or any preferred name).
3. **AMI**: Select **Ubuntu Server 22.04 LTS** (or 24.04 LTS).
4. **Instance Type**: Select `t2.medium` or higher (Minikube requires at least 2 CPUs and 2GB RAM).
5. **Key Pair**: Create a new `.pem` key pair or select an existing one. Save it securely.
6. **Network Settings** -> **Security Group**:
   - **Inbound Rules**: 
     - **SSH (Port 22)**: Allow from your IP (or anywhere `0.0.0.0/0` if necessary).
     - **HTTP (Port 80)**: Allow from anywhere for standard web traffic.
     - **HTTPS (Port 443)**: Allow from anywhere for secure web traffic.
   - *Note: Avoid opening unnecessary ports like 8000 globally unless explicitly required for external testing. Keep the Security Group locked down.*
7. **Storage**: Allocate at least **20 GB** (gp2/gp3).
8. Click **Launch Instance**.

## 2. SSH Connection
Once the instance is running, grab the **Public IPv4 Address** from the console. 

Run the following locally:
```bash
# Secure the key file (Mac/Linux only)
chmod 400 your-key.pem

# Connect to the server
ssh -i /path/to/your-key.pem ubuntu@<YOUR_EC2_PUBLIC_IP>
```

---

## 3. Environment Setup & Installations

The following commands should be run directly on the Ubuntu EC2 instance.

### Step 3.1: Basic Linux Setup & Updates
```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y curl wget apt-transport-https virtualenv software-properties-common
```

### Step 3.2: Install Docker
```bash
# Install Docker
sudo apt install -y docker.io

# Add the ubuntu user to the docker group so you don't need 'sudo' for docker commands
sudo usermod -aG docker $USER
```
*(You will need to log out and log back in, or run `newgrp docker`, for the group change to take effect).*

### Step 3.3: Install kubectl
```bash
# Download the latest kubectl binary
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make it executable and move it to your PATH
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

### Step 3.4: Install Minikube
```bash
# Download the Minikube binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Install it to your PATH
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

---

## 4. Verifying the Installations

Run these commands to ensure everything is installed correctly:

```bash
# 1. Verify Docker
docker --version
docker ps

# 2. Verify kubectl
kubectl version --client

# 3. Verify Minikube
minikube version
```

*Note: We are not starting Minikube or deploying Kubernetes components yet. This phase is purely for environment preparation.*
