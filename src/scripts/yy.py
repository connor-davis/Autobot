import threading
import time
from ctypes import windll, create_unicode_buffer
from os import path
from typing import Optional

import customtkinter as ctk
import pydirectinput
from pynput import mouse
from pynput.mouse import Button
from pynput import keyboard

import src.utils.configFile as configFile
from src.utils.beeper import beep

configuration = configFile.getConfiguration()

targetTitle = configuration.get("settings", "targetGame")
yyEnabled = configuration.getboolean("yy", "enabled")
yyActivatorKey = configuration.get("yy", "activatorKey")
yyWeaponSwapKey = configuration.get("yy", "weaponSwapKey")
yyDelay = configuration.get("yy", "delay")

doYY = False
job = None
listener = None

def GetForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    if buf.value:
        return buf.value
    else:
        return None

def performYY():
    global job, targetTitle, configuration, yyEnabled, yyActivatorKey, yyWeaponSwapKey, yyDelay, doYY

    if GetForegroundWindowTitle() is not None and targetTitle in GetForegroundWindowTitle().replace("​",
                                                                                                    ""):
        configuration = configFile.getConfiguration()

        yyEnabled = configuration.getboolean("yy", "enabled")
        yyActivatorKey = configuration.get("yy", "activatorKey")
        yyWeaponSwapKey = configuration.get("yy", "weaponSwapKey")
        yyDelay = configuration.get("yy", "delay")

        pydirectinput.PAUSE = 0

        while doYY and yyEnabled:
            pydirectinput.keyDown("1")
            time.sleep(0.01)
            pydirectinput.keyUp("1")
            time.sleep(0.1)


def handleYYActivate(key):
    global job, doYY, configuration, yyEnabled, yyActivatorKey

    configuration = configFile.getConfiguration()

    yyEnabled = configuration.getboolean("yy", "enabled")
    yyActivatorKey = configuration.get("yy", "activatorKey")

    if yyEnabled and "{0}".format(key).replace("'", "") == yyActivatorKey:
        if not doYY:
            doYY = True
        else:
            doYY = False

        if job is None or not job.is_alive():
            job = threading.Thread(target=performYY)
            job.start()


def initializeYY():
    global listener

    listener = keyboard.Listener(on_press=handleYYActivate)
    listener.start()


def uninitializeYY():
    global listener, job

    if listener is not None and job is not None:
        listener.stop()
        listener = None
        job = None