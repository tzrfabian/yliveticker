# Quick Start: Deploy to Easypanel

The fastest way to deploy yliveticker to Easypanel in 3 steps.

## Prerequisites

- Easypanel installed on your VPS ([Get Easypanel](https://easypanel.io/))
- Your code in a Git repository (GitHub, GitLab, etc.)

## 3-Step Deployment

### 1. Push to GitHub

```bash
git add .
git commit -m "Ready for Easypanel"
git push origin main
```

### 2. Create App in Easypanel

1. Login to Easypanel dashboard
2. Click **"Create"** → **"App"**
3. Enter name: `yliveticker`
4. Choose **"Build from Source"**
5. Enter your GitHub repository URL
6. Select **"Dockerfile"** as build method
7. Click **"Create"**

### 3. Deploy

Click **"Deploy"** and wait 2-3 minutes.

## View Live Data

1. Go to your app in Easypanel
2. Click **"Logs"** tab
3. Watch real-time market data stream! 📈

```
[EURUSD=X] CURRENCY | Price: 1.0621 | Time: 2025-11-03 14:23:45
[GC=F] FUTURE | Price: 2738.50 | Time: 2025-11-03 14:23:46
[^GSPC] INDEX | Price: 5728.80 | Time: 2025-11-03 14:23:47
```

## Customize Tickers

Before deploying, edit `yliveticker/client_code.py`:

```python
ticker_names=[
    "AAPL",      # Apple
    "TSLA",      # Tesla
    "BTC-USD",   # Bitcoin
    "^GSPC",     # S&P 500
]
```

## Test Locally First

```bash
docker build -t yliveticker .
docker run yliveticker
```

Press Ctrl+C to stop.

## Cost

- **VPS** (1GB RAM): $5-10/month (Hetzner, DigitalOcean, etc.)
- **Easypanel**: Free (open source)
- **Total**: Much cheaper than cloud platforms!

## Need Help?

See [EASYPANEL-DEPLOYMENT.md](EASYPANEL-DEPLOYMENT.md) for:
- Detailed deployment methods
- Troubleshooting
- Advanced configuration
- Docker Compose setup
- Data persistence

## What's Next?

✅ App is running  
📊 Add database to store historical data  
📈 Create a dashboard  
🔔 Set up price alerts  

---

**Pro Tip**: Markets only send data during trading hours. If you see no data, check if the market is open!

