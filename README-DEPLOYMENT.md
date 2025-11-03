# Deployment Options for yliveticker

Quick overview of how to deploy this Yahoo Finance Live Ticker application.

## Recommended: Easypanel 🎯

**Best for**: Self-hosted, cost-effective deployment

- **Cost**: $5-10/month (VPS)
- **Setup Time**: 5 minutes
- **Difficulty**: Easy
- **Guide**: [QUICKSTART.md](QUICKSTART.md) or [EASYPANEL-DEPLOYMENT.md](EASYPANEL-DEPLOYMENT.md)

### Quick Deploy

1. Push to GitHub
2. Create app in Easypanel from your repo
3. Select "Dockerfile" build method
4. Deploy!

---

## Alternative Options

### Local Docker

**Best for**: Testing and development

```bash
# Using Docker directly
docker build -t yliveticker .
docker run yliveticker

# Or using Docker Compose
docker-compose up
```

### VPS with Docker

**Best for**: Maximum control

```bash
# SSH into your VPS
ssh user@your-server

# Clone repository
git clone https://github.com/YOUR_USERNAME/yliveticker.git
cd yliveticker

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

### Cloud Platforms

If you prefer managed cloud services (more expensive):

- **Google Cloud Run**: ~$10-20/month
- **AWS ECS**: ~$15-30/month
- **Azure Container Instances**: ~$10-25/month
- **Railway**: ~$5-15/month
- **Render**: ~$7-21/month

---

## Comparison

| Platform | Cost/Month | Setup Time | Ease | Control |
|----------|-----------|------------|------|---------|
| **Easypanel** | $5-10 | 5 min | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Railway | $5-15 | 3 min | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cloud Run (GCP) | $10-20 | 5 min | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| VPS + Docker | $5-10 | 10 min | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Local | Free | 2 min | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## Files Included

- **`Dockerfile`**: Container configuration
- **`docker-compose.yml`**: Easy local testing
- **`.dockerignore`**: Optimizes Docker builds
- **`QUICKSTART.md`**: 3-step deployment guide
- **`EASYPANEL-DEPLOYMENT.md`**: Detailed Easypanel guide

---

## Getting Started

1. **Read**: [QUICKSTART.md](QUICKSTART.md) (5 minute deploy)
2. **Test locally**: `docker-compose up`
3. **Deploy**: Follow guide for your chosen platform
4. **Monitor**: Check logs to see live market data

---

## Support

- Issues: [GitHub Issues](https://github.com/yahoofinancelive/yliveticker/issues)
- Easypanel: [Documentation](https://easypanel.io/docs)
- Docker: [Docker Docs](https://docs.docker.com/)

---

**Need to customize ticker symbols?** Edit `yliveticker/client_code.py` before deploying!

