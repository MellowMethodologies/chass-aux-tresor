import pyautogui
import time
import re
import uinput
from concurrent.futures import ThreadPoolExecutor
from capture_screnn import TreasureHuntMonitor
from req_positions import get_positions
from parse_coordinate import find_closest_zaap
from movement import move_maps
from find_phorreur import detect_screen_change

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
    time.sleep(0.09)        # Short delay for the click
    device.emit(button, 0)  # Release the button
    time.sleep(5)        # Short delay before moving again

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

def redirect_Arrow(arrow):
    if arrow == 'left':
        return 'right'
    elif arrow == 'right':
        return 'left'
    elif arrow == 'up':
        return 'down'
    elif arrow == 'down':
        return 'up'


def main():
    seq = TreasureHuntMonitor()

    #/ go to the closest zaap
    monitor =seq.run()
    depart = monitor['depart']

    zaap = find_closest_zaap(monitor['depart'])
    if f'[{zaap[1][0]},{zaap[1][1]}]' != monitor['player_pos'] and monitor['player_pos'] != depart:
        pyautogui.press('h')
        time.sleep(2)
        pyautogui.moveTo(530, 430)
        click(mouse)

        pyautogui.write(zaap[0], interval=0.1)
        pyautogui.press('enter')
        time.sleep(2)
    if monitor['player_pos'] != depart:
        pyautogui.press('tab')
        pyautogui.write(f'/travel {monitor['depart'][1:-1]}', interval=0.1)
        time.sleep(1)
        pyautogui.press('enter',3,2)
        while monitor['player_pos'] != depart:
            # detect_screen_change([0, 70, 77, 25])
            time.sleep(4)
            monitor = seq.run()
    try:
        while True:
            print("Starting sequence...")
            time.sleep(4)  # Wait for 4 seconds before starting
            monitor = seq.run()
            loc = get_positions("en", monitor['player_pos'][1:-1], monitor["arrow"], 10, monitor['indices'])
            while loc == 'dr' and move_maps('[-10,-30]', ['../screens/drheller/drheller.png','../screens/drheller/drheller_back.png'], monitor['arrow'],0, 10) :
                print("drheller found")
                time.sleep(1)
                pyautogui.moveTo(monitor['pin_pos'][0]+8, monitor['pin_pos'][1]+28)
                click(mouse)
                break
            
            if loc != 'dr':
                pyautogui.press('tab')
                pyautogui.write(f'/travel {loc}', interval=0.1)
                time.sleep(1)
                pyautogui.press('enter',3, 2)


            while loc!= 'dr' and monitor['player_pos'] and loc != monitor['player_pos'][1:-1]:
                time.sleep(4)
                monitor = seq.run()
            
            if monitor['player_pos'].isString() and loc == monitor['player_pos'][1:-1]:
                print("You have reached the destination")
                pyautogui.moveTo(monitor['pin_pos'][0]+8,monitor['pin_pos'][1]+28)
                click(mouse)
                continue
            #check if the user reaches the distination 
            # print(monitor)

    #         move_and_click(mouse, 100, 100)
    #         # # Simulate keyboard actions
    #         # pyautogui.press('tab')          # Press the Tab key
    #         # pyautogui.write('hello') # Type the text
    #         # pyautogui.press('enter')         # Press Enter
    #         # pyautogui.press('enter')          # Press Enter again

            print("Sequence completed. Waiting for the next iteration...")
    except KeyboardInterrupt:
        print("Script terminated by user.")

# Run the main function
if __name__ == "__main__":
    main()