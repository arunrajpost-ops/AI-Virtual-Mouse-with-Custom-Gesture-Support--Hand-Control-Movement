# 🖱️ AI-Virtual-Mouse-with-Custom-Gesture-Support--Hand-Control-Movement

## 📌 Introduction
AI-Virtual-Mouse-with-Custom-Gesture-Support is a computer vision based project that allows users to control their computer mouse using hand gestures instead of a physical mouse.

The system uses a webcam to capture hand movements and applies real-time hand tracking to detect gestures. These gestures are then mapped to different mouse operations such as cursor movement, clicking, and scrolling.

The goal of this project is to demonstrate how Artificial Intelligence and Computer Vision can be used to create touchless human-computer interaction systems.

---

## 🛠️ Technologies Used

### 🐍 Programming Language
Python

### 📷 Computer Vision
OpenCV

### ✋ Hand Tracking
MediaPipe

### 🖱️ Mouse Control
PyAutoGUI

### 🔢 Numerical Computation
NumPy

### 🧪 Development Environment
Python
Jupyter Notebook / VS Code

---

## ✨ Key Features

🖐️ Real-time hand gesture detection using webcam  
🖱️ Control mouse cursor using index finger movement  
👆 Perform left click using finger gestures  
👉 Perform right click using specific gesture combinations  
🔽 Scroll functionality using multiple fingers  
⚡ Smooth and responsive cursor control  
🧠 AI-based hand landmark detection using MediaPipe  
💻 Touchless computer interaction  

---

## 📊 Gesture Controls

| Gesture | Action |
|------|------|
| Index Finger Up | Cursor Movement |
| Index + Thumb Close | Left Click |
| Two Fingers Up | Right Click |
| Three Fingers Up | Scroll |
| Open Palm | Pause / Idle Mode |

---

## ⚙️ How It Works

1. The webcam captures real-time video of the user’s hand.
2. MediaPipe detects hand landmarks and finger positions.
3. Finger coordinates are processed using OpenCV.
4. Specific gestures are recognized based on finger distances.
5. PyAutoGUI converts these gestures into mouse actions.

---

## 📂 Project Structure

```
AI-Virtual-Mouse-with-Custom-Gesture-Support--Hand-Control-Movement
│
├── main.py
├── hand_tracking.py
├── gesture_controller.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Clone the Repository

```
git clone https://github.com/arunrajpost-ops/AI-Virtual-Mouse-with-Custom-Gesture-Support--Hand-Control-Movement.git
```

### Navigate to Project Directory

```
cd AI-Virtual-Mouse-with-Custom-Gesture-Support--Hand-Control-Movement
```

### Install Required Libraries

```
pip install opencv-python mediapipe pyautogui numpy
```

or

```
pip install -r requirements.txt
```

---

## ▶️ Run the Project

```
python main.py
```

Once executed, your webcam will start and detect hand gestures to control the mouse.

---

## 📸 Project Demonstration

### 🖱️ Cursor Movement
Hand gesture controlling mouse movement.

### 👆 Click Gesture
Finger gesture used for left click.

### 🔽 Scroll Gesture
Multi-finger gesture used for scrolling.

---

## 📈 Applications

Accessibility tools for physically challenged users  
Touchless computer interaction  
Smart presentations and demonstrations  
Gesture-based control systems  
Learning project for Computer Vision and AI  

---

## 🚀 Future Improvements

Custom gesture training  
Gesture-based virtual keyboard  
Multi-hand gesture recognition  
Graphical user interface (GUI)  
Integration with voice commands  

---

## 📸 Project Screenshots

### 🖥️ Virtual Mouse Gesture Controller Interface

<p align="center">
  <img src="images/Screenshot 2026-03-08 151807.png" width="900">
</p>

## 📸 Project Working

### 🖱️ AI Virtual Mouse in Action

<p align="center">
  <img src="images/Screenshot 2026-03-08 152721.png" alt="AI Virtual Mouse Working" width="900">
</p>

## 👨‍💻 Author

**Arun Raj**

GitHub  
https://github.com/arunrajpost-ops

LinkedIn  
https://www.linkedin.com/in/arun-raj-80a2a0355/

---

## ⭐ Support

If you like this project, please consider giving it a **Star ⭐ on GitHub**.
