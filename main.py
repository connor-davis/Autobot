import configparser
from os import path

import ttkbootstrap as ttb

import src.gui.window as window
import updater

settings = configparser.ConfigParser()
settings.read("data/settings.ini")

if __name__ == '__main__':
    root = ttb.Window(themename=settings["settings"]["theme"])
    root.title("Autobot")
    iconFile = path.join("src", "assets", "logo.ico")
    root.iconbitmap(iconFile)

    root.overrideredirect(True)

    print("Running updater.")

    updater.runUpdater(root)

    print("Running window.")

    root.overrideredirect(False)

    window.runWindow(root)

    print("Application has finished.")
