import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
import pyautogui
import tkinter as tk
import threading
import screen_brightness_control as sbc
from PIL import Image, ImageTk
import json
import os
import custom_gestures
##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 10
no_hand_threshold = 10
#########################
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
running = False
# Initialize the root for tkinter
root = None
# Initialize capture device
cap = None
detector = None
wScr, hScr = autopy.screen.size()
# File to store custom gestures
gestures_file = "gestures.json"
# Load gestures from the JSON file
def load_gestures():
    return custom_gestures.load_gestures()
# Save gestures to the JSON file
def save_gesture(filename, landmarks, action):
    custom_gestures.save_gesture(filename, landmarks, action)
# Custom Gesture Handling
def apply_custom_gesture(lmList):
    return custom_gestures.apply_custom_gesture(lmList)
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')
def track_mouse():
    global pTime, plocX, plocY, clocX, clocY, running, cap, no_hand_start_time, detector
    no_hand_start_time = None
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = htm.handDetector(maxHands=1)
    running = True
    while running:
        success, img = cap.read()
        if not success:
            break
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            no_hand_start_time = None
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
            if fingers == [0, 1, 0, 0, 0]:
                x3 = np.interp(x1, (0, wCam), (0, hScr))
                y3 = np.interp(y1, (0, hCam), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                autopy.mouse.move(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
            elif fingers == [0, 1, 1, 0, 0]:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if length < 35:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()
            elif fingers == [0, 1, 1, 1, 0]:
                pyautogui.scroll(60)
            elif fingers == [0, 1, 1, 1, 1]:
                pyautogui.scroll(-60)
            elif fingers == [1, 0, 0, 0, 0]:
                autopy.mouse.click(autopy.mouse.Button.RIGHT)
            elif fingers == [1, 1, 0, 0, 0]:
                length, img, lineInfo = detector.findDistance(4, 8, img)
                if length < 50:
                    initial_x = x1
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 255), cv2.FILLED)
                    while True:
                        success, img = cap.read()
                        if not success:
                            break
                        img = detector.findHands(img)
                        lmList, bbox = detector.findPosition(img)
                        fingers = detector.fingersUp()
                        if fingers != [1, 1, 0, 0, 0]:
                            break
                        x1, _ = lmList[8][1:]
                        delta_x = x1 - initial_x
                        brightness = np.interp(delta_x, [-wCam // 2, wCam // 2], [0, 100])
                        sbc.set_brightness(brightness)
                        cv2.putText(img, f'Brightness: {int(brightness)}%', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                                    (255, 255, 255), 3)
                        cv2.imshow("Image", img)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
            else:
                if apply_custom_gesture(lmList):
                    print("Custom gesture applied")
        else:
            if no_hand_start_time is None:
                no_hand_start_time = time.time()
            elif time.time() - no_hand_start_time > no_hand_threshold:
                running = False
                print("No hand detected for a while (10 seconds). Stopped tracking.")
                break
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    root.deiconify()
    print("Tracking stopped.")
def customize_gesture():
    customize_gesture_window()
    root.withdraw()
def customize_gesture_window():
    customize_window = tk.Toplevel(root)
    customize_window.title("Customization - Gesture")
    window_width, window_height = 500, 400
    center_window(customize_window, window_width, window_height)
    customize_window.configure(bg='#87CEEB')
    label = tk.Label(customize_window, text="CUSTOMIZATION - GESTURE", bg='#87CEEB', font=('Helvetica', 16, 'bold'))
    label.pack(pady=20)
    gesture_icon = tk.Label(customize_window, text="\u21E7", font=('Helvetica', 48), bg='#87CEEB')
    gesture_icon.pack(pady=10)
    button_customize = tk.Button(customize_window, text="CUSTOMIZE YOUR GESTURES", padx=10, pady=5, fg="white",
                                 bg="#4682B4", command=customize_gesture_interface)
    button_customize.pack(pady=10)
    button_exit = tk.Button(customize_window, text="EXIT", padx=10, pady=5, fg="white", bg="#4682B4",
                            command=lambda: [customize_window.destroy(), root.deiconify()])
    button_exit.pack(pady=10)
def customize_gesture_interface():
    gesture_window = tk.Toplevel(root)
    gesture_window.title("Customize gestures")
    window_width, window_height = 990, 480
    center_window(gesture_window, window_width, window_height)
    gesture_window.configure(bg='white')
    camera_frame = tk.Frame(gesture_window, width=320, height=480, bg='white')
    camera_frame.pack(side="left", fill="both", expand=True)
    button_frame = tk.Frame(gesture_window, width=320, height=480, bg='white')
    button_frame.pack(side="right", fill="both", expand=True)
    label = tk.Label(button_frame, text="Customize gestures", bg='white', font=('Helvetica', 16, 'bold'), fg="blue")
    label.pack(pady=20)
    captured_gesture_label = tk.Label(button_frame, text="", bg='white', font=('Helvetica', 14), fg="green")
    captured_gesture_label.pack(pady=20)
    capture_button = tk.Button(button_frame, text="Capture", padx=10, pady=5, fg="white", bg="blue",
                               command=lambda: capture_gesture(captured_gesture_label))
    capture_button.pack(pady=10)
    button_exit = tk.Button(button_frame, text="EXIT", padx=10, pady=5, fg="white", bg="#4682B4",
                            command=lambda: gesture_window.destroy())
    button_exit.pack(pady=10)
    threading.Thread(target=start_camera_feed, args=(camera_frame, captured_gesture_label)).start()
def start_camera_feed(camera_frame, captured_gesture_label):
    global cap, detector, running
    cap = cv2.VideoCapture(0)
    detector = htm.handDetector(maxHands=1)
    camera_feed_label = tk.Label(camera_frame)
    camera_feed_label.pack()
    running = True
    while running:
        success, img = cap.read()
        if not success:
            break
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.flip(img_rgb, 1)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        camera_feed_label.config(image=img_tk)
        camera_feed_label.image = img_tk
        if not running:
            break
        time.sleep(0.03)
    cap.release()
def capture_gesture(captured_gesture_label):
    global cap, detector
    if cap is None or not cap.isOpened():
        return
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if lmList:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"captured_gesture_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(lmList, f)
            show_action_selection_gui(lmList, filename)
            captured_gesture_label.config(text=f"Gesture landmarks saved as {filename}")
        else:
            captured_gesture_label.config(text="No hand landmarks detected.")
def show_action_selection_gui(landmarks, filename):
    action_window = tk.Toplevel(root)
    action_window.title("Select Mouse Action")
    window_width, window_height = 500, 400
    center_window(action_window, window_width, window_height)
    action_window.configure(bg='#87CEEB')
    label = tk.Label(action_window, text="Select Mouse Action for Gesture", bg='#87CEEB', font=('Helvetica', 16, 'bold'))
    label.pack(pady=20)
    def save_action(action):
        save_gesture(filename, landmarks, action)
        print(f"Gesture for {action} saved with landmarks: {landmarks}")
        action_window.destroy()
        root.deiconify()
    actions = ["Mouse", "Click", "Right Click", "Scroll Up", "Scroll Down"]
    for action in actions:
        button = tk.Button(action_window, text=action, padx=10, pady=5, fg="white", bg="#4682B4", command=lambda a=action: save_action(a))
        button.pack(pady=10)
def exit_application():
    global running
    running = False
    if cap:
        cap.release()
    cv2.destroyAllWindows()
    root.quit()
def show_gui():
    global root
    root = tk.Tk()
    root.title("Virtual Mouse Gesture Controller")
    window_width, window_height = 480, 300
    center_window(root, window_width, window_height)
    canvas = tk.Canvas(root, height=window_height, width=window_width, bg='#87CEEB')
    canvas.pack()
    frame = tk.Frame(root, bg='#87CEEB')
    frame.place(relwidth=1, relheight=1)
    label = tk.Label(frame, text="Virtual Mouse Gesture Controller", bg='#87CEEB', font=('Helvetica', 16, 'bold'))
    label.pack(pady=20)
    button_track = tk.Button(frame, text="TRACK MOUSE", padx=10, pady=5, fg="white", bg="#4682B4",
                             command=lambda: [root.withdraw(), threading.Thread(target=track_mouse).start()])
    button_track.pack(pady=10)
    button_customize = tk.Button(frame, text="CUSTOMIZE GESTURE", padx=10, pady=5, fg="white", bg="#4682B4",
                                 command=customize_gesture)
    button_customize.pack(pady=10)
    button_exit = tk.Button(frame, text="EXIT", padx=10, pady=5, fg="white", bg="#4682B4", command=exit_application)
    button_exit.pack(pady=10)
    root.protocol("WM_DELETE_WINDOW", exit_application)
    root.mainloop()
if __name__ == "__main__":
    show_gui()
