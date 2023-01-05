import configparser
import threading
import time
from ctypes import windll, create_unicode_buffer
from typing import Optional

import pydirectinput
from pynput import mouse
from pynput.mouse import Button

import src.utils.configFile as configFile

def GetForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    if buf.value:
        return buf.value
    else:
        return None


def performSilentShot(x, y, button, pressed, targetTitle, silentShotTimeBefore, silentShotTimeAfter, silentShotLethalKey, silentShotWeaponSwapKey, exitScope):
    global job

    if GetForegroundWindowTitle() is not None and targetTitle in GetForegroundWindowTitle().replace("​",
                                                                                                    "") and pressed:
        pydirectinput.PAUSE = 0
        pydirectinput.mouseDown(button=pydirectinput.LEFT)

        if targetTitle == "Modern Warfare":
            time.sleep(0.02)
        else:
            time.sleep(0.04)

        pydirectinput.mouseUp(button=pydirectinput.LEFT)
        time.sleep((int(silentShotTimeBefore) / 1000))
        pydirectinput.keyDown("%s" % silentShotLethalKey.lower())
        time.sleep((int(silentShotTimeAfter) / 1000))
        pydirectinput.keyDown("%s" % silentShotWeaponSwapKey.lower())
        time.sleep(0.035)
        pydirectinput.keyUp("%s" % silentShotWeaponSwapKey.lower())
        time.sleep(0.025)
        pydirectinput.keyUp("%s" % silentShotLethalKey.lower())

        if exitScope:
            pydirectinput.mouseUp(button=pydirectinput.RIGHT)


def handleClick(x, y, button, pressed):
    global job

    configuration = configFile.getConfiguration()

    targetTitle = configuration.get("settings", "targetGame")
    silentShot = configuration.getboolean("silentshot", "enabled")
    silentShotTimeBefore = configuration.getint("silentshot", "timeBefore")
    silentShotTimeAfter = configuration.getint("silentshot", "timeAfter")
    silentShotLethalKey = configuration.get("silentshot", "lethalKey")
    silentShotWeaponSwapKey = configuration.get("silentshot", "weaponSwapKey")
    exitScope = configuration.getboolean("silentshot", "exitScope")

    if button == Button.left and silentShot:
        if job is None or not job.is_alive():
            job = threading.Thread(target=performSilentShot, args=(x, y, button, pressed, targetTitle, silentShotTimeBefore, silentShotTimeAfter, silentShotLethalKey, silentShotWeaponSwapKey, exitScope))
            job.start()


job = None

listener = mouse.Listener(on_click=handleClick)


def initializeSilentShot():
    listener.start()


def uninitializeSilentShot():
    listener.stop()
