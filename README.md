# 🐱 Cat Tracker Web App

A lightweight, real-time cat (and person) detection web app using **FastAPI**, **YOLOv8**, and **WebRTC webcam stream** directly from your browser.

---

## 🚀 Features

- 📸 Capture frames from browser webcam (no OpenCV camera needed)
- 🧠 Use **YOLOv8** to detect cats and people in real time
- 🔁 Toggle detection on/off with UI
- ⚡ Powered by **FastAPI** and **Ultralytics YOLOv8**
- ☁️ Deployable to cloud platforms like [Render.com](https://render.com)

---

## 📦 Requirements

- Python 3.8+
- `ultralytics`
- `fastapi`
- `uvicorn`
- `opencv-python`
- `jinja2`

Install dependencies with:

pip install -r requirements.txt

## 🛠️ Project Structure

.
├── main.py # FastAPI server
├── video.py # Frame generator (optional if using webcam only)
├── templates/
│ └── index.html # Frontend interface
├── static/ # (Optional) Static files (e.g. CSS, JS)
├── README.md # This file
└── yolov8n.pt # YOLOv8 model file (downloaded automatically if missing)

---

## 🖥️ Run Locally

```bash
uvicorn main:app --reload
Visit: http://localhost:8000

Make sure your browser allows webcam access.

🌐 Deploy to Render.com
Push this project to a GitHub repository

Go to https://render.com

Create a new Web Service

Set the start command to:

uvicorn main:app --host 0.0.0.0 --port 10000
Make sure to set the correct Python version and install from requirements.txt

Done 🎉

📸 How It Works
Browser captures webcam video

Sends 1 frame per second to server (/upload_frame)

Server runs YOLOv8 on the image

Server returns annotated image (base64-encoded)

Browser displays the result

🔁 You can toggle detection to pause/resume YOLO processing via the toggle button.