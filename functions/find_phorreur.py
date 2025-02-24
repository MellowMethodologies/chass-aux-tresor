import pyautogui
import numpy as np
import cv2
import time

def detect_screen_change(region=None, thresh_value=30):
    # Take initial screenshot
    prev_screenshot = pyautogui.screenshot(region=tuple(region))  # Convert list to tuple
    prev_frame = np.array(prev_screenshot)
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_RGB2GRAY)
    
    while True:
        # Take new screenshot
        curr_screenshot = pyautogui.screenshot(region=tuple(region))  # Convert list to tuple
        curr_frame = np.array(curr_screenshot)
        curr_frame_gray = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
        
        # Calculate difference
        diff = cv2.absdiff(prev_frame_gray, curr_frame_gray)
        
        # Apply threshold
        _, binary = cv2.threshold(diff, thresh_value, 255, cv2.THRESH_BINARY)
        
        # Find changes
        changes = np.where(binary > 0)
        if len(changes[0]) > 0:
            min_x, max_x = np.min(changes[1]), np.max(changes[1])
            min_y, max_y = np.min(changes[0]), np.max(changes[0])
            if max_x - min_x > 10 and max_y - min_y > 10:  # Ignore tiny changes
                print(f"Change detected at: ({min_x}, {min_y}) to ({max_x}, {max_y})")
            return True
        
        prev_frame_gray = curr_frame_gray
        
        time.sleep(0.1) 

