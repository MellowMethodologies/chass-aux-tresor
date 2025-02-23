import cv2
import numpy as np
from mss import mss
import pytesseract
import time
import hashlib
import re

method = cv2.TM_SQDIFF_NORMED  # Using squared difference normalized method

def parse_coordinates(input_string):
    numbers = re.findall(r'-?\d+', input_string)
    if len(numbers) >= 2:
        return f"[{numbers[0]},{numbers[1]}]"
    return None

# return the pin position  / and the valid button when no white pin and the valid is green in the same time
# return the fight button position
class TreasureHuntMonitor:
    def __init__(self):
        self.sct = mss()
        self.result_cache = {}
        self.last_hash = None
        
        # Define regions of interest
        self.regions = {
            'player_pos': {"top": 68, "left": 0, "width": 90, "height": 26},
            'depart': {"top": 227, "left": 81, "width": 90, "height": 20},
            'indices': {"top": 250, "left": 1, "width": 322, "height": 500}
        }
        
        # Load arrow templates
        self.icon_template = cv2.imread("../screens/pin.png")
        self.arrows = {
            'top': cv2.imread("../screens/arrows/top.png"),
            'down': cv2.imread("../screens/arrows/down.png"),
            'left': cv2.imread("../screens/arrows/left.png"),
            'right': cv2.imread("../screens/arrows/right.png")
        }

    def detect_image(self, screenshot, template, threshold=0.1):
        try:
            result = cv2.matchTemplate(screenshot, template, method)
            min_val, _, min_loc, _ = cv2.minMaxLoc(result)
            return (min_val < threshold), min_loc
        except Exception as e:
            print(f"Detection error: {e}")
            return False, (0, 0)

    def process_frame(self, screenshot):
        # Check if frame is different from previous
        current_hash = hashlib.md5(screenshot.tobytes()).hexdigest()
        if current_hash == self.last_hash:
            return None
        self.last_hash = current_hash

        results = {}
        
        # Detect main icon
        icon_detected, loc = self.detect_image(screenshot, self.icon_template, 0.1)
        results['icon_detected'] = icon_detected
        results['pin_pos'] = loc
        
        if icon_detected:
            # Process player position
            results['player_pos'] = parse_coordinates(
                self.process_region(screenshot, 'player_pos')
            )

            # Process depart text
            results['depart'] = self.process_region(screenshot, 'depart')

            # Detect arrows
            icon_x, icon_y = loc
            arrow_region = screenshot[
                max(0, icon_y-20):min(screenshot.shape[0], icon_y+30),
                0:40
            ]
            results['arrow'] = 'none'
            for name, arrow in self.arrows.items():
                detected, _ = self.detect_image(arrow_region, arrow, 0.1)
                if detected:
                    results['arrow'] = name
                    break

            # Process indices
            indices_roi = screenshot[
                max(0, icon_y-10):min(screenshot.shape[0], icon_y+20),
                37:150
            ]
            results['indices'] = self.process_region_image(indices_roi)
        else:
            results['error'] = 'Icon not detected'

        return results

    def process_region_image(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return pytesseract.image_to_string(rgb_image, config=r'--oem 3 --psm 6').strip()

    def process_region(self, image, region_name):
        region = self.regions[region_name]
        y1 = region["top"] - 20
        y2 = y1 + region["height"]
        x1 = region["left"]
        x2 = x1 + region["width"]
        
        roi = image[y1:y2, x1:x2]
        rgb_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        
        cache_key = f"{region_name}_{hashlib.md5(roi.tobytes()).hexdigest()}"
        if cache_key in self.result_cache:
            return self.result_cache[cache_key]
        
        text = pytesseract.image_to_string(rgb_roi, config=r'--oem 3 --psm 6').strip()
        self.result_cache[cache_key] = text
        return text

    def run(self):
        monitor_region = {"top": 20, "left": 1, "width": 322, "height": 410}
        
        try:
            while True:
                # Capture screenshot
                screenshot = cv2.cvtColor(np.array(self.sct.grab(monitor_region)), cv2.COLOR_RGBA2BGR)
                
                # Process frame
                results = self.process_frame(screenshot)
                
                if results:
                    return(self.print_results(results))
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped")

    def print_results(self, results):
        print("\n" + "="*40)
        if 'error' in results:
            print(results['error'])
            return

        # print(f"Icon detected: {results['icon_detected']}")
        if results['icon_detected']:
            print(f"Player position: {results['player_pos']}")
            print(f"Depart text: {results['depart']}")
            print(f"Arrow direction: {results['arrow']}")
            print(f"Indices:\n{results['indices']}")
            return results
        # print("="*40 + "\n")
