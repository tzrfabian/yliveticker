# Live Price from Yahoo Finance

Get market data from Yahoo Finance websocket in near-real time.
wss://streamer.finance.yahoo.com/

## Setup
```bash
pip install yliveticker
```
[pypi package home](https://pypi.org/project/yliveticker/)

## Example

The following snippet prints out live metrics in console output. You can follow other symbols by providing them in `ticker_names`.

```python
import yliveticker


# this function is called on each ticker update
def on_new_msg(ws, msg):
    print(msg)


yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=[
    "BTC=X", "^GSPC", "^DJI", "^IXIC", "^RUT", "CL=F", "GC=F", "SI=F", "EURUSD=X", "^TNX", "^VIX", "GBPUSD=X", "JPY=X", "BTC-USD", "^CMC200", "^FTSE", "^N225"])
```

### Fix Protobuf Version Issue

The generated protobuf code is incompatible with protobuf 3.21+. You need to downgrade to a compatible version:

```powershell
python -m pip install --upgrade "protobuf>=3.11.0,<3.21"
```

Or run the batch file:
```powershell
.\fix_protobuf_version.bat
```

### Run the Example

After fixing the protobuf version, run the example:

```powershell
python yliveticker/client_code.py
```

### Create Your Own Script

Create a new Python file (e.g., `my_ticker.py`):

```python
import yliveticker

def on_new_msg(ws, msg):
    print(msg)

yliveticker.YLiveTicker(
    on_ticker=on_new_msg, 
    ticker_names=["BTC-USD", "AAPL", "MSFT", "^GSPC"]
)
```

Then run:
```powershell
python my_ticker.py
```

## Alternative Solutions

If downgrading protobuf doesn't work, you can:

1. **Regenerate the protobuf file** (requires `protoc` compiler):
   ```powershell
   protoc --python_out=. --proto_path=yliveticker yliveticker/yaticker.proto
   ```

2. **Use environment variable workaround** (slower but works):
   ```powershell
   $env:PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"
   python yliveticker/client_code.py
   ```

## Deployment

Want to run this 24/7 in the cloud? Check out our deployment guides:

### 🚀 Quick Deploy to Easypanel (Recommended)
Deploy to your own VPS with Easypanel in just 5 minutes - only $5-10/month!

**[→ Quick Start Guide (QUICKSTART.md)](QUICKSTART.md)**

3 simple steps:
1. Push to GitHub
2. Create app in Easypanel
3. Deploy!

See detailed guide: **[EASYPANEL-DEPLOYMENT.md](EASYPANEL-DEPLOYMENT.md)**

### 🐳 Run with Docker

```bash
# Build and run
docker build -t yliveticker .
docker run yliveticker

# Or use Docker Compose
docker-compose up
```

See all deployment options: **[README-DEPLOYMENT.md](README-DEPLOYMENT.md)**

## Notes

- The connection runs continuously until you stop it (Ctrl+C)
- Data will only appear during trading hours for each market
- The `on_ticker` callback receives a dictionary with fields like `id`, `price`, `changePercent`, `timestamp`, etc.
- *Check trading hours for your market if you don't observe any live metrics*