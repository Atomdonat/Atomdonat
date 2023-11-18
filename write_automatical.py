import pyautogui
import time

def write(text:str):
    time.sleep(5)

    for char in text:
        pyautogui.press(char)


write("")