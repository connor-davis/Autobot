import configparser
from os import path

import ttkbootstrap as ttb

import src.gui.window as window
import src.utils.updateChecker as updater
import src.utils.configFile as configFile

configuration = configFile.getConfiguration()

if __name__ == '__main__':
    root = ttb.Window(themename=configuration.get("settings", "theme"))
    root.title("Autobot")

    iconFile = path.join("src", "assets", "logo.ico")

    root.iconbitmap(iconFile)

    print("Running updater.")

    updater.runUpdateChecker(root)

    print("Running window.")

    window.runWindow(root)

    print("Application has finished.")
