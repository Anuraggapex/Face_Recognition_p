# 🛡️ AI Face Attendance System with Anti-Spoofing

A professional biometric security application that uses deep learning to identify users while verifying they are "live" human beings, preventing photo-based fraud.

## 🌟 Features
* **Anti-Spoofing:** Blocks login attempts using photos or digital screens.
* **Biometric Identity:** Translates facial features into 128-bit digital "signatures."
* **Real-time UI:** Fluid 20ms update loop for the camera feed.
* **Logging:** Automated entry/exit tracking in `log.txt`.

## 🚀 Prerequisites & Installation

To avoid the `ModuleNotFoundError` for `pkg_resources`, follow these steps exactly:

### 1. Environment Setup
```bash
# Install the compatibility bridge for face_recognition_models
python -m pip install setuptools==69.5.1

# Install core libraries
pip install opencv-python pillow

# Install face recognition suite
pip install face-recognition face-recognition-models
