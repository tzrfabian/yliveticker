# Frontend Integration Guide

## Quick Start

Your backend is ready for frontend integration! Here's how to connect:

## WebSocket Endpoint

**Endpoint:** `ws://localhost:8000/ws` (development)
**Endpoint:** `wss://your-domain.com/ws` (production)

## JavaScript/TypeScript Example

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Connected to yliveticker server');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  // Data structure:
  // {
  //   "id": "EURUSD=X",
  //   "price": 1.06215,
  //   "open": 1.06200,
  //   "high": 1.06250,
  //   "low": 1.06180,
  //   "close": 1.06215,
  //   "timestamp": "2025-11-04 09:24:47",
  //   "changePercent": -0.15,
  //   "dayVolume": 1234567,
  //   "quoteType": 14,
  //   ...
  // }
  
  console.log(`[${data.id}] Price: ${data.price}`);
  
  // Update your UI with the data
  updatePriceDisplay(data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from server');
  // Optionally reconnect after a delay
  setTimeout(() => {
    // Reconnect logic here
  }, 5000);
};

function updatePriceDisplay(data) {
  // Example: Update DOM elements
  const priceElement = document.getElementById(`price-${data.id}`);
  if (priceElement) {
    priceElement.textContent = data.price;
  }
  
  // Update OHLC display
  if (data.open) {
    document.getElementById(`open-${data.id}`).textContent = data.open;
  }
  if (data.high) {
    document.getElementById(`high-${data.id}`).textContent = data.high;
  }
  if (data.low) {
    document.getElementById(`low-${data.id}`).textContent = data.low;
  }
  if (data.close) {
    document.getElementById(`close-${data.id}`).textContent = data.close;
  }
}
```

## React Example

```jsx
import { useEffect, useState } from 'react';

function LiveTicker({ tickerId }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onmessage = (event) => {
      const tickerData = JSON.parse(event.data);
      if (tickerData.id === tickerId) {
        setData(tickerData);
      }
    };

    return () => {
      ws.close();
    };
  }, [tickerId]);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h3>{data.id}</h3>
      <p>Price: {data.price}</p>
      <p>Open: {data.open || 'N/A'}</p>
      <p>High: {data.high || 'N/A'}</p>
      <p>Low: {data.low || 'N/A'}</p>
      <p>Close: {data.close || 'N/A'}</p>
      <p>Change: {data.changePercent}%</p>
    </div>
  );
}
```

## Health Check

You can check if the server is running:

```javascript
fetch('http://localhost:8000/health')
  .then(res => res.json())
  .then(data => console.log(data));
// Returns: { "status": "healthy", "connected_clients": 1 }
```

## Production Setup

1. **Update CORS origins** in `server.py`:
```python
allow_origins=["https://your-frontend-domain.com"]
```

2. **Use WSS (secure WebSocket)** in production:
```javascript
const ws = new WebSocket('wss://your-backend-domain.com/ws');
```

3. **Set up reverse proxy** (Nginx/Traefik) for WebSocket support:
```nginx
location /ws {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

## Data Format

All prices are formatted with appropriate decimal places:
- **5 decimals**: USD, GBP, CHF, CAD currency pairs (e.g., EURUSD=X)
- **3 decimals**: JPY currency pairs (e.g., USDJPY=X)
- **2 decimals**: Commodities, indices (e.g., GC=F, ^GSPC)
- **Raw**: Stocks, ETFs (e.g., AAPL)

## Available Tickers

The server streams these tickers by default:
- Currency pairs: EURUSD=X, GBPUSD=X, JPY=X, etc.
- Commodities: GC=F (gold), SI=F (silver), CL=F (crude oil)
- Indices: ^DJI, ^NDX, ^GSPC, ^N225, ^HSI

