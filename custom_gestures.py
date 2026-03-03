import json
import autopy
import pyautogui
import numpy as np
from scipy.spatial.distance import cosine
gestures_file = "gestures.json"
SIMILARITY_THRESHOLD = 10  # Adjust this value as needed
def load_gestures():
    try:
        with open(gestures_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
def save_gesture(filename, landmarks, action):
    gestures = load_gestures()
    # Remove any existing gestures with the same action
    gestures = {k: v for k, v in gestures.items() if v['action'] != action}
    gestures[filename] = {'landmarks': landmarks, 'action': action}
    with open(gestures_file, 'w') as file:
        json.dump(gestures, file, indent=4)
def normalize_landmarks(landmarks):
    base_x, base_y = landmarks[0][1:]
    return [(id, (x - base_x), (y - base_y)) for id, x, y in landmarks]
def landmarks_match(lmList1, lmList2):
    lmList1 = normalize_landmarks(lmList1)
    lmList2 = normalize_landmarks(lmList2)
    if len(lmList1) != len(lmList2):
        return False
    distances = []
    for lm1, lm2 in zip(lmList1, lmList2):
        distances.append(cosine(lm1[1:], lm2[1:]))
    avg_distance = np.mean(distances)
    return avg_distance < SIMILARITY_THRESHOLD
def apply_custom_gesture(lmList):
    gestures = load_gestures()
    for gesture_name, gesture_data in gestures.items():
        if landmarks_match(lmList, gesture_data['landmarks']):
            action = gesture_data['action']
            if action == "Mouse":
                autopy.mouse.move(autopy.screen.size().width - lmList[0][1], lmList[0][2])
            elif action == "Click":
                autopy.mouse.click()
            elif action == "Right Click":
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
            elif action == "Scroll Up":
                pyautogui.scroll(60)
            elif action == "Scroll Down":
                pyautogui.scroll(-60)
            return True
    return False
