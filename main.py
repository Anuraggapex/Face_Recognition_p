import os
import pickle
import tkinter as tk
from datetime import datetime
from typing import Optional, Any

import cv2
import face_recognition
from PIL import Image, ImageTk

# Local imports - Ensure util.py and test.py are in the same folder
import util
from test import test

class App:
    def __init__(self):
        # 1. Initialize Window
        self.main_window = tk.Tk()

        # 2. Pre-declare all attributes (Removes "defined outside __init__" warnings)
        self.cap: Optional[cv2.VideoCapture] = None
        self.most_recent_capture_arr: Any = None
        self.most_recent_capture_pil: Optional[Image.Image] = None
        self.webcam_label: Optional[tk.Label] = None
        self.entry_text: Optional[tk.Text] = None
        self.register_window: Optional[tk.Toplevel] = None
        self.register_capture: Any = None

        self.db_dir: str = './db'
        self.log_path: str = './log.txt'

        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        # 3. Setup UI and Camera
        self._setup_ui()
        self.start_webcam()

    def _setup_ui(self):
        """Initializes the UI components."""
        self.main_window.title("Face Attendance System")
        self.main_window.geometry("1200x520+350+100")

        # noinspection PyArgumentList
        util.get_button(self.main_window, 'Login', 'green', lambda: self.login()).place(x=750, y=200)
        # noinspection PyArgumentList
        util.get_button(self.main_window, 'Logout', 'red', lambda: self.logout()).place(x=750, y=300)
        # noinspection PyArgumentList
        util.get_button(self.main_window, 'Register', 'gray', lambda: self.register_new_user(), fg='black').place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

    def start_webcam(self):
        """Initializes the camera hardware."""
        self.cap = cv2.VideoCapture(0)
        self.process_webcam()

    def process_webcam(self):
        """Webcam loop processing."""
        ret, frame = self.cap.read()
        if ret:
            self.most_recent_capture_arr = frame
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_rgb)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

            if self.webcam_label:
                self.webcam_label.imgtk = imgtk  # type: ignore
                self.webcam_label.configure(image=imgtk)

        # noinspection PyArgumentList
        self.main_window.after(20, self.process_webcam)

    def login(self):
        if self.most_recent_capture_arr is None:
            return

        model_path = os.path.join(os.getcwd(), 'resources', 'anti_spoof_models')

        if test(self.most_recent_capture_arr, model_path, 0) == 1:
            name = util.recognize(self.most_recent_capture_arr, self.db_dir)
            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Alert', 'User not recognized.')
            else:
                util.msg_box('Success', f'Welcome, {name}!')
                self._log_action(name, 'in')
        else:
            util.msg_box('Alert', 'Spoof detected!')

    def logout(self):
        if self.most_recent_capture_arr is None:
            return

        name = util.recognize(self.most_recent_capture_arr, self.db_dir)
        if name not in ['unknown_person', 'no_persons_found']:
            util.msg_box('Success', f'Goodbye, {name}!')
            self._log_action(name, 'out')
        else:
            util.msg_box('Alert', 'User not recognized.')

    def _log_action(self, name, status):
        with open(self.log_path, 'a') as f:
            f.write(f'{name},{datetime.now()},{status}\n')

    def register_new_user(self):
        self.register_window = tk.Toplevel(self.main_window)
        self.register_window.geometry("1200x520+370+120")

        # noinspection PyArgumentList
        util.get_button(self.register_window, 'Accept', 'green', lambda: self.accept_register()).place(x=750, y=300)

        self.entry_text = util.get_entry_text(self.register_window)
        self.entry_text.place(x=750, y=150)

        label = util.get_img_label(self.register_window)
        label.place(x=10, y=0, width=700, height=500)

        if self.most_recent_capture_pil:
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            label.imgtk = imgtk  # type: ignore
            label.configure(image=imgtk)
            self.register_capture = self.most_recent_capture_arr.copy()

    def accept_register(self):
        if self.entry_text is None:
            return

        name = self.entry_text.get(1.0, "end-1c").strip()
        if not name:
            util.msg_box('Error', 'Please enter a name.')
            return

        # Fixed: Correct logic for face registration
        embeddings = face_recognition.face_encodings(self.register_capture)
        if len(embeddings) > 0:
            with open(os.path.join(self.db_dir, f'{name}.pickle'), 'wb') as f:
                pickle.dump(embeddings[0], f)
            util.msg_box('Success', 'User registered successfully!')
            if self.register_window:
                self.register_window.destroy()
        else:
            util.msg_box('Error', 'No face detected. Please try again.')

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
