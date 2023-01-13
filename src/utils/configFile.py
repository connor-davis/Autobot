import configparser
from os import path

import yaml

configFile = configparser.ConfigParser()

if not path.exists("data/configuration.yml"):
    configuration = {
        "silentshot": {
            "lethalKey": "j",
            "weaponSwapKey": "1",
            "timeBefore": "1",
            "timeAfter": "30",
            "exitScope": "1",
            "enabled": "0"
        },
        "slidecancel": {
            "activatorKey": "c",
            "slideKey": "c",
            "cancelKey": "space",
            "enabled": "0"
        },
        "settings": {
            "targetGame": "Modern Warfare",
            "theme": "darkly",
            "version": "0.1.4"
        }
    }

    stream = open('data/configuration.yml', 'w')
    yaml.dump(configuration, stream)
    stream.flush()
    stream.close()


class YamlConfig:
    def __init__(self, data):
        self.data = data

    def get(self, section, key):
        return self.data[section][key]

    def getboolean(self, section, key):
        return self.data[section][key] == "1" or self.data[section][key] is True

    def getint(self, section, key):
        return int(self.data[section][key])

    def set(self, section, key, value):
        self.data[section][key] = value

    def write(self, f):
        yaml.dump(self.data, f)


def getConfiguration():
    f = open('data/configuration.yml', 'r')
    yamlConfig = yaml.load(f.read(), yaml.CLoader)
    f.flush()
    f.close()

    if yamlConfig is None:
        yamlConfig = {
            "silentshot": {
                "lethalKey": "j",
                "weaponSwapKey": "1",
                "timeBefore": "1",
                "timeAfter": "30",
                "exitScope": "1",
                "enabled": "0"
            },
            "slidecancel": {
                "activatorKey": "c",
                "slideKey": "c",
                "cancelKey": "space",
                "enabled": "0"
            },
            "yy": {
                "enabled": "0",
                "activatorKey": "e",
                "weaponSwapKey": "1",
                "delay": "100"
            },
            "settings": {
                "targetGame": "Modern Warfare",
                "version": "0.1.9"
            }
        }

        try:
            print("YY Enabled: %s" % yamlConfig["slidecancel"]["enabled"])
        except TypeError:
            yamlConfig["silentshot"]["enabled"] = "0"
            yamlConfig["silentshot"]["lethalKey"] = "j"
            yamlConfig["silentshot"]["weaponSwapKey"] = "1"
            yamlConfig["silentshot"]["timeBefore"] = "1"
            yamlConfig["silentshot"]["timeAfter"] = "60"
            yamlConfig["silentshot"]["exitScope"] = "0"

        try:
            print("YY Enabled: %s" % yamlConfig["slidecancel"]["enabled"])
        except TypeError:
            yamlConfig["slidecancel"]["enabled"] = "0"
            yamlConfig["slidecancel"]["activatorKey"] = "c"
            yamlConfig["slidecancel"]["slideKey"] = "c"
            yamlConfig["slidecancel"]["cancelKey"] = "space"

        try:
            print("YY Enabled: %s" % yamlConfig["yy"]["enabled"])
        except TypeError:
            yamlConfig["yy"]["enabled"] = "0"
            yamlConfig["yy"]["activatorKey"] = "e"
            yamlConfig["yy"]["weaponSwapKey"] = "1"
            yamlConfig["yy"]["delay"] = "100"

        try:
            print("Autobot Version: v%s" % yamlConfig["settings"]["version"])
        except TypeError:
            yamlConfig["yy"]["targetGame"] = "Modern Warfare"
            yamlConfig["yy"]["version"] = "0.1.9"

        return YamlConfig(yamlConfig)
