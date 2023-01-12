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

    return YamlConfig(yamlConfig)
