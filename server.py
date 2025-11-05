import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import yliveticker
import uvicorn

app = FastAPI()

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()
event_loop = None

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "yliveticker",
        "websocket_endpoint": "/ws",
        "connected_clients": len(clients)
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "connected_clients": len(clients)}

# Track which tickers we've seen (for console output)
seen_tickers = set()

# Track previous prices for each ticker to calculate percent change
previous_prices = {}

# Quote type mapping for readability
QUOTE_TYPE_MAP = {
    0: "NONE", 5: "ALTSYMBOL", 7: "HEARTBEAT", 8: "EQUITY", 9: "INDEX",
    11: "MUTUALFUND", 12: "MONEYMARKET", 13: "OPTION", 14: "CURRENCY",
    15: "WARRANT", 17: "BOND", 18: "FUTURE", 20: "ETF", 23: "COMMODITY",
    28: "ECNQUOTE", 41: "CRYPTOCURRENCY", 42: "INDICATOR", 1000: "INDUSTRY"
}

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    print(f"[WebSocket] Client connected. Total clients: {len(clients)}")
    try:
        while True:
            # Keep connection alive - receive any messages (can be used for ping/pong)
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)
        print(f"[WebSocket] Client disconnected. Total clients: {len(clients)}")

def on_ticker(ws, msg):
    # Print to console like client_code.py does with OHLC data
    ticker_id = msg.get("id", "UNKNOWN")
    quote_type = msg.get("quoteType", -1)
    price = msg.get("price", 0)
    timestamp = msg.get("timestamp", "N/A")
    quote_type_name = QUOTE_TYPE_MAP.get(quote_type, f"TYPE_{quote_type}")
    
    # Get OHLC data, bid/ask, and volume
    open_price = msg.get("open")
    high_price = msg.get("high")
    low_price = msg.get("low")
    close_price = msg.get("close") or price  # Use current price if close is None
    bid_price = msg.get("bid")
    ask_price = msg.get("ask")
    volume = msg.get("dayVolume")
    
    # Calculate absolute value change from previous close price
    price_change_value = None
    price_change_direction = None
    
    if ticker_id in previous_prices and previous_prices[ticker_id] is not None:
        prev_price = previous_prices[ticker_id]
        if prev_price > 0 and close_price and close_price > 0:
            price_change_value = close_price - prev_price
            price_change_direction = "+" if price_change_value >= 0 else "-"
            # Add to message for frontend
            msg["priceChangeDirection"] = price_change_direction
            msg["priceChange"] = round(price_change_value, 6)
    
    # Update previous price for next calculation
    if close_price and close_price > 0:
        previous_prices[ticker_id] = close_price
    
    # Track seen tickers
    if ticker_id not in seen_tickers:
        seen_tickers.add(ticker_id)
        print(f"\n[+] NEW TICKER SUBSCRIBED: {ticker_id} (Type: {quote_type_name})")
    
    # Build clear OHLC output with labels
    # Note: Volume is only relevant for stocks, commodities, futures, etc.
    # Forex pairs (CURRENCY type) don't have volume, so skip it for those
    ohlc_parts = []
    if open_price is not None:
        ohlc_parts.append(f"Open: {open_price}")
    if high_price is not None:
        ohlc_parts.append(f"High: {high_price}")
    if low_price is not None:
        ohlc_parts.append(f"Low: {low_price}")
    if close_price is not None:
        ohlc_parts.append(f"Close: {close_price}")
    # Add bid and ask prices
    if bid_price is not None:
        ohlc_parts.append(f"Bid: {bid_price}")
    if ask_price is not None:
        ohlc_parts.append(f"Ask: {ask_price}")
    # Add absolute value change from previous close price
    if price_change_value is not None:
        # Format with appropriate precision (up to 6 decimal places, strip trailing zeros)
        change_abs = abs(price_change_value)
        change_str = f"{price_change_direction}{change_abs:.6f}".rstrip('0').rstrip('.')
        ohlc_parts.append(f"Change: {change_str}")
    # Only show volume if it's greater than 0 and not a currency pair
    # Currencies don't have volume in traditional sense
    if volume is not None and volume > 0 and quote_type != 14:  # 14 = CURRENCY
        ohlc_parts.append(f"Volume: {volume}")
    
    # Format the output clearly
    ohlc_str = " | ".join(ohlc_parts) if ohlc_parts else ""
    time_str = f"Time: {timestamp}"
    
    if ohlc_str:
        print(f"[{ticker_id}] {quote_type_name} | {ohlc_str} | {time_str}")
    else:
        print(f"[{ticker_id}] {quote_type_name} | Price: {price} | {time_str}")
    
    # Broadcast the message to all WebSocket clients (with added price change data)
    data = json.dumps(msg)
    if event_loop and clients:
        for client in list(clients):
            asyncio.run_coroutine_threadsafe(client.send_text(data), event_loop)

def start_ticker():
    yliveticker.YLiveTicker(
        on_ticker=on_ticker,
        ticker_names=[
            "EURUSD=X",
            "JPY=X",  # USDJPY
            "GBPUSD=X",
            "CHF=X",  # USDCHF
            "AUDUSD=X",
            "NZDUSD=X",
            "CAD=X",  # USDCAD
            "GBPJPY=X",
            "CHFJPY=X",
            "AUDJPY=X",
            "EURGBP=X",
            "GC=F",  # gold
            "SI=F",  # silver
            "^DJI",  # Dow Jones
            "^NDX",  # Nasdaq
            "^GSPC",  # S&P 500
            "CL=F",  # crude oil
            "^N225",  # Nikkei 225
            "^HSI",  # Hang Seng Index
        ],
        enable_socket_trace=False  # Set to True for debugging websocket raw/decoded messages
    )

if __name__ == "__main__":
    import threading
    
    # Start the ticker in a separate thread
    threading.Thread(target=start_ticker, daemon=True).start()
    
    # Run the FastAPI app with uvicorn and capture the event loop
    async def run_server():
        global event_loop
        event_loop = asyncio.get_running_loop()
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()
    
    asyncio.run(run_server())