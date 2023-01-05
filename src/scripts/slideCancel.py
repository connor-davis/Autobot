import configparser
import threading
import time
from ctypes import windll, create_unicode_buffer
from typing import Optional

import pydirectinput
from pynput import keyboard
import src.utils.configFile as configFile

configuration = configFile.getConfiguration()

def GetForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    if buf.value:
        return buf.value
    else:
        return None


targetTitle = "Modern Warfare"


def performSlideCancel():
    global job, configuration

    configuration = configFile.getConfiguration()

    slideCancelSlideKey = configuration.get("slidecancel", "slideKey")
    slideCancelCancelKey = configuration.get("slidecancel", "cancelKey")

    if GetForegroundWindowTitle() is not None and targetTitle in GetForegroundWindowTitle().replace("​",
                                                                                                    ""):
        pydirectinput.PAUSE = 0
        pydirectinput.keyDown("%s" % slideCancelSlideKey.lower())
        time.sleep(0.08)
        pydirectinput.keyUp("%s" % slideCancelSlideKey.lower())
        time.sleep(0.08)
        pydirectinput.keyDown("%s" % slideCancelSlideKey.lower())
        time.sleep(0.08)
        pydirectinput.keyUp("%s" % slideCancelSlideKey.lower())
        time.sleep(0.035)
        pydirectinput.keyDown("%s" % slideCancelCancelKey.lower())
        time.sleep(0.035)
        pydirectinput.keyUp("%s" % slideCancelCancelKey.lower())

        job = None


def handlePress(key):
    global job, configuration

    configuration = configFile.getConfiguration()

    slideCancelEnabled = configuration.get("slidecancel", "enabled") == "1"
    slideCancelActivatorKey = configuration.get("slidecancel", "activatorKey")

    if "{0}".format(key).replace("'", "") == slideCancelActivatorKey.lower() and slideCancelEnabled is True:
        if job is None or not job.is_alive():
            job = threading.Thread(target=performSlideCancel)
            job.start()


job = None

listener = keyboard.Listener(on_press=handlePress)


def initializeSlideCancel():
    listener.start()


def uninitializeSlideCancel():
    listener.stop()
