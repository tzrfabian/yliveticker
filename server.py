import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import yliveticker
import uvicorn

app = FastAPI()
clients = set()
event_loop = None

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
    if event_loop and clients:
        for client in list(clients):
            asyncio.run_coroutine_threadsafe(client.send_text(data), event_loop)

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