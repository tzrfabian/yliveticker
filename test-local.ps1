# PowerShell script to test yliveticker locally with Docker
# Usage: .\test-local.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  YLiveTicker Local Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerInstalled) {
    Write-Host "Error: Docker is not installed!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Docker is running
try {
    docker ps | Out-Null
} catch {
    Write-Host "Error: Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Docker is installed and running" -ForegroundColor Green
Write-Host ""

# Build the Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t yliveticker .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed. Please check the errors above." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Build successful!" -ForegroundColor Green
Write-Host ""

# Run the container
Write-Host "Starting yliveticker container..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Cyan
Write-Host ""
Write-Host "You should see market data streaming below:" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray

docker run --rm yliveticker

Write-Host ""
Write-Host "Container stopped." -ForegroundColor Yellow
Write-Host ""
Write-Host "To deploy to Easypanel, see: QUICKSTART.md" -ForegroundColor Cyan

