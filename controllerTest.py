import threading
import time
from ctypes import windll, create_unicode_buffer
from typing import Optional

import pydirectinput

import src.utils.configFile as configFile
import pyglet
import vgamepad as vg

gamepad = vg.VDS4Gamepad()

controller = None

controllers = pyglet.input.get_controllers()

if controllers:
    controller = controllers[0]

controller.open()

job = None

configuration = configFile.getConfiguration()

targetTitle = configuration.get("settings", "targetGame")
silentShotTimeBefore = configuration.getint("silentshot", "timeBefore")
silentShotTimeAfter = configuration.getint("silentshot", "timeAfter")
silentShotLethalKey = configuration.get("silentshot", "lethalKey")
silentShotWeaponSwapKey = configuration.get("silentshot", "weaponSwapKey")
exitScope = configuration.getboolean("silentshot", "exitScope")


def GetForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    if buf.value:
        return buf.value
    else:
        return None


def rightTriggerPressed(name, value):
    global job, configuration, targetTitle, silentShotTimeBefore, silentShotTimeAfter, silentShotLethalKey, silentShotWeaponSwapKey, exitScope

    if value == 1:
        if GetForegroundWindowTitle() is not None and targetTitle in GetForegroundWindowTitle().replace("​",
                                                                                                        ""):
            configuration = configFile.getConfiguration()

            targetTitle = configuration.get("settings", "targetGame")
            silentShotTimeBefore = configuration.getint("silentshot", "timeBefore")
            silentShotTimeAfter = configuration.getint("silentshot", "timeAfter")
            silentShotLethalKey = configuration.get("silentshot", "lethalKey")
            silentShotWeaponSwapKey = configuration.get("silentshot", "weaponSwapKey")
            exitScope = configuration.getboolean("silentshot", "exitScope")

            if configuration.get("silentshot", "enabled") == "1":
                print("Sending silent shot gamepad");

                gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
                gamepad.update()
                time.sleep(0.5)
                gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
                gamepad.update()
                time.sleep(0.5)

                # pydirectinput.PAUSE = 0
                # pydirectinput.mouseDown(button=pydirectinput.LEFT)
                #
                # if targetTitle == "Modern Warfare":
                #     time.sleep(0.02)
                # else:
                #     time.sleep(0.04)
                #
                # pydirectinput.mouseUp(button=pydirectinput.LEFT)
                # time.sleep((int(silentShotTimeBefore) / 1000))
                # pydirectinput.keyDown("%s" % silentShotLethalKey.lower())
                # time.sleep((int(silentShotTimeAfter) / 1000))
                # pydirectinput.keyDown("%s" % silentShotWeaponSwapKey.lower())
                # time.sleep(0.035)
                # pydirectinput.keyUp("%s" % silentShotWeaponSwapKey.lower())
                # time.sleep(0.025)
                # pydirectinput.keyUp("%s" % silentShotLethalKey.lower())
                #
                # if exitScope:
                #     pydirectinput.mouseUp(button=pydirectinput.RIGHT)


while True:
    @controller.event
    def on_button_press(controller, button_name):
        global job

        print("%s pressed from %s" % (button_name, controller))

        if button_name == "a":
            print("Sending silent shot gamepad");

            time.sleep(5)

            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
            time.sleep(0.5)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
            time.sleep(0.5)
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
            time.sleep(0.5)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
            time.sleep(0.5)
            gamepad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
            time.sleep(0.5)
            gamepad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
            gamepad.update()
            time.sleep(0.5)


    @controller.event
    def on_trigger_motion(controller, name, value):
        global job

        if job is None or not job.is_alive():
            job = threading.Thread(target=rightTriggerPressed, args=(name, value))
            job.start()
