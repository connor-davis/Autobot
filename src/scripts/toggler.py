import configparser
from pynput import keyboard
from pynput.keyboard import Key
from src.utils.beeper import *
import src.utils.configFile as configFile

listener = None

def handlePress(key):
    configuration = configFile.getConfiguration()

    if key == Key.f2:
        if configuration.getboolean("silentshot", "enabled"):
            configuration.set("silentshot", "enabled", "0")

            beep(200, 100)
        else:
            configuration.set("silentshot", "enabled", "1")
            
            beep(200, 100)
            beep(200, 100)
    if key == Key.f3:
        if configuration.getboolean("slidecancel", "enabled"):
            configuration.set("slidecancel", "enabled", "0")

            beep(200, 100)
        else:
            configuration.set("slidecancel", "enabled", "1")

            beep(200, 100)
            beep(200, 100)

    with open('data/configuration.ini', 'w') as configfile:
        configuration.write(configfile)
        configfile.flush()
        configfile.close()

def initializeToggler():
    global listener

    listener = keyboard.Listener(on_press=handlePress)
    listener.start()


def uninitializeToggler():
    global listener

    listener.stop()
