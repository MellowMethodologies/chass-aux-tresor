import pyautogui
import time
import uinput
from concurrent.futures import ThreadPoolExecutor

# Optimize PyAutoGUI settings
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0

def create_mouse():
    events = (
        uinput.BTN_LEFT,
        uinput.BTN_RIGHT,
        uinput.REL_X,
        uinput.REL_Y
    )
    device = uinput.Device(events)
    time.sleep(0.5)
    return device

def click(device, button=uinput.BTN_LEFT):
    device.emit(button, 1)
    time.sleep(0.5)
    device.emit(button, 0)

def move_and_click(device, rel_x, rel_y):
    device.emit(uinput.REL_X, rel_x)
    device.emit(uinput.REL_Y, rel_y)
    click(device)

mouse = create_mouse()

def find_image_on_screen(image_path, confidence=0.65):
    try:
        screen_width, screen_height = pyautogui.size()
        search_zone = (130, 400, screen_width // 2, screen_height)
        
        location = pyautogui.locateOnScreen(image_path, confidence=confidence, 
                                          region=search_zone, grayscale=True)
        if location:
            center_location = pyautogui.center(location)
            pyautogui.press('1')
            pyautogui.moveTo(center_location, duration=0)
            click(mouse)
            return True
        return False
    except Exception as e:
        return False

def find_png_on_screen():
    try:
        find_png = pyautogui.locateOnScreen('./assets/png.png', confidence=0.8, grayscale=True)
        if find_png:
            pyautogui.moveTo(find_png, duration=0)
            click(mouse)
            time.sleep(1)
            
            click_text = pyautogui.locateOnScreen('./assets/cliv.png', 
                                                 confidence=0.7, grayscale=True)
            if click_text:
                pyautogui.moveTo(click_text, duration=0)
                click(mouse)
                time.sleep(1.5)
                pyautogui.press('f1')
                return True
        return False
    except Exception:
        return False

def process_images(image_paths):
    for path in image_paths:
        find_image_on_screen(path)

def main():
    image_paths = ['./assets/tofuright.png', './assets/tofule.png']
    search_interval = 0.5
    cycle_duration = 60  # Duration in seconds for each cycle
    
    try:
        while True:
            cycle_start = time.time()
            
            while time.time() - cycle_start < cycle_duration:
                find_png_on_screen()
                process_images(image_paths)
                time.sleep(search_interval)
                pyautogui.moveTo(1500, 200, duration=0.01)
                
                remaining = cycle_duration - (time.time() - cycle_start)
                if remaining > 0:
                    print(f"Time left: {remaining:.1f} seconds")
            
            print("Cycle complete, starting new cycle")
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nScript stopped by user")

if __name__ == "__main__":
    main()