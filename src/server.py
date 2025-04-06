#server.py 
import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import threading
import queue
import speech_recognition as sr
import totta  # Import backend script

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Queue for handling messages from the backend
message_queue = queue.Queue()

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected")

    def backend_worker():
        while True:
            msg = message_queue.get()
            if msg is None:
                break
            asyncio.run_coroutine_threadsafe(
                websocket.send_text(json.dumps(msg)), asyncio.get_event_loop()
            )
    
    threading.Thread(target=backend_worker, daemon=True).start()
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from frontend: {data}")
            
            # Send message to AI backend
            totta.process_input(data, message_queue)  # Process and queue response

    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        print("WebSocket closed")
