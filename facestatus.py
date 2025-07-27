import cv2
import numpy as np

# Screen setup
screen_width, screen_height = 1920, 1080
try:
    import ctypes
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
except:
    print("Using default resolution")

# Initialize detectors
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

# Create fullscreen window
cv2.namedWindow('Attention Status', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Attention Status', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Status box parameters
BOX_SIZE = 400
BOX_POS = (screen_width - BOX_SIZE - 20, 20)
BOX_COLOR = (50, 50, 50)

while True:
    ret, frame = cap.read()
    if not ret:
        # Camera error handling
        blank = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
        cv2.putText(blank, "CAMERA ERROR", (screen_width//4, screen_height//2),
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        cv2.imshow('Attention Status', blank)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue
    
    frame = cv2.resize(frame, (screen_width, screen_height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]  # Only use the first face detected
        
        # Face bounding box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Eye detection region
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        if len(eyes) >= 1:  # At least one eye detected
            attention_status = "Attentive"
            status_color = (0, 255, 0)  # Green
        else:
            attention_status = "Distracted (Eyes not visible)"
            status_color = (0, 0, 255)  # Red
    else:
        attention_status = "Distracted (No face detected)"
        status_color = (0, 0, 255)  # Red

    # Draw status box
    cv2.rectangle(frame, 
                 (BOX_POS[0], BOX_POS[1]),
                 (BOX_POS[0] + BOX_SIZE, BOX_POS[1] + BOX_SIZE),
                 BOX_COLOR, 3)
    
    # Fill box background
    cv2.rectangle(frame,
                 (BOX_POS[0] + 3, BOX_POS[1] + 3),
                 (BOX_POS[0] + BOX_SIZE - 3, BOX_POS[1] + BOX_SIZE - 3),
                 (40, 40, 40), -1)
    
    # Display status information
    cv2.putText(frame, "ATTENTION STATUS",
               (BOX_POS[0] + 20, BOX_POS[1] + 100),
               cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
    
    cv2.putText(frame, attention_status,
               (BOX_POS[0] + 20, BOX_POS[1] + 200),
               cv2.FONT_HERSHEY_SIMPLEX, 1.2, status_color, 3)
    
    # Display frame
    cv2.imshow('Attention Status', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
