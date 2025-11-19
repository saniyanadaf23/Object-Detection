<p align="center">
  <img src="https://img.shields.io/badge/YOLOVision%20Pro-Real--Time%20Object%20Detection-blueviolet?style=for-the-badge" />
</p>

<h1 align="center">YOLOVision Pro — Real-Time Object Detection (YOLO11)</h1>

<p align="center">
A full-stack computer vision application that supports <b>image detection, video analysis, and live webcam inference</b> using YOLO11.  
Beautiful UI + Authentication + Real-time Object Tracking.
</p>

---

## 🔥 Features

| Feature | Description |
|---------|------------|
| 🖼 Upload Image | Detect objects on a single frame |
| 🎞 Upload Video | Processes video frame-by-frame & returns annotated output |
| 🎥 Live Webcam | Real-time streaming with bounding box overlays |
| 🔑 User Authentication | Signup + Login (SQLAlchemy + hashed passwords) |
| 🧠 YOLO11 Integration | Fast and accurate object detection via Ultralytics |
| 🎨 Modern UI | Neumorphism + Gradient + Responsive design |

---

## 🛠 Tech Stack

| Layer | Tools |
|-------|-------|
| **Frontend** | HTML, CSS, Bootstrap, JS |
| **Backend** | Flask (Python) |
| **Model** | YOLO11 – Ultralytics |
| **Database** | SQLite + SQLAlchemy |
| **Video Processing** | OpenCV |

---

## 📎 Project Structure

📂 YOLOVision-Pro
│── app.py
│── models.py
│── extensions.py
│── requirements.txt
│── /static
│ ├── processed.mp4
│ ├── uploads/
│── /templates
│ ├── index.html
│ ├── login.html
│ ├── signup.html
│ ├── intro.html
└── /database
└── users.db


---

## 🚀 Installation Guide

### **1️⃣ Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/YOLOVision-Pro.git
cd YOLOVision-Pro
python -m venv venv
source venv/Scripts/activate   # Windows
pip install -r requirements.txt
yolo11m.pt
python app.py
