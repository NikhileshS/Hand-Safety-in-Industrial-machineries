import cv2
import mediapipe as mp
import math
import winsound
import numpy as np
import logging
import os

# define log_path location (You can add your own log path for your log file)
log_path = 'E:/hand_detection_logs/hand_detection.log'

# Check if the log file exists, and if so, delete it to start fresh
if os.path.exists(log_path):
    os.remove(log_path)

# Configure logging
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Safety circle parameters (adjust as needed)
safety_circle_center = (320, 170)  # (x, y) coordinates of the circle center
safety_circle_radius = 10  # Radius of the safety circle

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
hands_model = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.4, min_tracking_confidence=0.5)

# Calibration mode and parameters
calibration_mode = False
new_boundary_center = None
new_boundary_radius = None

# Mouse event callback function
def mouse_callback(event, x, y, flags, param):
    global calibration_mode, new_boundary_center, new_boundary_radius, safety_circle_center, safety_circle_radius

    if event == cv2.EVENT_LBUTTONDOWN:
        # Left mouse button click sets the new boundary center
        new_boundary_center = (x, y)
        logging.info("New boundary center set to (%d, %d)", x, y)
    elif event == cv2.EVENT_MOUSEMOVE and calibration_mode:
        # If in calibration mode, calculate the new boundary radius while dragging
        if new_boundary_center is not None:
            new_boundary_radius = int(math.dist((x, y), new_boundary_center))
            logging.info("New boundary radius set to %d", new_boundary_radius)
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Right mouse button click toggles calibration mode
        calibration_mode = not calibration_mode
        if not calibration_mode:
            # Exit calibration mode, update safety boundary
            if new_boundary_center is not None:
                safety_circle_center = new_boundary_center
                logging.info("Safety circle center updated to (%d, %d)", new_boundary_center[0], new_boundary_center[1])
            if new_boundary_radius is not None:
                safety_circle_radius = new_boundary_radius
                logging.info("Safety circle radius updated to %d", new_boundary_radius)

# Create a window and set the mouse callback function
cv2.namedWindow("Real-time Hand Detection")
cv2.setMouseCallback("Real-time Hand Detection", mouse_callback)

def detect_hands(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_model.process(image_rgb)
    
    if results.multi_hand_landmarks:
        return [[(int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
                 for landmark in hand_landmarks.landmark]
                for hand_landmarks in results.multi_hand_landmarks]
    else:
        return []  # Return an empty list if no hands are detected

def draw_hand_boxes(image, hands):
    for box in hands:
        box = np.array(box)  # Convert the box to a numpy array
        x_min, y_min, x_max, y_max = np.min(box[:, 0]), np.min(box[:, 1]), np.max(box[:, 0]), np.max(box[:, 1])
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 4)

def draw_safety_circle(image, center, radius):
    cv2.circle(image, center, radius, (0, 0, 255), 2)

def is_hand_touching_circle(box, circle_center, circle_radius):
    for x, y in box:
        if math.dist((x, y), circle_center) <= circle_radius:
            return True
    x_min, y_min, x_max, y_max = np.min(box[:, 0]), np.min(box[:, 1]), np.max(box[:, 0]), np.max(box[:, 1])
    if (x_min <= circle_center[0] <= x_max) and (abs(circle_center[1] - y_min) <= circle_radius or abs(circle_center[1] - y_max) <= circle_radius):
        return True
    if (y_min <= circle_center[1] <= y_max) and (abs(circle_center[0] - x_min) <= circle_radius or abs(circle_center[0] - x_max) <= circle_radius):
        return True
    return False

cap = cv2.VideoCapture(0)
hand_touching_circle, beep_playing = False, False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    overlay = np.zeros_like(frame)
    overlay[:] = (0, 0, 255)

    hands = detect_hands(frame)
    draw_hand_boxes(frame, hands)

    # Calibration mode logic
    if calibration_mode:
        if new_boundary_center is not None:
            cv2.circle(frame, new_boundary_center, new_boundary_radius, (0, 255, 255), 2)
        cv2.putText(frame, "Calibration mode", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    else:
        draw_safety_circle(frame, safety_circle_center, safety_circle_radius)

    hand_touching_circle_new = any(is_hand_touching_circle(np.array(hand), safety_circle_center, safety_circle_radius) for hand in hands)

    if hand_touching_circle_new and not hand_touching_circle and not beep_playing:
        winsound.Beep(1500, 50)
        beep_playing = True
        logging.warning("Safety breach detected!")
    elif not hand_touching_circle_new and hand_touching_circle and beep_playing:
        beep_playing = False
    hand_touching_circle = hand_touching_circle_new

    if hand_touching_circle:
        cv2.putText(frame, "Safety breach!", (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)

    cv2.imshow("Real-time Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
dd