import asyncio
import json
from webbrowser import get
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import yliveticker
import uvicorn

app = FastAPI()
clients = set()

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.remove(ws)

def on_ticker(ws, msg):
    # Broadcast the message to all clients
    data = json.dumps(msg)
    for client in list(clients):
        asyncio.run_coroutine_threadsafe(client.send_text(data), asyncio.get_event_loop())

def start_ticker():
    yliveticker.YLiveTicker(
        on_ticker=on_ticker,
        ticker_names=[
            "EURUSD=X",
            "JPY=X",
            "GBPUSD=X"
        ],
        enable_socket_trace=False # Optional: for debugging
    )

if __name__ == "__main__":
    import threading
    threading.Thread(target=start_ticker, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)