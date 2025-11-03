# Quick Start: Deploy to GCP in 5 Minutes

This is the fastest way to get yliveticker running on Google Cloud Platform.

## Prerequisites

1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Login: `gcloud auth login`
3. Create a project in [GCP Console](https://console.cloud.google.com)

## Quick Deploy (Windows PowerShell)

```powershell
# Replace with your actual project ID
.\deploy-gcp.ps1 -ProjectID "your-project-id"
```

That's it! The script will:
- Enable required APIs
- Build your container
- Deploy to Cloud Run
- Show you how to view logs

## Quick Deploy (Mac/Linux Bash)

```bash
# Set your project ID
export PROJECT_ID="your-project-id"

# Set the project
gcloud config set project $PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/yliveticker
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

## View Live Data

```bash
# Watch the real-time ticker data
gcloud run services logs tail yliveticker --region us-central1
```

You should see market data streaming in real-time!

## Customize Tickers

Edit `yliveticker/client_code.py` and change the ticker symbols:

```python
ticker_names=[
    "AAPL",    # Apple
    "TSLA",    # Tesla
    "BTC-USD", # Bitcoin
    # Add your favorites here
]
```

Then redeploy:

```powershell
.\deploy-gcp.ps1 -ProjectID "your-project-id"
```

## Cost

With Cloud Run:
- First 2 million requests free per month
- ~$10-20/month for 1 instance running 24/7

## Stop/Delete

```bash
# Stop the service
gcloud run services delete yliveticker --region us-central1
```

## Need Help?

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Detailed deployment options
- Compute Engine setup
- Kubernetes (GKE) deployment
- Troubleshooting
- Advanced configuration

## What's Next?

- Monitor in [GCP Console](https://console.cloud.google.com/run)
- Set up alerts
- Save data to BigQuery
- Create a dashboard with Grafana

