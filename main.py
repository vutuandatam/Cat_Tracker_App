from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from video import generate_video, set_source
import asyncio
import cv2
import base64
import numpy as np
from ultralytics import YOLO

app = FastAPI()
model = YOLO("yolov8n.pt")
detection_enabled = True  # Global flag
clients = set()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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
async def toggle_detection_api():
    global detection_enabled
    detection_enabled = not detection_enabled
    await notify_clients(detection_enabled)
    return {"enabled": detection_enabled}


@app.get("/status")
async def get_status():
    return {"enabled": detection_enabled}


@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
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

    if detection_enabled:
        results = model(frame)[0]
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                if label not in ["cat", "person"]:
                    continue
                conf = box.conf[0]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    _, jpeg = cv2.imencode(".jpg", frame)
    b64 = base64.b64encode(jpeg.tobytes()).decode("utf-8")
    return {"result": b64}

from fastapi.responses import FileResponse

@app.get("/manifest.json")
async def manifest():
    return FileResponse("static/manifest.json")
