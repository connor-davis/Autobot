import configparser
import time
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
            "version": "0.2.0"
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
                    "version": "0.2.0"
                }
            }

    def sectionExists(self, section):
        try:
            return section not in self.data
        except KeyError:
            return False

    def keyExists(self, section, key):
        try:
            return key not in self.data[section]
        except KeyError:
            return False

    def get(self, section, key):
        if section in self.data:
            return self.data[section][key]
        else:
            return False

    def getboolean(self, section, key):
        if section in self.data:
            return self.data[section][key] == "1" or self.data[section][key] is True
        else:
            return False

    def getint(self, section, key):
        if section in self.data:
            return int(self.data[section][key])
        else:
            return False

    def set(self, section, key, value):
        self.data[section][key] = value

    def write(self, f):
        yaml.dump(self.data, f)


def testConfiguration():
    f = open('data/configuration.yml', 'r')
    yamlConfig = yaml.load(f.read(), yaml.CLoader)
    f.flush()
    f.close()

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
        },
        "settings": {
            "targetGame": "Modern Warfare",
            "version": "0.2.0"
        }
    }

    for sectionName in required:

        if sectionName not in yamlConfig:
            print(sectionName)

            yamlConfig[sectionName] = {}

            for keyName in required[sectionName]:
                yamlConfig[sectionName][keyName] = required[sectionName][keyName]
        else:
            for keyName in required[sectionName]:
                if keyName not in yamlConfig[sectionName]:
                    print(keyName)

                    yamlConfig[sectionName][keyName] = required[sectionName][keyName]

    with open("data/configuration.yml", "w") as file:
        yaml.dump(yamlConfig, file)
        file.flush()
        file.close()


def getConfiguration():
    f = open('data/configuration.yml', 'r')
    yamlConfig = yaml.load(f.read(), yaml.CLoader)
    f.flush()
    f.close()

    return YamlConfig(yamlConfig)
