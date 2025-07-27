import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, font, messagebox
import threading
import time
import ctypes
import os
from scipy.spatial import distance as dist

class EduFocusSystem:
    def __init__(self):
        # Get screen resolution
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        
        # Initialize main interface
        self.root = tk.Tk()
        self.root.title("EDU-FOCUS Attention Monitor")
        self.setup_interface()
        
        # Detection variables
        self.detection_active = False
        self.cap = None
        self.current_status = "Ready"
        
        # Eye detection parameters
        self.EYE_AR_THRESH = 0.25  # Eye Aspect Ratio threshold
        self.COUNTER = 0
        self.CONSEC_FRAMES = 3
        
        # Alarm system variables
        self.eyes_closed_start_time = None
        self.ALARM_TRIGGER_TIME = 10  # seconds to trigger alarm

        # Pre-load classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    def setup_interface(self):
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.root.attributes('-fullscreen', True)

        bg_frame = tk.Frame(self.root, bg='#2c3e50')
        bg_frame.place(x=0, y=0, relwidth=1, relheight=1)

        content_frame = tk.Frame(bg_frame, bg='#34495e', bd=0)
        content_frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=500)

        title_font = font.Font(family='Helvetica', size=36, weight='bold', slant='italic')
        title_label = tk.Label(content_frame, text="EDU-FOCUS", font=title_font, fg='white', bg='#34495e')
        title_label.pack(pady=(40, 50))

        button_font = font.Font(family='Helvetica', size=16, weight='bold')

        self.start_btn = tk.Button(content_frame, text="START MONITORING", font=button_font, fg='white',
                                   bg='#27ae60', activeforeground='white', activebackground='#2ecc71',
                                   relief='raised', borderwidth=3, padx=30, pady=15, command=self.start_detection)
        self.start_btn.pack(pady=20)

        self.stop_btn = tk.Button(content_frame, text="STOP SYSTEM", font=button_font, fg='white',
                                  bg='#e74c3c', activeforeground='white', activebackground='#c0392b',
                                  relief='raised', borderwidth=3, padx=30, pady=15, command=self.stop_system)
        self.stop_btn.pack(pady=20)

        self.status_label = tk.Label(content_frame, text="System Ready", font=('Helvetica', 14),
                                     fg='white', bg='#34495e')
        self.status_label.pack(pady=20)

    def eye_aspect_ratio(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        return (A + B) / (2.0 * C)

    def calculate_avg_ear(self, eyes, roi_gray):
        ear_sum = 0
        valid_eyes = 0

        for (ex, ey, ew, eh) in eyes[:2]:
            eye_landmarks = np.array([
                (ex, ey+eh//2), (ex+ew, ey+eh//2),
                (ex+ew//4, ey), (ex+3*ew//4, ey),
                (ex+ew//4, ey+eh), (ex+3*ew//4, ey+eh)
            ])
            ear_sum += self.eye_aspect_ratio(eye_landmarks)
            valid_eyes += 1

        return ear_sum / valid_eyes if valid_eyes > 0 else 0

    def start_detection(self):
        self.root.withdraw()
        self.status_label.config(text="Starting detection...")
        self.detection_active = True
        detection_thread = threading.Thread(target=self.run_detection, daemon=True)
        detection_thread.start()

    def run_detection(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.screen_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.screen_height)

        cv2.namedWindow('Attention Detection', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Attention Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while self.detection_active:
            ret, frame = self.cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(100, 100))

            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                roi_gray = gray[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)

                if len(eyes) >= 2:
                    avg_ear = self.calculate_avg_ear(eyes, roi_gray)

                    if avg_ear < self.EYE_AR_THRESH:
                        self.COUNTER += 1

                        if self.eyes_closed_start_time is None:
                            self.eyes_closed_start_time = time.time()

                        closed_duration = time.time() - self.eyes_closed_start_time

                        if closed_duration >= self.ALARM_TRIGGER_TIME:
                            status = f"DISTRACTED ({int(closed_duration)}s)"
                            color = (0, 0, 255)
                            cv2.putText(frame, "ALARM!", (self.screen_width//2 - 100, 150),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                        else:
                            status = f"Warning ({int(closed_duration)}s)"
                            color = (0, 165, 255)
                    else:
                        self.COUNTER = 0
                        self.eyes_closed_start_time = None
                        status = "ATTENTIVE"
                        color = (0, 255, 0)
                else:
                    status = "Distracted (Eyes not detected)"
                    color = (0, 0, 255)
            else:
                status = "Distracted (No face detected)"
                color = (0, 0, 255)

            cv2.putText(frame, status, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
            cv2.imshow('Attention Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_detection()
                break

        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
        self.root.deiconify()
        self.status_label.config(text="Detection stopped. Ready to start again.")

    def stop_detection(self):
        self.detection_active = False
        self.eyes_closed_start_time = None

    def stop_system(self):
        self.stop_detection()
        self.root.destroy()

if __name__ == "__main__":
    app = EduFocusSystem()
    app.root.mainloop()
