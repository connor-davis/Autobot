from os import path
from tkinter.constants import *

import customtkinter as ctk
from pynput import keyboard

from src.scripts.silentShot import *
from src.scripts.slideCancel import *
from src.scripts.yy import *

import src.utils.configFile as configFile
from src.utils.beeper import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.keyboardListener = None
        self.keyboard = keyboard

        self.configuration = configFile.getConfiguration()

        self.silentShotEnabled = self.configuration.getboolean("silentshot", "enabled")
        self.silentShotLethalKey = self.configuration.get("silentshot", "lethalKey")
        self.silentShotWeaponSwapKey = self.configuration.get("silentshot", "weaponSwapKey")
        self.silentShotTimeBefore = self.configuration.get("silentshot", "timeBefore")
        self.silentShotTimeAfter = self.configuration.get("silentshot", "timeAfter")
        self.exitScopeAfterSilentShot = self.configuration.getboolean("silentshot", "exitScope")

        self.slideCancelEnabled = self.configuration.getboolean("slidecancel", "enabled")
        self.slideCancelActivatorKey = self.configuration.get("slidecancel", "activatorKey")
        self.slideCancelSlideKey = self.configuration.get("slidecancel", "slideKey")
        self.slideCancelCancelKey = self.configuration.get("slidecancel", "cancelKey")

        self.yyEnabled = self.configuration.getboolean("yy", "enabled")
        self.yyActivatorKey = self.configuration.get("yy", "activatorKey")
        self.yyWeaponSwapKey = self.configuration.get("yy", "weaponSwapKey")
        self.yyDelay = self.configuration.get("yy", "delay")

        # configure window
        self.title("Autobot v%s" % self.configuration.get("settings", "version"))
        self.iconbitmap(path.join("src", "assets", "logo.ico"))
        self.resizable(False, False)

        self.mainFrame = ctk.CTkFrame(self, fg_color="#191919", corner_radius=0)
        self.tabs = ctk.CTkTabview(self.mainFrame, border_color="#404040", fg_color="#191919", border_width=1)

        self.tabs.add("SS")
        self.tabs.add("SC")
        self.tabs.add("RC")
        self.tabs.add("RF")
        self.tabs.add("AR")
        self.tabs.add("YY")
        self.tabs.add("Settings")

        # Silent Shot

        self.silentShotLabel = ctk.CTkLabel(self.tabs.tab("SS"), text="Silent Shot", text_color="white",
                                            font=("Arial", 16, "bold"))
        self.silentShotLabel.pack()

        self.statusFrame = ctk.CTkFrame(self.tabs.tab("SS"), fg_color="#191919")

        self.silentShotEnabledLabel = ctk.CTkLabel(self.statusFrame, text="Is Enabled?")
        self.silentShotEnabledLabel.pack(side=RIGHT, padx=(0, 5))
        self.silentShotSwitchVar = ctk.StringVar(value="on")

        if self.silentShotEnabled:
            self.silentShotSwitchVar.set("on")
        else:
            self.silentShotSwitchVar.set("off")

        self.slideCancelEnabledSwitch = ctk.CTkSwitch(
            master=self.statusFrame,
            text="",
            command=self.silentShotSwitchEvent,
            variable=self.silentShotSwitchVar,
            onvalue="on",
            offvalue="off"
        )
        self.slideCancelEnabledSwitch.pack(side=LEFT, anchor=W)

        self.statusFrame.pack(fill=X)

        self.silentShotLethalKeyVar = ctk.StringVar(value=self.silentShotLethalKey)

        self.silentShotLethalKeyLabel = ctk.CTkLabel(self.tabs.tab("SS"), text="Lethal Key, e.g. F")
        self.silentShotLethalKeyLabel.pack(pady=(10, 0), padx=5, anchor=W)

        self.silentShotLethalKeyButton = ctk.CTkButton(
            self.tabs.tab("SS"),
            textvariable=self.silentShotLethalKeyVar,
            command=self.getSilentShotLethalKey
        )
        self.silentShotLethalKeyButton.pack(pady=10, padx=5, fill=X)

        self.silentShotWeaponSwapKeyVar = ctk.StringVar(value=self.silentShotWeaponSwapKey)

        self.silentShotWeaponSwapKeyLabel = ctk.CTkLabel(self.tabs.tab("SS"), text="Weapon Swap Key, e.g. 1")
        self.silentShotWeaponSwapKeyLabel.pack(padx=5, anchor=W)

        self.silentShotWeaponSwapKeyButton = ctk.CTkButton(
            self.tabs.tab("SS"),
            textvariable=self.silentShotWeaponSwapKeyVar,
            command=self.getSilentShotWeaponSwapKey
        )
        self.silentShotWeaponSwapKeyButton.pack(pady=10, padx=5, fill=X)

        self.silentShotTimeBeforeVar = ctk.StringVar(value=self.silentShotTimeBefore)

        self.silentShotTimeBeforeLabel = ctk.CTkLabel(self.tabs.tab("SS"), text="Time Before, e.g. 1")
        self.silentShotTimeBeforeLabel.pack(padx=5, pady=(0, 5), anchor=W)

        self.silentShotTimeBeforeEntry = ctk.CTkEntry(
            self.tabs.tab("SS"),
            textvariable=self.silentShotTimeBeforeVar,
            fg_color="#171717",
            border_width=1,
            border_color="#404040",
            corner_radius=5
        )
        self.silentShotTimeBeforeEntry.pack(padx=5, pady=(0, 5), fill=X)

        self.silentShotTimeAfterVar = ctk.StringVar(value=self.silentShotTimeAfter)

        self.silentShotTimeAfterLabel = ctk.CTkLabel(self.tabs.tab("SS"), text="Time After, e.g. 140")
        self.silentShotTimeAfterLabel.pack(padx=5, pady=(0, 5), anchor=W)

        self.silentShotTimeAfterEntry = ctk.CTkEntry(
            self.tabs.tab("SS"),
            textvariable=self.silentShotTimeAfterVar,
            fg_color="#171717",
            border_width=1,
            border_color="#404040",
            corner_radius=5
        )
        self.silentShotTimeAfterEntry.pack(padx=5, pady=(0, 5), fill=X)

        self.silentShotExitScopeSwitchVar = ctk.StringVar(value="on")

        if self.exitScopeAfterSilentShot:
            self.silentShotExitScopeSwitchVar.set("on")
        else:
            self.silentShotExitScopeSwitchVar.set("off")

        self.slideCancelEnabledSwitch = ctk.CTkSwitch(
            master=self.tabs.tab("SS"),
            text="Exit scope after silent shot?",
            command=self.silentShotExitScopeSwitchEvent,
            variable=self.silentShotExitScopeSwitchVar,
            onvalue="on",
            offvalue="off"
        )
        self.slideCancelEnabledSwitch.pack(side=LEFT, anchor=W)

        # Slide Cancel

        self.slideCancelLabel = ctk.CTkLabel(
            self.tabs.tab("SC"),
            text="Slide Cancel",
            text_color="white",
            font=("Arial", 16, "bold")
        )
        self.slideCancelLabel.pack()

        self.slideCancelStatusFrame = ctk.CTkFrame(self.tabs.tab("SC"), fg_color="#191919")

        self.slideCancelEnabledLabel = ctk.CTkLabel(self.slideCancelStatusFrame, text="Is Enabled?")
        self.slideCancelEnabledLabel.pack(side=RIGHT, padx=(0, 5))
        self.slideCancelSwitchVar = ctk.StringVar(value="on")

        if self.silentShotEnabled:
            self.slideCancelSwitchVar.set("on")
        else:
            self.slideCancelSwitchVar.set("off")

        self.slideCancelEnabledSwitch = ctk.CTkSwitch(
            master=self.slideCancelStatusFrame,
            text="",
            command=self.slideCancelSwitchEvent,
            variable=self.slideCancelSwitchVar,
            onvalue="on",
            offvalue="off"
        )
        self.slideCancelEnabledSwitch.pack(side=LEFT, anchor=W)

        self.slideCancelStatusFrame.pack(fill=X)

        self.slideCancelActivatorKeyVar = ctk.StringVar(value=self.slideCancelActivatorKey)

        self.slideCancelActivatorKeyLabel = ctk.CTkLabel(self.tabs.tab("SC"), text="Activator Key, e.g. c")
        self.slideCancelActivatorKeyLabel.pack(padx=5, anchor=W)

        self.slideCancelActivatorKeyButton = ctk.CTkButton(
            self.tabs.tab("SC"),
            textvariable=self.slideCancelActivatorKeyVar,
            command=self.getSlideCancelActivatorKey
        )
        self.slideCancelActivatorKeyButton.pack(pady=10, padx=5, fill=X)

        self.slideCancelSlideKeyVar = ctk.StringVar(value=self.slideCancelSlideKey)

        self.slideCancelSlideKeyLabel = ctk.CTkLabel(self.tabs.tab("SC"), text="Slide Key, e.g. c")
        self.slideCancelSlideKeyLabel.pack(padx=5, anchor=W)

        self.slideCancelSlideKeyButton = ctk.CTkButton(
            self.tabs.tab("SC"),
            textvariable=self.slideCancelSlideKeyVar,
            command=self.getSlideCancelSlideKey
        )
        self.slideCancelSlideKeyButton.pack(pady=10, padx=5, fill=X)

        self.slideCancelCancelKeyVar = ctk.StringVar(value=self.slideCancelCancelKey)

        self.slideCancelCancelKeyLabel = ctk.CTkLabel(self.tabs.tab("SC"), text="Cancel Key, e.g. space")
        self.slideCancelCancelKeyLabel.pack(padx=5, anchor=W)

        self.slideCancelCancelKeyButton = ctk.CTkButton(
            self.tabs.tab("SC"),
            textvariable=self.slideCancelCancelKeyVar,
            command=self.getSlideCancelCancelKey
        )
        self.slideCancelCancelKeyButton.pack(pady=10, padx=5, fill=X)

        # Rechamber Cancel

        self.rechamberCancelLabel = ctk.CTkLabel(self.tabs.tab("RC"), text="Rechamber Cancel", text_color="white",
                                                 font=("Arial", 16, "bold"))
        self.rechamberCancelLabel.pack()

        self.rechamberCancelDescription = ctk.CTkLabel(self.tabs.tab("RC"), text="Rechamber Cancel not available yet.",
                                                       text_color="white",
                                                       font=("Arial", 12))
        self.rechamberCancelDescription.pack()

        # Rapid Fire

        self.rapidFireLabel = ctk.CTkLabel(self.tabs.tab("RF"), text="Rapid Fire", text_color="white",
                                           font=("Arial", 16, "bold"))
        self.rapidFireLabel.pack()

        self.rapidFireDescription = ctk.CTkLabel(self.tabs.tab("RF"), text="Rapid Fire not available yet.",
                                                 text_color="white",
                                                 font=("Arial", 12))
        self.rapidFireDescription.pack()

        # Anti-Recoil

        self.antiRecoilLabel = ctk.CTkLabel(self.tabs.tab("AR"), text="Anti-Recoil", text_color="white",
                                           font=("Arial", 16, "bold"))
        self.antiRecoilLabel.pack()

        self.antiRecoilDescription = ctk.CTkLabel(
             self.tabs.tab("AR"),
             text="Anti-Recoil not available yet.",
             text_color="white",
             font=("Arial", 12)
        )
        self.antiRecoilDescription.pack()

        # YY

        self.yyLabel = ctk.CTkLabel(
            self.tabs.tab("YY"),
            text="YY",
            text_color="white",
            font=("Arial", 16, "bold")
        )
        self.yyLabel.pack()

        self.yyStatusFrame = ctk.CTkFrame(self.tabs.tab("YY"), fg_color="#191919")

        self.yyEnabledLabel = ctk.CTkLabel(self.yyStatusFrame, text="Is Enabled?")
        self.yyEnabledLabel.pack(side=RIGHT, padx=(0, 5))

        self.yyEnabledSwitchVar = ctk.StringVar(value="on")

        if self.yyEnabled:
            self.yyEnabledSwitchVar.set("on")
        else:
            self.yyEnabledSwitchVar.set("off")

        self.yyEnabledSwitch = ctk.CTkSwitch(
            master=self.yyStatusFrame,
            text="",
            command=self.yySwitchEvent,
            variable=self.yyEnabledSwitchVar,
            onvalue="on",
            offvalue="off"
        )
        self.yyEnabledSwitch.pack(side=LEFT, anchor=W)

        self.yyStatusFrame.pack(fill=X)

        self.yyActivatorKeyVar = ctk.StringVar(value=self.yyActivatorKey)

        self.yyActivatorKeyLabel = ctk.CTkLabel(self.tabs.tab("YY"), text="Activator Key, e.g. e")
        self.yyActivatorKeyLabel.pack(padx=5, anchor=W)

        self.yyActivatorKeyButton = ctk.CTkButton(
            self.tabs.tab("YY"),
            textvariable=self.yyActivatorKeyVar,
            command=self.getYYActivatorKey
        )
        self.yyActivatorKeyButton.pack(pady=10, padx=5, fill=X)

        self.yyWeaponSwapKeyVar = ctk.StringVar(value=self.yyWeaponSwapKey)

        self.yyWeaponSwapKeyLabel = ctk.CTkLabel(self.tabs.tab("YY"), text="Weapon Swap Key, e.g. 1")
        self.yyWeaponSwapKeyLabel.pack(padx=5, anchor=W)

        self.yyWeaponSwapKeyButton = ctk.CTkButton(
            self.tabs.tab("YY"),
            textvariable=self.yyWeaponSwapKeyVar,
            command=self.getYYWeaponSwapKey
        )
        self.yyWeaponSwapKeyButton.pack(pady=10, padx=5, fill=X)

        self.yyDelayVar = ctk.StringVar(value=self.yyDelay)

        self.yyDelayLabel = ctk.CTkLabel(self.tabs.tab("YY"), text="Delay, e.g. 100")
        self.yyDelayLabel.pack(padx=5, pady=(0, 5), anchor=W)

        self.yyDelayEntry = ctk.CTkEntry(
            self.tabs.tab("YY"),
            textvariable=self.yyDelayVar,
            fg_color="#171717",
            border_width=1,
            border_color="#404040",
            corner_radius=5
        )
        self.yyDelayEntry.pack(padx=5, pady=(0, 5), fill=X)

        # Settings

        self.targetGameLabel = ctk.CTkLabel(self.tabs.tab("Settings"), text="Target Game", text_color="white")
        self.targetGameLabel.pack(anchor=W)
        self.optionMenuOne = ctk.CTkOptionMenu(
            self.tabs.tab("Settings"),
            dynamic_resizing=True,
            values=["Modern Warfare", "Modern Warfare 2"]
        )
        self.optionMenuOne.pack(fill=X)

        self.appVersion = ctk.CTkLabel(self.tabs.tab("Settings"),
                                       text="Autobot Version: %s" % self.configuration.get("settings", "version"),
                                       text_color="white")
        self.appVersion.pack(side=BOTTOM)

        self.tabs.pack(padx=5, pady=5)

        self.applyChangesButton = ctk.CTkButton(self.mainFrame, text="Apply Changes", command=self.applyChanges)
        self.applyChangesButton.pack(padx=5, pady=(0, 5), expand=True, fill=X)

        self.mainFrame.pack()

    def getSilentShotLethalKey(self):
        self.silentShotLethalKeyButton.focus()

        if self.keyboardListener is not None:
            self.keyboardListener = None

        self.keyboardListener = self.keyboard.Listener(on_press=self.handleSilentShotLethalKeyPress)
        self.keyboardListener.start()

    def handleSilentShotLethalKeyPress(self, key):
        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        self.silentShotLethalKeyVar.set(keyBind)

        self.update_idletasks()
        self.update()

        self.keyboardListener.stop()

    def getSilentShotWeaponSwapKey(self):
        self.silentShotWeaponSwapKeyButton.focus()

        if self.keyboardListener is not None:
            self.keyboardListener = None

        self.keyboardListener = self.keyboard.Listener(on_press=self.handleSilentShotWeaponSwapKeyPress)
        self.keyboardListener.start()

    def handleSilentShotWeaponSwapKeyPress(self, key):
        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        self.silentShotWeaponSwapKeyVar.set(keyBind)

        self.update_idletasks()
        self.update()

        self.keyboardListener.stop()

    def silentShotSwitchEvent(self):
        self.configuration = configFile.getConfiguration()

        if self.silentShotSwitchVar.get() == "on":
            self.configuration.set("silentshot", "enabled", '1')
            initializeSilentShot()
            beep(200, 100)
            beep(200, 100)
            print("Silent shot enabled.")
        else:
            self.configuration.set("silentshot", "enabled", '0')
            uninitializeSilentShot()
            beep(200, 100)
            print("Silent shot disabled.")

        with open("data/configuration.yml", "w") as config:
            self.configuration.write(config)

            config.flush()
            config.close()

    def silentShotExitScopeSwitchEvent(self):
        self.configuration = configFile.getConfiguration()

        if self.silentShotExitScopeSwitchVar.get() == "on":
            self.configuration.set("silentshot", "exitScope", '1')
        else:
            self.configuration.set("silentshot", "exitScope", '0')

        with open("data/configuration.yml", "w") as config:
            self.configuration.write(config)

            config.flush()
            config.close()

    def getSlideCancelActivatorKey(self):
        if self.keyboardListener is not None:
            self.keyboardListener = None

        self.keyboardListener = self.keyboard.Listener(on_press=self.handleSlideCancelActivatorKeyPress)
        self.keyboardListener.start()

    def handleSlideCancelActivatorKeyPress(self, key):
        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        self.slideCancelActivatorKeyVar.set(keyBind)

        self.update_idletasks()
        self.update()

        self.keyboardListener.stop()

    def getSlideCancelSlideKey(self):
        if self.keyboardListener is not None:
            self.keyboardListener = None

        self.keyboardListener = self.keyboard.Listener(on_press=self.handleSlideCancelSlideKeyPress)
        self.keyboardListener.start()

    def handleSlideCancelSlideKeyPress(self, key):
        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        self.slideCancelSlideKeyVar.set(keyBind)

        self.update_idletasks()
        self.update()

        self.keyboardListener.stop()

    def getSlideCancelCancelKey(self):
        if self.keyboardListener is not None:
            self.keyboardListener = None

        self.keyboardListener = self.keyboard.Listener(on_press=self.handleSlideCancelCancelKeyPress)
        self.keyboardListener.start()

    def handleSlideCancelCancelKeyPress(self, key):
        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        self.slideCancelCancelKeyVar.set(keyBind)

        self.update_idletasks()
        self.update()

        self.keyboardListener.stop()

    def slideCancelSwitchEvent(self):
        self.configuration = configFile.getConfiguration()

        if self.slideCancelSwitchVar.get() == "on":
            self.configuration.set("slidecancel", "enabled", '1')
            initializeSlideCancel()
            beep(200, 100)
            beep(200, 100)
        else:
            self.configuration.set("slidecancel", "enabled", '0')
            uninitializeSlideCancel()
            beep(200, 100)

        with open("data/configuration.yml", "w") as config:
            self.configuration.write(config)

            config.flush()
            config.close()

    def getYYActivatorKey(self):
        if self.keyboardListener is not None:
            self.keyboardListener = None

        self.keyboardListener = self.keyboard.Listener(on_press=self.handleYYActivatorKeyPress)
        self.keyboardListener.start()

    def handleYYActivatorKeyPress(self, key):
        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        self.yyActivatorKeyVar.set(keyBind)

        self.update_idletasks()
        self.update()

        self.keyboardListener.stop()

    def getYYWeaponSwapKey(self):
        if self.keyboardListener is not None:
            self.keyboardListener = None

        self.keyboardListener = self.keyboard.Listener(on_press=self.handleYYWeaponSwapKeyPress)
        self.keyboardListener.start()

    def handleYYWeaponSwapKeyPress(self, key):
        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        self.yyWeaponSwapKeyVar.set(keyBind)

        self.update_idletasks()
        self.update()

        self.keyboardListener.stop()

    def yySwitchEvent(self):
        self.configuration = configFile.getConfiguration()

        if self.yyEnabledSwitchVar.get() == "on":
            self.configuration.set("yy", "enabled", '1')
            initializeYY()
            beep(200, 100)
            beep(200, 100)
        else:
            self.configuration.set("yy", "enabled", '0')
            uninitializeYY()
            beep(200, 100)

        with open("data/configuration.yml", "w") as config:
            self.configuration.write(config)

            config.flush()
            config.close()

    def toggleExitScope(self):
        if self.exitScopeAfterSilentShot:
            self.exitScopeAfterSilentShot = False
        else:
            self.exitScopeAfterSilentShot = True

    def applyChanges(self):
        self.configuration = configFile.getConfiguration()

        self.configuration.set("silentshot", "enabled", self.silentShotSwitchVar.get() == "on")
        self.configuration.set("silentshot", "lethalKey", self.silentShotLethalKeyVar.get())
        self.configuration.set("silentshot", "weaponSwapKey", self.silentShotWeaponSwapKeyVar.get())
        self.configuration.set("silentshot", "timeBefore", self.silentShotTimeBeforeVar.get())
        self.configuration.set("silentshot", "timeAfter", self.silentShotTimeAfterVar.get())
        self.configuration.set("silentshot", "exitScope", self.silentShotExitScopeSwitchVar.get() == "on")

        self.configuration.set("slidecancel", "enabled", self.slideCancelSwitchVar.get() == "on")
        self.configuration.set("slidecancel", "activatorKey", self.slideCancelActivatorKeyVar.get())
        self.configuration.set("slidecancel", "slideKey", self.slideCancelSlideKeyVar.get())
        self.configuration.set("slidecancel", "cancelKey", self.slideCancelCancelKeyVar.get())

        self.configuration.set("yy", "enabled", self.yyEnabledSwitchVar.get() == "on")
        self.configuration.set("yy", "activatorKey", self.yyActivatorKeyVar.get())
        self.configuration.set("yy", "weaponSwapKey", self.yyWeaponSwapKeyVar.get())
        self.configuration.set("yy", "delay", self.yyDelayVar.get())

        if self.optionMenuOne.get() == "Modern Warfare":
            self.configuration.set("settings", "targetGame", "Modern Warfare")
        else:
            self.configuration.set("settings", "targetGame", "HQ")

        with open("data/configuration.yml", "w") as config:
            self.configuration.write(config)

            config.flush()
            config.close()

        print("Uninitializing scripts.")

        if self.configuration.get("silentshot", "enabled") == "0":
            uninitializeSilentShot()

        if self.configuration.get("slidecancel", "enabled") == "0":
            uninitializeSlideCancel()

        if self.configuration.get("yy", "enabled") == "0":
            uninitializeYY()

        print("Initializing scripts.")

        if self.configuration.get("silentshot", "enabled") == "1":
            initializeSilentShot()

        if self.configuration.get("slidecancel", "enabled") == "1":
            initializeSlideCancel()

        if self.configuration.get("yy", "enabled") == "1":
            initializeYY()

        self.update_idletasks()
        self.update()