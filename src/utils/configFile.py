import configparser
from os import path

configFile = configparser.ConfigParser()

if not path.exists("data/configuration.ini"):
    configFile.add_section("silentshot")

    configFile.set("silentshot", "lethalKey", "j")
    configFile.set("silentshot", "weaponSwapKey", "1")
    configFile.set("silentshot", "timeBefore", "1")
    configFile.set("silentshot", "timeAfter", "140")
    configFile.set("silentshot", "exitScope", "1")
    configFile.set("silentshot", "enabled", "0")

    configFile.add_section("slidecancel")

    configFile.set("slidecancel", "activatorKey", "c")
    configFile.set("slidecancel", "slideKey", "c")
    configFile.set("slidecancel", "cancelKey", "space")
    configFile.set("slidecancel", "enabled", "0")

    configFile.add_section("settings")

    configFile.set("settings", "targetGame", "Modern Warfare")
    configFile.set("settings", "theme", "darkly")
    configFile.set("settings", "version", "0.1.2")

    with open(r"data/configuration.ini", 'w') as configfileObj:
        configFile.write(configfileObj)
        configfileObj.flush()
        configfileObj.close()

def getConfiguration():
    config = configparser.ConfigParser()
    config.read('data/configuration.ini')

    return config