import pyautogui
import time

def write(text:str):
    time.sleep(5)

    for char in text:
        pyautogui.press(char)


write("")

# Primitive virtual keyboard emulator to paste text in target window. When copy and past doesn't work, for example in web consoles:
# - enter text to be pasted in write("")
# - run program
# - switch to target window
# - wait until its done
