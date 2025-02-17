import cv2
import numpy as np
from mss import mss
import pytesseract
import time
import threading
from queue import Queue
import hashlib
import re

method = cv2.TM_SQDIFF_NORMED  # Using squared difference normalized method

def parse_coordinates( input_string):
    numbers = re.findall(r'-?\d+', input_string)
        
    if len(numbers) >= 2:
        return (int(numbers[0]), int(numbers[1]))
        
    return None  

class TreasureHuntMonitor:
    def __init__(self):
        self.sct = mss()
        self.screenshot_queue = Queue(maxsize=1)
        self.result_cache = {}
        self.running = True
        self.last_hash = None
        
        # Define regions of interest
        self.regions = {
            'player_pos': {"top": 68, "left": 0, "width": 90, "height": 26},
            'depart': {"top": 227, "left": 30, "width": 250, "height": 44},
            'indices': {"top": 250, "left": 1, "width": 322, "height": 500}
        }
        self.icon_template = cv2.imread("../screens/pin.png")
        self.top_arrow = cv2.imread("../screens/arrows/top.png")
        self.bottom_arrow = cv2.imread("../screens/arrows/down.png")
        self.left_arrow = cv2.imread("../screens/arrows/left.png")
        self.right_arrow = cv2.imread("../screens/arrows/right.png")


    def detect_image(self, screenshot, arrow_template, threshold=0.1):
        try:
            result = cv2.matchTemplate(screenshot, arrow_template, method)
            min_val, _, min_loc, _ = cv2.minMaxLoc(result)
            print(min_loc)
            return min_val < threshold, min_loc
        except Exception as e:
            print(f"Detection error: {e}")
            return False, (0, 0)

    def process_screenshots(self):
        while self.running:
            try:
                if not self.screenshot_queue.empty():
                    screenshot = self.screenshot_queue.get()
                    
                    icon_detected, loc = self.detect_image(screenshot, self.icon_template, 0.4)

                    # Process regions in color
                    player_pos = parse_coordinates(self.process_region(screenshot, 'player_pos'))
                    depart = self.process_region(screenshot, 'depart')
                    arrow_pos = 'none'

                    # Dynamic indices region and arrow detection
                    indices = ""
                if icon_detected:
                    icon_x, icon_y = loc

                    # Adjusted arrow detection region (0-40 width, same Y-axis)
                    arrow_region = screenshot[
                        max(0, icon_y-20):min(screenshot.shape[0], icon_y+20),
                        0:40  # Fixed left 40px width
                    ]
                    
                    # Arrow detection
                    for arrow, name in [(self.top_arrow, "top"),
                                      (self.bottom_arrow, "down"),
                                      (self.left_arrow, "left"),
                                      (self.right_arrow, "right")]:
                        detected, _ = self.detect_image(arrow_region, arrow, 0.1)
                        if detected:
                            arrow_pos = name
                            break

                    # Indices processing
                    indices_roi = screenshot[
                        max(0, icon_y-10):min(screenshot.shape[0], icon_y+20),
                        37:187  # Adjusted indices region
                    ]
                    indices = self.process_region_image(indices_roi)
                else:
                    indices = self.process_region(screenshot, 'indices')

                # Print results
                print(f"\nIcon detected: {icon_detected}")
                print(f"Player position: {player_pos}")
                print(f"Depart: {depart}")
                print(f"Arrow direction: {arrow_pos}")
                print(f"Indices:\n{indices}")
                print("-" * 50)
                    
            except Exception as e:
                print(f"Error processing screenshot: {e}")
            
            time.sleep(0.1)

    def process_region_image(self, image):
        """Process color images directly"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return pytesseract.image_to_string(rgb_image, config=r'--oem 3 --psm 6').strip()

    def capture_screenshot(self):
        while self.running:
            with mss() as sct:
                monitor = {"top": 20, "left": 1, "width": 322, "height": 410}
                # Convert RGBA to BGR format (3 channels)
                screenshot = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_RGBA2BGR)
                current_hash = hashlib.md5(screenshot.tobytes()).hexdigest()
                if current_hash != self.last_hash:
                    self.last_hash = current_hash
                    if self.screenshot_queue.full():
                        self.screenshot_queue.get()
                    self.screenshot_queue.put(screenshot)
                time.sleep(0.1)

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
        capture_thread = threading.Thread(target=self.capture_screenshot)
        process_thread = threading.Thread(target=self.process_screenshots)
        capture_thread.start()
        process_thread.start()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
            capture_thread.join()
            process_thread.join()
            print("Monitoring stopped")

def main():
    monitor = TreasureHuntMonitor()
    monitor.run()

if __name__ == "__main__":
    main()
