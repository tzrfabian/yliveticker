# Live Price from Yahoo Finance

Get market data from Yahoo Finance websocket in near-real time.
wss://streamer.finance.yahoo.com/

## Features

- ✅ Real-time market data streaming (currencies, commodities, indices, stocks)
- ✅ OHLC data (Open, High, Low, Close) with proper decimal formatting
- ✅ Price change tracking (plus/minus from previous close)
- ✅ WebSocket server for frontend integration
- ✅ CORS enabled for cross-origin requests
- ✅ Health check endpoints
- ✅ Docker deployment ready

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

## WebSocket Server for Frontend Integration

Run the WebSocket server to stream data to your frontend:

```bash
python server.py
```

The server will:
- Start on `http://localhost:8000`
- WebSocket endpoint: `ws://localhost:8000/ws`
- Stream real-time market data with OHLC formatting
- Track price changes from previous close (plus/minus)

### Frontend Connection Example

```javascript
// Connect to WebSocket server
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Data includes: id, price, open, high, low, close, 
  // priceChange, priceChangeDirection, timestamp, etc.
  console.log(`[${data.id}] Close: ${data.close}, Change: ${data.priceChangeDirection}${data.priceChange}`);
};
```

### Data Format

Each message includes:
- `id` - Ticker symbol (e.g., "EURUSD=X")
- `price` - Current price
- `open`, `high`, `low`, `close` - OHLC data
- `priceChange` - Absolute value change from previous close
- `priceChangeDirection` - "+" or "-"
- `timestamp` - Formatted timestamp
- `dayVolume` - Volume (for stocks/commodities)
- `quoteType` - Asset type

### Decimal Formatting

Prices are automatically formatted:
- **5 decimals**: USD, GBP, CHF, CAD currency pairs (e.g., EURUSD=X)
- **3 decimals**: JPY currency pairs (e.g., USDJPY=X)
- **2 decimals**: Commodities, indices (e.g., GC=F, ^GSPC)
- **Raw**: Stocks, ETFs (e.g., AAPL)

See **[FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)** for detailed frontend integration guide.

## Deployment

Want to run this 24/7 in the cloud? Check out our deployment guides:

### 🚀 Quick Deploy to Easypanel (Recommended)
Deploy to your own VPS with Easypanel in just 5 minutes - only $5-10/month!

**[→ Quick Start Guide (QUICKSTART.md)](QUICKSTART.md)**

3 simple steps:
1. Push to GitHub
2. Create app in Easypanel
3. Deploy!

The server will be available at:
- **WebSocket**: `wss://your-domain.com/ws`
- **Health Check**: `https://your-domain.com/health`

See detailed guide: **[EASYPANEL-DEPLOYMENT.md](EASYPANEL-DEPLOYMENT.md)**

### 🐳 Run with Docker

```bash
# Build and run
docker build -t yliveticker .
docker run -p 8000:8000 yliveticker

# Or use Docker Compose
docker-compose up
```

The WebSocket server will be available at `ws://localhost:8000/ws`

See all deployment options: **[README-DEPLOYMENT.md](README-DEPLOYMENT.md)**

## Notes

- The connection runs continuously until you stop it (Ctrl+C)
- Data will only appear during trading hours for each market
- The `on_ticker` callback receives a dictionary with fields like:
  - `id`, `price`, `open`, `high`, `low`, `close`
  - `priceChange`, `priceChangeDirection` (from previous close)
  - `timestamp`, `dayVolume`, `quoteType`, etc.
- OHLC data is cached and tracked from streaming prices
- *Check trading hours for your market if you don't observe any live metrics*

## Available Tickers

The server streams these tickers by default:
- **Currency pairs**: EURUSD=X, GBPUSD=X, JPY=X, CHF=X, AUDUSD=X, etc.
- **Commodities**: GC=F (gold), SI=F (silver), CL=F (crude oil)
- **Indices**: ^DJI (Dow Jones), ^NDX (Nasdaq), ^GSPC (S&P 500), ^N225 (Nikkei), ^HSI (Hang Seng)

You can customize the ticker list in `server.py`.