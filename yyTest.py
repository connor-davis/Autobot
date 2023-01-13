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


class YYWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.configuration = configFile.getConfiguration()
        self.job = None
        self.listener = None
        self.enabled = False

        self.targetTitle = self.configuration.get("settings", "targetGame")
        self.silentShotTimeBefore = self.configuration.getint("silentshot", "timeBefore")
        self.silentShotTimeAfter = self.configuration.getint("silentshot", "timeAfter")
        self.silentShotLethalKey = self.configuration.get("silentshot", "lethalKey")
        self.silentShotWeaponSwapKey = self.configuration.get("silentshot", "weaponSwapKey")
        self.exitScope = self.configuration.getboolean("silentshot", "exitScope")

        # configure window
        self.title("Autobot")
        self.iconbitmap(path.join("src", "assets", "logo.ico"))
        self.resizable(False, False)

        self.rapidFireFrame = ctk.CTkFrame(self)

        self.startButton = ctk.CTkButton(self.rapidFireFrame, text="Start", command=self.startYY)
        self.startButton.pack()

        self.stopButton = ctk.CTkButton(self.rapidFireFrame, text="Stop", command=self.stopYY)
        self.stopButton.pack()

        self.rapidFireFrame.pack(padx=50, pady=50)

    def performYY(self):
        pydirectinput.PAUSE = 0

        while self.enabled:
            pydirectinput.keyDown("1")
            time.sleep(0.01)
            pydirectinput.keyUp("1")
            time.sleep(0.1)

    def handleYYActivate(self, key):
        if "{0}".format(key).replace("'", "") == "f":
            if not self.enabled:
                self.enabled = True
            else:
                self.enabled = False

            if self.job is None or not self.job.is_alive():
                self.job = threading.Thread(target=self.performYY)
                self.job.start()

    def startYY(self):
        print("Toggled yy on")
        self.listener = keyboard.Listener(on_press=self.handleYYActivate)
        self.listener.start()

    def stopYY(self):
        print("Toggled yy off")
        if self.listener is not None and self.job is not None:
            self.listener.stop()
            self.listener = None
            self.job = None


if __name__ == '__main__':
    yy = YYWindow()
    yy.mainloop()
