from pynput import keyboard
from datetime import datetime
import os
import config as cfg

listener = None
keystroke_callback = None

log_folder = cfg.log_folder_name
os.makedirs(log_folder, exist_ok=True)

# ---------- DAILY FILE ----------
def get_log_file():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(log_folder, f"{today}.txt")

# ---------- EVENT LOGGER ----------
def log_event(status):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(get_log_file(), "a") as f:
        f.write(f"{status} | {timestamp}\n")

# ---------- KEY LOGGER WITH CPM TRACKING ----------
def log_key(key): 
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Track keystroke for CPM
    if keystroke_callback:
        keystroke_callback()

    # Only log actual character keys (filter out special keys)
    try:
        if hasattr(key, 'char') and key.char:
            with open(get_log_file(), "a") as f:
                f.write(f"Keystroke | {timestamp}\n")
    except:
        pass

# ---------- SET KEYSTROKE CALLBACK ----------
def set_keystroke_callback(callback):
    """Set callback function to be called on each keystroke"""
    global keystroke_callback
    keystroke_callback = callback

# ---------- START ----------
def start_logger():
    global listener
    if listener is None:
        listener = keyboard.Listener(on_press=log_key) 
        listener.start()

# ---------- STOP ----------
def stop_logger():
    global listener
    if listener:
        listener.stop()
        listener = None