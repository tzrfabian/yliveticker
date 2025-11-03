# Deploying yliveticker to Google Cloud Platform (GCP)

This guide covers multiple deployment options for the yliveticker application on GCP.

## Prerequisites

1. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud SDK**: Install from [cloud.google.com/sdk](https://cloud.google.com/sdk)
3. **Docker**: Install from [docker.com](https://www.docker.com/get-started)
4. **Project Setup**:
   ```bash
   # Login to GCP
   gcloud auth login
   
   # Create a new project (or use existing)
   gcloud projects create yliveticker-project --name="YLiveTicker"
   
   # Set the project as active
   gcloud config set project yliveticker-project
   
   # Enable required APIs
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

## Option 1: Cloud Run (Recommended)

Cloud Run is the easiest and most cost-effective option for running containerized applications.

### Step 1: Build and Test Locally

```bash
# Build the Docker image
docker build -t yliveticker .

# Test locally
docker run yliveticker
```

### Step 2: Deploy to Cloud Run

```bash
# Set your project ID
export PROJECT_ID=your-project-id

# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/yliveticker

# Deploy to Cloud Run
gcloud run deploy yliveticker \
  --image gcr.io/$PROJECT_ID/yliveticker \
  --platform managed \
  --region us-central1 \
  --cpu 1 \
  --memory 512Mi \
  --max-instances 1 \
  --min-instances 1 \
  --timeout 3600 \
  --no-allow-unauthenticated
```

### Step 3: View Logs

```bash
# Stream logs in real-time
gcloud run services logs tail yliveticker --region us-central1
```

### Important Notes for Cloud Run:
- Cloud Run is designed for HTTP services, but it works for websocket clients
- Set `--min-instances 1` to keep the connection alive
- Use `--no-allow-unauthenticated` since this doesn't serve HTTP requests
- Cost: ~$10-20/month with 1 instance running 24/7

## Option 2: Compute Engine (VM)

For more control and traditional VM deployment.

### Step 1: Create a VM Instance

```bash
# Create a VM with Container-Optimized OS
gcloud compute instances create-with-container yliveticker-vm \
  --container-image=gcr.io/$PROJECT_ID/yliveticker \
  --machine-type=e2-micro \
  --zone=us-central1-a \
  --container-restart-policy=always \
  --boot-disk-size=10GB
```

### Step 2: SSH into the VM (if needed)

```bash
gcloud compute ssh yliveticker-vm --zone=us-central1-a
```

### Step 3: View Logs

```bash
# SSH into the VM and view container logs
gcloud compute ssh yliveticker-vm --zone=us-central1-a
docker logs $(docker ps -q)
```

### Important Notes for Compute Engine:
- More expensive than Cloud Run (~$5-10/month for e2-micro)
- Full control over the VM
- Must manage updates and security patches

## Option 3: Google Kubernetes Engine (GKE)

For production-grade orchestration and scaling.

### Step 1: Create a GKE Cluster

```bash
# Create a small cluster
gcloud container clusters create yliveticker-cluster \
  --num-nodes=1 \
  --machine-type=e2-small \
  --zone=us-central1-a
```

### Step 2: Build and Push Image

```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/yliveticker
```

### Step 3: Create Kubernetes Deployment

Create a file `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yliveticker
spec:
  replicas: 1
  selector:
    matchLabels:
      app: yliveticker
  template:
    metadata:
      labels:
        app: yliveticker
    spec:
      containers:
      - name: yliveticker
        image: gcr.io/YOUR_PROJECT_ID/yliveticker
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Step 4: Deploy to GKE

```bash
# Apply the deployment
kubectl apply -f k8s-deployment.yaml

# View logs
kubectl logs -f deployment/yliveticker
```

### Important Notes for GKE:
- Most expensive option (~$50+/month)
- Best for production workloads requiring scaling
- Advanced orchestration features

## Option 4: Automated Deployment with Cloud Build

Use the included `cloudbuild.yaml` for CI/CD.

### Step 1: Connect to Source Repository

```bash
# If using GitHub
gcloud builds triggers create github \
  --repo-name=yliveticker \
  --repo-owner=YOUR_GITHUB_USERNAME \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

### Step 2: Push Changes

Every push to the `main` branch will automatically build and deploy.

## Customization

### Change Ticker Symbols

Edit `yliveticker/client_code.py` and modify the `ticker_names` list:

```python
ticker_names=[
    "AAPL",    # Apple
    "MSFT",    # Microsoft
    "GOOGL",   # Google
    "TSLA",    # Tesla
    "BTC-USD", # Bitcoin
]
```

### Environment Variables

You can pass environment variables in the deployment:

**Cloud Run:**
```bash
gcloud run deploy yliveticker \
  --image gcr.io/$PROJECT_ID/yliveticker \
  --set-env-vars PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```

**Compute Engine:**
```bash
gcloud compute instances create-with-container yliveticker-vm \
  --container-image=gcr.io/$PROJECT_ID/yliveticker \
  --container-env PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```

## Monitoring and Logging

### View Logs in Cloud Console

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Navigate to **Logging** > **Logs Explorer**
3. Filter by resource (Cloud Run service, VM, or GKE container)

### Set Up Alerts

```bash
# Example: Alert when service is down
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="YLiveTicker Down" \
  --condition-display-name="Service Down" \
  --condition-threshold-value=1 \
  --condition-threshold-duration=300s
```

## Cost Optimization

1. **Cloud Run**: Use `--max-instances 1` to limit scaling
2. **Compute Engine**: Use preemptible instances for development
3. **GKE**: Use autopilot mode or node auto-scaling
4. **All Options**: Set budgets and alerts in GCP Billing

## Troubleshooting

### Container Fails to Start

```bash
# View build logs
gcloud builds log $(gcloud builds list --limit=1 --format='value(id)')

# Test locally first
docker build -t yliveticker .
docker run yliveticker
```

### No Data Received

- Check if markets are open (data only flows during trading hours)
- Verify ticker symbols are correct
- Check websocket connection in logs

### Protobuf Errors

The Dockerfile already sets `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`. If issues persist:

```bash
# Rebuild with specific protobuf version
docker build --build-arg PROTOBUF_VERSION=3.20.3 -t yliveticker .
```

## Cleanup

### Remove Cloud Run Service

```bash
gcloud run services delete yliveticker --region us-central1
```

### Remove Compute Engine VM

```bash
gcloud compute instances delete yliveticker-vm --zone us-central1-a
```

### Remove GKE Cluster

```bash
gcloud container clusters delete yliveticker-cluster --zone us-central1-a
```

### Remove Container Images

```bash
gcloud container images delete gcr.io/$PROJECT_ID/yliveticker
```

## Support

For issues specific to:
- **GCP**: [cloud.google.com/support](https://cloud.google.com/support)
- **yliveticker**: [GitHub Issues](https://github.com/yahoofinancelive/yliveticker/issues)

## Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Compute Engine Documentation](https://cloud.google.com/compute/docs)
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

