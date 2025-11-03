# PowerShell script for deploying yliveticker to Google Cloud Platform
# Usage: .\deploy-gcp.ps1 -ProjectID "your-project-id" -DeploymentType "cloudrun"

param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectID,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("cloudrun", "computeengine", "gke")]
    [string]$DeploymentType = "cloudrun",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  YLiveTicker GCP Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set the project
Write-Host "Setting project to: $ProjectID" -ForegroundColor Yellow
gcloud config set project $ProjectID

# Enable required APIs
Write-Host "Enabling required GCP APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build the container image
Write-Host "Building container image..." -ForegroundColor Yellow
gcloud builds submit --tag gcr.io/$ProjectID/yliveticker

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Please check the errors above." -ForegroundColor Red
    exit 1
}

Write-Host "Build successful!" -ForegroundColor Green

# Deploy based on type
switch ($DeploymentType) {
    "cloudrun" {
        Write-Host "Deploying to Cloud Run..." -ForegroundColor Yellow
        gcloud run deploy yliveticker `
            --image gcr.io/$ProjectID/yliveticker `
            --platform managed `
            --region $Region `
            --cpu 1 `
            --memory 512Mi `
            --max-instances 1 `
            --min-instances 1 `
            --timeout 3600 `
            --no-allow-unauthenticated
        
        Write-Host ""
        Write-Host "Cloud Run deployment complete!" -ForegroundColor Green
        Write-Host "To view logs, run:" -ForegroundColor Cyan
        Write-Host "  gcloud run services logs tail yliveticker --region $Region" -ForegroundColor White
    }
    
    "computeengine" {
        Write-Host "Deploying to Compute Engine..." -ForegroundColor Yellow
        gcloud compute instances create-with-container yliveticker-vm `
            --container-image=gcr.io/$ProjectID/yliveticker `
            --machine-type=e2-micro `
            --zone=$Region-a `
            --container-restart-policy=always `
            --boot-disk-size=10GB
        
        Write-Host ""
        Write-Host "Compute Engine deployment complete!" -ForegroundColor Green
        Write-Host "To SSH into the VM, run:" -ForegroundColor Cyan
        Write-Host "  gcloud compute ssh yliveticker-vm --zone=$Region-a" -ForegroundColor White
    }
    
    "gke" {
        Write-Host "Deploying to Google Kubernetes Engine..." -ForegroundColor Yellow
        Write-Host "Note: GKE deployment requires additional setup. Please see DEPLOYMENT.md" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Creating GKE cluster..." -ForegroundColor Yellow
        gcloud container clusters create yliveticker-cluster `
            --num-nodes=1 `
            --machine-type=e2-small `
            --zone=$Region-a
        
        Write-Host "Updating k8s-deployment.yaml with project ID..." -ForegroundColor Yellow
        $k8sContent = Get-Content k8s-deployment.yaml -Raw
        $k8sContent = $k8sContent -replace "YOUR_PROJECT_ID", $ProjectID
        $k8sContent | Set-Content k8s-deployment.yaml
        
        Write-Host "Deploying to GKE..." -ForegroundColor Yellow
        kubectl apply -f k8s-deployment.yaml
        
        Write-Host ""
        Write-Host "GKE deployment complete!" -ForegroundColor Green
        Write-Host "To view logs, run:" -ForegroundColor Cyan
        Write-Host "  kubectl logs -f deployment/yliveticker" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

