import configparser
from pynput import keyboard
from pynput.keyboard import Key
from src.utils.beeper import *
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.dialogs import Messagebox

listener = None

def handlePress(key):
    silentShotConfig = configparser.ConfigParser()
    silentShotConfig.read("data/silentShot.ini")

    slideCancelConfig = configparser.ConfigParser()
    slideCancelConfig.read("data/slideCancel.ini")

    if key == Key.f2:
        if silentShotConfig["config"]["enabled"] == "0":
            silentShotConfig["config"]["enabled"] = "1"

            beep(200, 100)
            beep(200, 100)
        else:
            silentShotConfig["config"]["enabled"] = "0"
            
            beep(200, 100)
    if key == Key.f3:
        if slideCancelConfig["config"]["enabled"] == "0":
            slideCancelConfig["config"]["enabled"] = "1"

            beep(200, 100)
            beep(200, 100)
        else:
            slideCancelConfig["config"]["enabled"] = "0"

            beep(200, 100)

    with open('data/silentShot.ini', 'w') as configfile:
        silentShotConfig.write(configfile)

    with open('data/slideCancel.ini', 'w') as configfile:
        slideCancelConfig.write(configfile)

def initializeToggler():
    global listener

    listener = keyboard.Listener(on_press=handlePress)
    listener.start()


def uninitializeToggler():
    global listener

    listener.stop()
