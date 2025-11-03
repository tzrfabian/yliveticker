# Deploying yliveticker to Easypanel

This guide will help you deploy the Yahoo Finance Live Ticker application to Easypanel in just a few minutes.

## What is Easypanel?

Easypanel is a modern server control panel that lets you deploy applications with Docker. It's perfect for:
- Self-hosted deployments on your own VPS
- Cost-effective alternative to cloud platforms
- Simple UI-based deployment
- No complex configuration needed

## Prerequisites

1. **Easypanel Instance**: You need Easypanel installed on a VPS or server
   - [Get Easypanel](https://easypanel.io/)
   - Install on any VPS (DigitalOcean, Hetzner, Linode, etc.)

2. **Git Repository**: Your code should be in a Git repository
   - GitHub, GitLab, or Gitea
   - Or use Easypanel's built-in Git support

## Method 1: Deploy from GitHub (Recommended)

### Step 1: Push Your Code to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Add your remote repository
git remote add origin https://github.com/YOUR_USERNAME/yliveticker.git
git push -u origin main
```

### Step 2: Create New App in Easypanel

1. Login to your Easypanel dashboard
2. Click **"Create"** → **"App"**
3. Enter app name: `yliveticker`
4. Choose **"Build from Source"**

### Step 3: Configure the Source

1. **Repository URL**: Enter your GitHub repository URL
2. **Branch**: `main` (or your default branch)
3. **Build Method**: Choose **"Dockerfile"**
4. Click **"Create"**

### Step 4: Configure Environment (Optional)

In the app settings, add environment variable if needed:
- **Key**: `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION`
- **Value**: `python`

### Step 5: Deploy

1. Click **"Deploy"** button
2. Wait for the build to complete (2-3 minutes)
3. The app will start automatically

### Step 6: View Logs

1. Go to your app in Easypanel
2. Click on **"Logs"** tab
3. You should see real-time market data streaming!

## Method 2: Deploy with Docker Compose

### Step 1: Create App from Docker Compose

1. In Easypanel, click **"Create"** → **"App"**
2. Choose **"Docker Compose"**
3. Paste the following configuration:

```yaml
version: '3.8'

services:
  yliveticker:
    image: ghcr.io/YOUR_USERNAME/yliveticker:latest
    restart: unless-stopped
    environment:
      - PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```

4. Click **"Create"**

### Step 2: Build and Push Image

First, build and push your Docker image:

```bash
# Build the image
docker build -t yliveticker .

# Tag for your registry
docker tag yliveticker ghcr.io/YOUR_USERNAME/yliveticker:latest

# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Push the image
docker push ghcr.io/YOUR_USERNAME/yliveticker:latest
```

Then deploy in Easypanel.

## Method 3: Deploy from Local Files

If you don't want to use Git:

### Step 1: Access Your Server

```bash
ssh user@your-server-ip
```

### Step 2: Upload Files

```bash
# On your local machine
scp -r yliveticker user@your-server-ip:/home/user/
```

### Step 3: Deploy with Docker Compose

```bash
# SSH into server
ssh user@your-server-ip

# Navigate to directory
cd /home/user/yliveticker

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

## Customizing Ticker Symbols

Edit `yliveticker/client_code.py` before deploying:

```python
ticker_names=[
    "AAPL",      # Apple
    "MSFT",      # Microsoft
    "GOOGL",     # Google
    "TSLA",      # Tesla
    "BTC-USD",   # Bitcoin
    "ETH-USD",   # Ethereum
    "^GSPC",     # S&P 500
    "^DJI",      # Dow Jones
]
```

Then redeploy in Easypanel (it will rebuild automatically if using GitHub).

## Managing Your App

### View Logs

In Easypanel:
1. Go to your app
2. Click **"Logs"** tab
3. See real-time market data

### Restart App

1. Go to your app
2. Click **"Restart"** button

### Stop App

1. Go to your app
2. Click **"Stop"** button

### Update App

If using GitHub:
1. Push changes to your repository
2. In Easypanel, click **"Rebuild"**
3. App will update automatically

## Resource Configuration

### Recommended Settings

In Easypanel app settings:

- **CPU**: 0.25-0.5 cores (sufficient for ticker streaming)
- **Memory**: 128-256 MB (very lightweight)
- **Restart Policy**: Always (to keep connection alive)

### Scaling

This app doesn't need multiple instances since it maintains a persistent websocket connection. Keep it at 1 instance.

## Monitoring

### Check if App is Running

```bash
# Via Easypanel dashboard
# or via SSH:
docker ps | grep yliveticker
```

### View Resource Usage

In Easypanel:
1. Go to your app
2. See CPU and Memory graphs in dashboard

## Troubleshooting

### App Won't Start

1. **Check logs in Easypanel**
   - Look for error messages
   - Common issue: protobuf version conflicts

2. **Verify Dockerfile**
   - Make sure Dockerfile is in repository root
   - Test locally: `docker build -t yliveticker .`

### No Data Received

1. **Check market hours**: Data only flows when markets are open
2. **Verify ticker symbols**: Make sure they're valid Yahoo Finance symbols
3. **Check logs**: Look for connection errors

### Container Keeps Restarting

1. **Check logs** for Python errors
2. **Verify dependencies** in setup.py
3. **Test locally** with docker-compose:
   ```bash
   docker-compose up
   ```

### Build Fails

1. **Ensure all files are committed** to Git
2. **Check .dockerignore** isn't excluding necessary files
3. **Verify setup.py** has correct dependencies

## Testing Locally Before Deployment

Always test locally first:

```bash
# Build the image
docker build -t yliveticker .

# Run it
docker run yliveticker

# Or use docker-compose
docker-compose up
```

You should see market data streaming in the console.

## Cost Considerations

With Easypanel on a VPS:
- **Small VPS** (1 vCPU, 1GB RAM): $5-10/month
  - Can run multiple apps on same VPS
- **Easypanel**: Free (open source)
- **Total**: Much cheaper than cloud platforms!

Recommended VPS providers:
- [Hetzner](https://www.hetzner.com/) - $4.50/month
- [DigitalOcean](https://www.digitalocean.com/) - $6/month
- [Linode](https://www.linode.com/) - $5/month
- [Vultr](https://www.vultr.com/) - $5/month

## Advanced Configuration

### Auto-restart on Failure

Already configured in docker-compose.yml:
```yaml
restart: unless-stopped
```

### Save Data to File

Modify `yliveticker/client_code.py`:

```python
import json
from datetime import datetime

def printRes(ws, res):
    # Save to file
    with open('/app/data/ticker_data.jsonl', 'a') as f:
        f.write(json.dumps(res) + '\n')
    
    # Also print
    print(json.dumps(res, indent=2))
```

Then add volume in Easypanel:
- **Host Path**: `/var/lib/easypanel/projects/YOUR_PROJECT/yliveticker/data`
- **Container Path**: `/app/data`

### Send Data to Database

You can modify the callback to store data in PostgreSQL, MongoDB, etc.:

```python
import psycopg2

def printRes(ws, res):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ticker_data (symbol, price, timestamp) VALUES (%s, %s, %s)",
        (res['id'], res['price'], res['timestamp'])
    )
    conn.commit()
```

### Environment Variables

Add in Easypanel app settings:
- `DATABASE_URL`: Your database connection string
- `TICKER_SYMBOLS`: Comma-separated list of tickers (optional)
- `LOG_LEVEL`: `DEBUG`, `INFO`, `WARNING`, etc.

## Next Steps

1. ✅ Deploy the basic app
2. 📊 Set up data persistence (optional)
3. 📈 Create a dashboard to visualize data
4. 🔔 Add alerts for price changes
5. 🗄️ Store historical data

## Support

- **Easypanel Docs**: https://easypanel.io/docs
- **yliveticker Issues**: https://github.com/yahoofinancelive/yliveticker/issues
- **Docker Help**: https://docs.docker.com/

## Example: Complete Workflow

Here's a complete example from start to finish:

```bash
# 1. Clone or navigate to your project
cd yliveticker

# 2. Test locally
docker build -t yliveticker .
docker run yliveticker
# Ctrl+C to stop

# 3. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 4. In Easypanel:
#    - Create new app
#    - Connect to GitHub repo
#    - Select "Dockerfile" build method
#    - Click Deploy
#    - Wait 2-3 minutes
#    - View logs to see data streaming!

# Done! 🎉
```

## Alternative: Quick Deploy Script

Create `deploy-easypanel.sh`:

```bash
#!/bin/bash

echo "Building Docker image..."
docker build -t yliveticker .

echo "Testing image..."
timeout 10 docker run yliveticker || true

echo "Image ready for Easypanel deployment!"
echo "Push to your registry or deploy from GitHub"
```

Make it executable and run:
```bash
chmod +x deploy-easypanel.sh
./deploy-easypanel.sh
```

