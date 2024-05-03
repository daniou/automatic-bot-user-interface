import pyautogui
import time

while True:
    x, y = pyautogui.position()
    print(f"Posición del ratón: X={x}, Y={y}")
    time.sleep(0.2)
