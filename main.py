from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from video import generate_video, set_source, toggle_detection, detection_enabled
import asyncio
from fastapi import File,UploadFile
import cv2
import base64
import numpy as np
from ultralytics import YOLO

app = FastAPI()
model = YOLO("yolov8n.pt")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

clients = set()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_video(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.post("/set_source")
async def set_video_source(source: dict):
    ok = set_source(source["source"])
    return JSONResponse(content={"status": "ok" if ok else "error"})

@app.post("/toggle_detection")
async def toggle():
    enabled = toggle_detection()
    await notify_clients(enabled)
    return JSONResponse(content={"enabled": enabled})

@app.get("/status")
async def get_status():
    return JSONResponse(content={"enabled": detection_enabled})

@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Giữ kết nối sống
    except WebSocketDisconnect:
        clients.remove(websocket)

async def notify_clients(enabled: bool):
    to_remove = set()
    for client in clients:
        try:
            await client.send_json({"enabled": enabled})
        except:
            to_remove.add(client)
    clients.difference_update(to_remove)
@app.post("/upload_frame")
async def upload_frame(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(frame)[0]
    annotated = results.plot()

    _, jpeg = cv2.imencode(".jpg", annotated)
    b64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")
    return {"result": b64}

