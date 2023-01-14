import configparser
from os import path

import yaml

configFile = configparser.ConfigParser()

if not path.exists("data/configuration.yml"):
    configuration = {
                "silentshot": {
                    "enabled": "0",
                    "lethalKey": "j",
                    "weaponSwapKey": "1",
                    "timeBefore": "1",
                    "timeAfter": "60",
                    "exitScope": "0"
                },
                "slidecancel": {
                    "enabled": "0",
                    "activatorKey": "c",
                    "slideKey": "c",
                    "cancelKey": "space"
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

    stream = open('data/configuration.yml', 'w')
    yaml.dump(configuration, stream)
    stream.flush()
    stream.close()


class YamlConfig:
    def __init__(self, data):
        self.data = data

        if self.data is None:
            self.data = {
                "silentshot": {
                    "enabled": "0",
                    "lethalKey": "j",
                    "weaponSwapKey": "1",
                    "timeBefore": "1",
                    "timeAfter": "60",
                    "exitScope": "0"
                },
                "slidecancel": {
                    "enabled": "0",
                    "activatorKey": "c",
                    "slideKey": "c",
                    "cancelKey": "space"
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

    def sectionExists(self, section):
        if section not in self.data:
            return False
        else:
            return True

    def keyExists(self, section, key):
        if key not in self.data[section]:
            return False
        else:
            return True

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


def testConfiguration():
    localConfiguration = getConfiguration()

    required = {
        "silentshot": {
            "enabled": "0",
            "lethalKey": "j",
            "weaponSwapKey": "1",
            "timeBefore": "1",
            "timeAfter": "60",
            "exitScope": "0"
        },
        "slidecancel": {
            "enabled": "0",
            "activatorKey": "c",
            "slideKey": "c",
            "cancelKey": "space"
        },
        "yy": {
            "enabled": "0",
            "activatorKey": "e",
            "weaponSwapKey": "1",
            "delay": "100"
        }
    }

    for section in required:
        if not localConfiguration.sectionExists(section.lower()):
            print("Section does not exist, creating %s " % section)

            for key in required[section.lower()]:
                localConfiguration.set(section.lower(), required[section.lower()], required[section][key])
        else:
            for key in required[section.lower()]:
                print("key does not exist, creating %s " % key)

                if not localConfiguration.keyExists(section.lower(), key):
                    localConfiguration.set(section.lower(), required[section.lower()], required[section][key])

    with open("data/configuration.yml", "w") as file:
        localConfiguration.write(file)
        file.flush()
        file.close()


def getConfiguration():
    f = open('data/configuration.yml', 'r')
    yamlConfig = yaml.load(f.read(), yaml.CLoader)
    f.flush()
    f.close()

    return YamlConfig(yamlConfig)
