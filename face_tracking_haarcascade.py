import cv2
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
time.sleep(2)  # Wait for Arduino to initialize

# Initialize the camera
cap = cv2.VideoCapture(1)

# Variables to store the previous positions
prev_angleX = 90
prev_angleY = 90
smoothing_factor = 0.2  # Smoothing factor for smoother movement

def send_angles_to_arduino(angleX, angleY):
    arduino.write(f"{angleX},{angleY}\n".encode())

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally to fix mirror view issue
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # If a face is detected
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            centerX = x + w // 2
            centerY = y + h // 2
            frameCenterX = frame.shape[1] // 2
            frameCenterY = frame.shape[0] // 2

            # Calculate new angles with some smoothing
            new_angleX = int(90 + (centerX - frameCenterX) / frameCenterX * 45)
            new_angleY = int(90 - (centerY - frameCenterY) / frameCenterY * 45)

            # Smooth the angle transitions
            angleX = int(prev_angleX + (new_angleX - prev_angleX) * smoothing_factor)
            angleY = int(prev_angleY + (new_angleY - prev_angleY) * smoothing_factor)

            # Send the angles to Arduino
            send_angles_to_arduino(angleX, angleY)

            # Update the previous angles
            prev_angleX = angleX
            prev_angleY = angleY

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        # No face detected, stop the camera movement
        send_angles_to_arduino(prev_angleX, prev_angleY)

    cv2.namedWindow('Live Face cam', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Live Face cam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Live Face cam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
