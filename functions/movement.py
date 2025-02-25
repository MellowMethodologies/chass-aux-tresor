import pyautogui
import time
from find_phorreur import detect_screen_change


def move_maps(position, images, arrow, t, X=10):
    # Extract coordinates from position string
    try:
        coords = eval(position)  # Converts '[x,y]' to tuple
        map_x, map_y = coords
    except (SyntaxError, TypeError):
        print("Invalid position format. Use '[x,y]'")
        return False
    image_pos = None
        # Look for the image X times
    for _ in range(X):
            # Try each image in the list
        for image in images:
            try:
                # Using grayscale=True for better matching

                image_pos = pyautogui.locateCenterOnScreen(image, confidence=0.629)
                if image_pos:
                    return True
            except pyautogui.ImageNotFoundException:
                continue
        if image_pos is None:
            pyautogui.keyDown('alt')
            pyautogui.press(arrow)
            pyautogui.keyUp('alt')
            detect_screen_change([0, 70, 77, 25])
            
            # Short pause between checks
        time.sleep(0.5)
        
    
    # If we've exhausted all tries
    print(f"Failed to find any of the images after {X} attempts")
    return False
