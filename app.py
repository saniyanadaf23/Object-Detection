from flask import Flask, render_template, request, Response, send_from_directory, session, flash, redirect
import cv2
import numpy as np
import base64
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from ultralytics import YOLO
from extensions import db
from models import User


app = Flask(__name__)
app.secret_key = "secret_key_123"
app.permanent_session_lifetime = timedelta(days=7)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ------------------- AUTH -------------------




model = YOLO("yolo11s.pt")


UPLOAD_FOLDER = os.path.join(os.getcwd(), "static")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        pw = request.form["password"]

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("User already exists!")
            return redirect("/login")

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(pw)
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created!")
        return redirect("/login")

    # *THIS RENDERS THE SIGNUP FORM*
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pw = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template("login.html", msg="User does not exist!")

        if not check_password_hash(user.password, pw):
            return render_template("login.html", msg="Incorrect password!")

        session["user"] = email
        return redirect("/detect")

    # Render login page on GET request
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out!")
    return redirect("/login")

@app.route("/show_users")
def show_users():
    users = User.query.all()
    return str([(u.id, u.name, u.email) for u in users])



@app.route('/')
def home():
    return render_template('intro.html')


# Detection dashboard (index.html)
@app.route('/detect')
def detect_page():
    if "user" not in session:
        return redirect("/login")
    return render_template('index.html')

# ------------------- IMAGE DETECTION -------------------
@app.route('/detect_image', methods=['POST'])
def detect_image():
    if 'image' not in request.files:
        return render_template('index.html', detection_status="No file uploaded")

    file = request.files['image']
    if file.filename == '':
        return render_template('index.html', detection_status="No file selected")

    # Read image
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Run YOLO model
    results = model(img)

    # Draw detections
    annotated = results[0].plot()
    img = annotated


    # Convert result to base64
    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return render_template('index.html', detected_image=img_base64)

# ------------------- VIDEO DETECTION -------------------
@app.route('/detect_video', methods=['POST'])
def detect_video():
    if 'video' not in request.files:
        return render_template('index.html', detection_status="No video uploaded")

    file = request.files['video']
    if file.filename == '':
        return render_template('index.html', detection_status="No file selected")

    # Save input
    uploaded_path = os.path.join(UPLOAD_FOLDER, "input.mp4")
    file.save(uploaded_path)

    # Output path (ensure MP4)
    output_path = os.path.join(UPLOAD_FOLDER, "processed.mp4")

    cap = cv2.VideoCapture(uploaded_path)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:
        fps = 24
    width = int(cap.get(3))
    height = int(cap.get(4))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        frame = results[0].plot()
        out.write(frame)

    cap.release()
    out.release()

    return render_template("index.html",
                           detected_video="processed.mp4",
                           detection_status="Completed")


# ------------------- WEBCAM STREAM -------------------
# ------------------- WEBCAM STREAM -------------------
def generate_frames():
    cap = cv2.VideoCapture(0)
    frame_count = 0  # 👈 added

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_count += 1

        # 👉 Process only every 2nd frame (reduces lag)
        if frame_count % 2 != 0:
            continue

        # 👉 Resize frame to reduce computation
        frame = cv2.resize(frame, (640, 480))

        # 👉 Run YOLO
        results = model(frame)
        frame = results[0].plot()

        # Encode and stream
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
