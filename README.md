+-------------------------+     +-------------------------+
|      Mobile App         | <--> |   Home Tracking Server  |
|  - Live cam view        |      |  - USB/IP camera input  |
|  - Alert list           |      |  - Motion tracking (CV) |
|  - View saved clips     |      |  - REST API + Video API |
+-------------------------+     +-------------------------+
                                      
                              +---------------+
                              | Local Storage |
                              +---------------+
Technologies That Work Well
Task	Tools
Video stream (home)	OpenCV + MJPEG server, WebRTC, or RTSP
REST API (alerts)	Node.js/Express or Python/Flask
Mobile app	Flutter or React Native
Push alerts	Firebase Cloud Messaging
Optional auth	JWT, token-based API access
Deployment	Run on home PC or Raspberry Pi 24/7

Cat_Tracker_App/
│
├── main.py              # FastAPI server chính
├── video.py             # Xử lý stream + YOLO
├── templates/
│   └── index.html       # HTML UI
└── static/
    └── script.js        # (tùy chọn) JS riêng