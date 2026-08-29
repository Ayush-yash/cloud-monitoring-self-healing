# Domain Routing and HTTPS Setup

This guide explains how to expose the Cloud Monitoring application via a custom domain (`cloud-monitor.local`) using the NGINX Ingress Controller, and how to automatically provision TLS certificates using `cert-manager` and Let's Encrypt.

## 1. Enable NGINX Ingress Controller in Minikube
Minikube has a built-in addon for the NGINX Ingress Controller. Enable it by running:
```bash
minikube addons enable ingress
```
*Verify the ingress controller pods are running in the `ingress-nginx` namespace:*
```bash
kubectl get pods -n ingress-nginx
```

## 2. Install cert-manager
`cert-manager` automates the management and issuance of TLS certificates from various issuing sources, including Let's Encrypt.

Install `cert-manager` using standard Kubernetes manifests:
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml
```
Wait for the pods to be ready:
```bash
kubectl get pods --namespace cert-manager
```

## 3. Apply the Configurations
We have created two new manifests:
* **`k8s/clusterissuer.yaml`**: Configures `cert-manager` to talk to the Let's Encrypt staging API. *(Note: You should update `your-email@example.com` in this file).*
* **`k8s/ingress.yaml`**: Routes external HTTP/HTTPS traffic from `cloud-monitor.local` to our internal `cloud-monitoring-service`.

Apply them to the cluster:
```bash
kubectl apply -f k8s/clusterissuer.yaml
kubectl apply -f k8s/ingress.yaml
```

## 4. Local Testing (/etc/hosts)
Since `cloud-monitor.local` is not a real registered domain, you need to trick your local computer into routing this domain to your Minikube cluster's IP address.

1. Get the Minikube IP address:
   ```bash
   minikube ip
   ```
2. Open your system's hosts file:
   * **Linux/Mac:** `sudo nano /etc/hosts`
   * **Windows:** Open Notepad as Administrator and edit `C:\Windows\System32\drivers\etc\hosts`
3. Add a line at the bottom linking the Minikube IP to the domain:
   ```text
   <MINIKUBE_IP>   cloud-monitor.local
   ```
   *(e.g., `192.168.49.2 cloud-monitor.local`)*

## 5. Verify the Application
Now, open your web browser and navigate to:
**https://cloud-monitor.local**

*Note on TLS:* Because we are using the Let's Encrypt "Staging" environment (to avoid rate limits during testing) or a self-signed cert on local setups, your browser will show a "Your connection is not private" warning. This is expected. In Chrome, you can type `thisisunsafe` blindly on the error page, or click Advanced -> Proceed to see the site.

For a production environment, you would use a real domain name and update the `ClusterIssuer` to point to the Let's Encrypt production API (`https://acme-v02.api.letsencrypt.org/directory`).
