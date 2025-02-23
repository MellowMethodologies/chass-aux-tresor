import pyautogui

def move_maps(position, x, arrow, t, X=10):
    # Extract coordinates from position string
    try:
        coords = eval(position)  # Converts '[x,y]' to tuple
        map_x, map_y = coords
    except (SyntaxError, TypeError):
        print("Invalid position format. Use '[x,y]'")
        return False

    tries = 0
    while tries < X:
        # Move to the next map using alt + arrow key
        pyautogui.keyDown('alt')
        pyautogui.press(arrow)
        pyautogui.keyUp('alt')
        
        # Wait for map transition
        pyautogui.sleep(t)
        
        # Look for the image X times
        for _ in range(x):
            # Try to find the image on screen
            try:
                # Using grayscale=True for better matching
                image_pos = pyautogui.locateCenterOnScreen('x.png', confidence=0.8, grayscale=True)
                if image_pos:
                    # Click on the found image
                    pyautogui.click(image_pos)
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            
            # Short pause between checks
            pyautogui.sleep(0.5)
        
        tries += 1
    
    # If we've exhausted all tries
    print(f"Failed to find image after {X} attempts")
    return False