# 🛡️ AI Face Attendance System with Anti-Spoofing

A high-tech, biometric attendance system that uses computer vision to recognize faces while preventing fraud through real-time anti-spoofing detection.

## 🌟 Features
* **Live Face Recognition:** Identifies registered users in milliseconds.
* **Anti-Spoofing:** Detects if a person is real or holding up a photo/screen.
* **Biometric Security:** Converts faces into 128-bit digital signatures (embeddings).
* **Automated Logging:** Records "In" and "Out" timestamps in a local ledger.
* **Modern UI:** Built with Tkinter for a clean, user-friendly experience.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Libraries:** OpenCV, Face_Recognition, TensorFlow, PIL, Tkinter.
* **Models:** Dlib 68-point landmark predictor, Anti-spoofing Mini-Network.

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed, then install the required dependencies:
```bash
pip install opencv-python face-recognition pillow setuptools
