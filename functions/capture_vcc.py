import cv2
import numpy as np
from mss import mss
import pytesseract
import time
import threading
from queue import Queue
import hashlib

class EnhancedScreenMonitor:
    def __init__(self):
        self.screenshot_queue = Queue(maxsize=1)
        self.result_cache = {}
        self.running = True
        self.last_hash = None
        
        # Define the monitoring region
        self.monitor = {
            "top": 300,
            "left": 700,
            "width": 500,
            "height": 500
        }

    def process_screenshots(self):
        while self.running:
            try:
                if not self.screenshot_queue.empty():
                    screenshot = self.screenshot_queue.get()
                    
                    # Process the image and get text
                    text = self.process_image(screenshot)
                    if text:
                        lines = [line.strip() for line in text.split('\n') if line.strip()]
                        for line in lines:
                            print(line)
                        print("-" * 50)
                    
            except Exception as e:
                print(f"Error processing screenshot: {e}")
            
            time.sleep(0.1)

    def process_image(self, image):
        """Enhanced image processing pipeline"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Rescale image to improve small text readability
        scale_factor = 2
        gray = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        
        # Noise reduction using median blur
        gray = cv2.medianBlur(gray, 3)
        
        # Contrast Limited Adaptive Histogram Equalization
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        
        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
        
        # Morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Invert image if needed (white text on black background)
        cleaned = cv2.bitwise_not(cleaned)
        
        # Tesseract configuration
        config = '--psm 6 --oem 3 '
        
        return pytesseract.image_to_string(cleaned, config=config).strip()

    def capture_screenshot(self):
        with mss() as sct:
            while self.running:
                try:
                    screenshot = np.array(sct.grab(self.monitor))
                    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                    
                    current_hash = hashlib.md5(screenshot.tobytes()).hexdigest()
                    if current_hash != self.last_hash:
                        self.last_hash = current_hash
                        if self.screenshot_queue.full():
                            self.screenshot_queue.get()
                        self.screenshot_queue.put(screenshot)
                
                except Exception as e:
                    print(f"Error capturing screenshot: {e}")
                
                time.sleep(0.1)

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
    monitor = EnhancedScreenMonitor()
    monitor.run()

if __name__ == "__main__":
    main()