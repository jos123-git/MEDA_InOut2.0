import pyautogui
from datetime import datetime
import os
import config as cfg

os.makedirs(cfg.screenshot_folder_name, exist_ok=True)

def take_screenshot(log_callback=None):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"{cfg.screenshot_folder_name}/screenshot_{timestamp}.png"

    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

    if log_callback:
        log_callback(f"Screenshot saved")