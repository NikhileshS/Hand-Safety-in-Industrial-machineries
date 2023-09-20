import cv2
import mediapipe as mp
import math
import winsound
import numpy as np

# Safety circle parameters (adjust as needed)
safety_circle_center = (320, 170)  # (x, y) coordinates of the circle center
safety_circle_radius = 10  # Radius of the safety circle

def detect_hands(frame, mp_hands):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(image_rgb)
    return [[(int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]))
             for landmark in hand_landmarks.landmark]
            for hand_landmarks in results.multi_hand_landmarks]

def draw_hand_boxes(image, hands):
    for box in hands:
        x_min, y_min, x_max, y_max = np.min(box[:, 0]), np.min(box[:, 1]), np.max(box[:, 0]), np.max(box[:, 1])
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 4)

def draw_safety_circle(image):
    cv2.circle(image, safety_circle_center, safety_circle_radius, (0, 0, 255), 2)

def is_hand_touching_circle(box):
    circle_center_x, circle_center_y = safety_circle_center
    circle_radius = safety_circle_radius
    for x, y in box:
        if math.dist((x, y), (circle_center_x, circle_center_y)) <= circle_radius:
            return True
    x_min, y_min, x_max, y_max = np.min(box[:, 0]), np.min(box[:, 1]), np.max(box[:, 0]), np.max(box[:, 1])
    if (x_min <= circle_center_x <= x_max) and (abs(circle_center_y - y_min) <= circle_radius or abs(circle_center_y - y_max) <= circle_radius):
        return True
    if (y_min <= circle_center_y <= y_max) and (abs(circle_center_x - x_min) <= circle_radius or abs(circle_center_x - x_max) <= circle_radius):
        return True
    return False

mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.4)

cap = cv2.VideoCapture(0)
hand_touching_circle, beep_playing = False, False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    overlay = np.zeros_like(frame)
    overlay[:] = (0, 0, 255)

    hands = detect_hands(frame, mp_hands)
    draw_hand_boxes(frame, hands)
    draw_safety_circle(frame)

    hand_touching_circle_new = any(is_hand_touching_circle(np.array(hand)) for hand in hands)

    if hand_touching_circle_new and not hand_touching_circle and not beep_playing:
        winsound.Beep(1500, 50)
        beep_playing = True
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