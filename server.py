import asyncio
import json
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