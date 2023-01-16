import threading
import time
from ctypes import windll, create_unicode_buffer
from typing import Optional

import pydirectinput
from pynput import keyboard

from src.utils.configFile import getConfiguration


def GetForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    if buf.value:
        return buf.value
    else:
        return None


class AntiRecoil:
    def __init__(self):
        self.listener = None
        self.job = None
        self.toggled = False
        self.configuration = getConfiguration()

        self.targetTitle = self.configuration.get("settings", "targetGame")
        self.enabled = self.configuration.getboolean("antirecoil", "enabled")
        self.toggleKey = self.configuration.get("antirecoil", "toggleKey")
        self.verticalStrength = int(self.configuration.get("antirecoil", "verticalStrength"))
        self.horizontalStrength = int(self.configuration.get("antirecoil", "horizontalStrength"))

    def runAntiRecoil(self):
        self.configuration = getConfiguration()
        self.targetTitle = self.configuration.get("settings", "targetGame")

        # if GetForegroundWindowTitle() is not None and self.targetTitle in GetForegroundWindowTitle().replace("​",
        #                                                                                                      ""):
        self.verticalStrength = self.configuration.get("antirecoil", "verticalStrength")
        self.horizontalStrength = self.configuration.get("antirecoil", "horizontalStrength")

        pydirectinput.PAUSE = 0

        while self.toggled:
            pydirectinput.moveRel(-int(self.horizontalStrength), int(self.verticalStrength))

            time.sleep(0.02)

        self.job = None

    def toggle(self):
        if self.toggled:
            self.toggled = False
            self.job = None
            self.listener = None
        else:
            self.toggled = True

    def handleKeyPress(self, key):
        self.configuration = getConfiguration()
        self.enabled = self.configuration.getboolean("antirecoil", "enabled")
        self.toggleKey = self.configuration.get("antirecoil", "toggleKey")

        if "{0}".format(key).replace("'", "") == self.toggleKey.lower():
            self.toggle()

            if self.enabled and self.job is None or not self.job.is_alive():
                job = threading.Thread(target=self.runAntiRecoil)
                job.start()

    def start(self):
        self.enabled = True
        self.listener = keyboard.Listener(on_press=self.handleKeyPress)
        self.listener.start()

        print("Started anti-recoil")

    def stop(self):
        try:
            self.listener.stop()
            self.listener = None
            self.job = None
        except:
            print("Error")

        print("Stopped anti-recoil.")
