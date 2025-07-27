# 🧠 EDU-FOCUS: AI-Based Attention Monitoring System

**Edu-Focus** is an intelligent desktop-based application built with Python and OpenCV that monitors a student's attentiveness using real-time webcam feed. By analyzing facial and eye features, the system determines whether the user is **attentive** or **distracted** during an educational session.

> 📌 No machine learning training required — this uses classic Haarcascade classifiers and Eye Aspect Ratio logic to determine eye closure.

---

## 📸 Demo

![Demo](edufocus.gif) <!-- Optional: You can record and insert a demo GIF here -->

---

## 🚀 Features

- 🎯 Real-time face and eye detection using OpenCV
- 🧠 Eye Aspect Ratio (EAR) calculation for attention estimation
- 📊 On-screen feedback: **"ATTENTIVE"**, **"DISTRACTED"**, **"Warning"**
- 👁️ Fullscreen distraction detection interface
- 🔄 Simple interface using `Tkinter`
- ⚡ Fast and responsive with threading

---

## 🏗️ How It Works

1. The system uses your **webcam** to continuously capture video frames.
2. It detects the **face** and **eyes** using OpenCV's **Haarcascade classifiers**.
3. If eyes are detected, it calculates the **Eye Aspect Ratio (EAR)**:
   - If eyes are **closed or half-closed** for more than 10 seconds, you're labeled as "DISTRACTED".
   - Otherwise, you're considered "ATTENTIVE".
4. If no eyes or face are detected, it also shows "DISTRACTED".

---

## 🖥️ Interface

The interface includes:

- A fullscreen GUI window using `Tkinter`
- A title screen with:
  - ✅ "START MONITORING" button
  - ❌ "STOP SYSTEM" button
- On monitoring, a fullscreen OpenCV window shows:
  - Webcam feed with detection boxes
  - Live attention status (color-coded)

---

## 🧰 Technologies & Libraries Used

| Library | Purpose |
|--------|--------|
| `OpenCV (cv2)` | Video capture and face/eye detection |
| `NumPy` | Numerical calculations |
| `Tkinter` | GUI for user interaction |
| `scipy` | Eye aspect ratio using Euclidean distance |
| `threading` | Smooth UI & video processing |
| `ctypes` | Screen resolution detection |
| `os` | File system interactions |

---

## 📦 Installation

### ✅ Requirements

- Python 3.7+
- Webcam (built-in or external)
- Windows OS (tested on Windows 10/11)

### 📥 Install Dependencies

Open your terminal or command prompt and run:

```bash
pip install opencv-python numpy scipy
### Running the Project
git clone https://github.com/Sabin2806/edu-focus-attention-monitor.git
cd edu-focus-attention-monitor
Run the script:
python edu_focus.py
Click “START MONITORING” to begin detection.

Press Q anytime to stop the detection window.

##💡 Use Cases

👩‍🎓 Online learning attention monitoring

🧑‍🏫 Classroom focus detection

🧠 Self-productivity tool

##📷 Basic computer vision demonstration

⚠️ Known Limitations

Works best under good lighting conditions.

May have issues with people wearing glasses.

Haar cascades are less accurate than deep learning models (but much faster).

Only uses the first detected face.

##📌 Future Enhancements

Integrate with Telegram API to send real-time alerts

Replace Haarcascade with deep learning models (Dlib / Mediapipe)

Add optional alarm sound and audio feedback

Export daily attention reports

⭐️ Support
If you found this useful, give it a ⭐️ on GitHub!

---

### 📌 What You Need to Do:

- Replace **`Sabin Sasidharan`** and **Sabin2806** in the author and clone URL.
- If you're adding back the **alarm sound**, include the `.mp3` file and update relevant sections.
- Add a **GIF demo** if possible, using [ScreenToGif](https://www.screentogif.com/) or similar.

