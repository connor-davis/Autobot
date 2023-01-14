import threading
import time
from ctypes import windll, create_unicode_buffer
from os import path
from typing import Optional

import customtkinter as ctk
import pydirectinput
from pynput import mouse
from pynput.mouse import Button

import src.utils.configFile as configFile
from src.utils.beeper import beep


def GetForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    if buf.value:
        return buf.value
    else:
        return None


ctk.set_default_color_theme("green")


class RapidFireTestWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.configuration = configFile.getConfiguration()
        self.job = None
        self.listener = None
        self.pressed = False

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

        self.startButton = ctk.CTkButton(self.rapidFireFrame, text="Start", command=self.startRapidFire)
        self.startButton.pack()

        self.stopButton = ctk.CTkButton(self.rapidFireFrame, text="Stop", command=self.stopRapidFire)
        self.stopButton.pack()

        self.rapidFireFrame.pack(padx=50, pady=50)

    def performRapidFire(self):
        while self.pressed:
                pydirectinput.PAUSE = 0

                pydirectinput.click()
                time.sleep(0.018)

    def handleClick(self, x, y, button, pressed):
        if button == Button.right and pressed:
            self.pressed = True

            beep(200, 100)
            beep(200, 100)

            print("Rapid fire can shoot")
        elif button == Button.right and not pressed:
            self.pressed = False

            beep(200, 100)

            print("Rapid fire can not shoot")

        if button == Button.left:
            if self.job is None or not self.job.is_alive():
                self.job = threading.Thread(target=self.performRapidFire)
                self.job.start()

    def startRapidFire(self):
        self.listener = mouse.Listener(on_click=self.handleClick)
        self.listener.start()

    def stopRapidFire(self):
        if self.listener is not None and self.job is not None:
            self.listener.stop()
            self.listener = None
            self.job = None

        beep(200, 100)


if __name__ == '__main__':
    rapidFireTest = RapidFireTestWindow()
    rapidFireTest.mainloop()
