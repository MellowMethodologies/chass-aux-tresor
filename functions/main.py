import pyautogui
import time
import uinput
from concurrent.futures import ThreadPoolExecutor
from capture_screnn import TreasureHuntMonitor
from req_positions import get_positions



# Configure pyautogui for faster execution
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0.1  # Small pause between actions for reliability

# Create a virtual mouse device using uinput
def create_mouse():
    events = (
        uinput.BTN_LEFT,
        uinput.BTN_RIGHT,
        uinput.REL_X,
        uinput.REL_Y
    )
    device = uinput.Device(events)
    time.sleep(0.5)  # Allow time for the device to initialize
    return device

# Simulate a mouse click
def click(device, button=uinput.BTN_LEFT):
    device.emit(button, 1)  # Press the button
    time.sleep(0.05)        # Short delay for the click
    device.emit(button, 0)  # Release the button

# Move the mouse and click
def move_and_click(device, rel_x, rel_y):
    device.emit(uinput.REL_X, rel_x)  # Move horizontally
    device.emit(uinput.REL_Y, rel_y)  # Move vertically
    click(device)                     # Click at the new position

# Initialize the virtual mouse
mouse = create_mouse()

# Main function
# 
# Icon detected: True
# Player position: (-25, -36)
# Depart text: Start [-4,-53]
# Cania Plains (Stontusk Desert)
# Arrow direction: left
# Indices:
# sneaky Drheller
def main():
    seq = TreasureHuntMonitor()

    try:
        while True:
            print("Starting sequence...")
            time.sleep(4)  # Wait for 4 seconds before starting

            # Move the mouse and click at (100, 100) relative to the current position
            move_and_click(mouse, 100, 100)

            # Simulate keyboard actions
            pyautogui.press('tab')            # Press the Tab key
            pyautogui.write() # Type the text
            pyautogui.press('enter')         # Press Enter
            pyautogui.press('enter')          # Press Enter again

            print("Sequence completed. Waiting for the next iteration...")
    except KeyboardInterrupt:
        print("Script terminated by user.")

# Run the main function
if __name__ == "__main__":
    main()