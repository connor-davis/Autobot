from os import path
from tkinter.constants import *

import customtkinter as ctk
from pynput import keyboard

from src.scripts.silentShot import *
from src.scripts.slideCancel import *

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
            text="Rapid Fire",
            text_color="white",
            font=("Arial", 16, "bold")
        )
        self.yyLabel.pack()

        self.yyDescription = ctk.CTkLabel(
            self.tabs.tab("YY"),
            text="YY not available yet.",
            text_color="white",
            font=("Arial", 12)
        )
        self.yyDescription.pack()

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

        if self.optionMenuOne.get() == "Modern Warfare":
            self.configuration.set("settings", "targetGame", "Modern Warfare")
        else:
            self.configuration.set("settings", "targetGame", "HQ")

        with open("data/configuration.yml", "w") as config:
            self.configuration.write(config)

            config.flush()
            config.close()

        print("Uninitializing scripts.")

        if self.configuration.get("silentshot", "enabled") == "1":
            uninitializeSilentShot()

        if self.configuration.get("slidecancel", "enabled") == "1":
            uninitializeSlideCancel()

        print("Initializing scripts.")

        if self.configuration.get("silentshot", "enabled") == "1":
            initializeSilentShot()

        if self.configuration.get("slidecancel", "enabled") == "1":
            initializeSlideCancel()

        self.update_idletasks()
        self.update()

#
#
# job = None
# listenerKeyboard = None
# entrySilentShotLethalKey = None
#
#
# def runMainWindow(root):
#     global entrySilentShotLethalKey
#
#     labelHeading = ttb.Label(text="Autobot Macros", font=("Impact", 24))
#     labelHeading.pack(pady=10, padx=10)
#
#     labelDescription = ttb.Label(
#         text="Autobot Macros help you with lazily performing the silent shot and slide cancel.",
#         font="Arial", wraplength=400)
#     labelDescription.pack(pady=5, padx=5)
#
#     notebookConfiguration = ttb.Notebook(root)
#
#     frameSilentShot = ttb.Frame(notebookConfiguration, padding=5)
#
#     labelSilentShotLethalKey = ttb.Label(master=frameSilentShot, text="Lethal Key, e.g. f")
#     labelSilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5)
#
#     btnSilentShotLethalKeyText = StringVar()
#
#     def getLethalKey():
#         global listenerKeyboard
#
#         if listenerKeyboard is not None:
#             listenerKeyboard = None
#
#         listenerKeyboard = keyboard.Listener(on_press=handleLethalPress)
#         listenerKeyboard.start()
#
#     def handleLethalPress(key):
#         global listenerKeyboard, job
#
#         keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")
#
#         btnSilentShotLethalKeyText.set(keyBind)
#
#         root.update_idletasks()
#         root.update()
#
#         listenerKeyboard.stop()
#
#     btnSilentShotLethalKeyText.set(silentShotLethalKey)
#     entrySilentShotLethalKey = ttb.Button(master=frameSilentShot, style="success-outline",
#                                           textvariable=btnSilentShotLethalKeyText, command=getLethalKey)
#     entrySilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5, anchor=W)
#
#     labelSilentShotWeaponSwap = ttb.Label(master=frameSilentShot, text="Weapon Swap Key, e.g. 1")
#     labelSilentShotWeaponSwap.pack(fill=X, expand=True, pady=5, padx=5)
#
#     btnSilentShotWeaponSwapKeyText = StringVar()
#
#     def getWeaponSwapKey():
#         global listenerKeyboard
#
#         if listenerKeyboard is not None:
#             listenerKeyboard = None
#
#         listenerKeyboard = keyboard.Listener(on_press=handleWeaponSwapPress)
#         listenerKeyboard.start()
#
#     def handleWeaponSwapPress(key):
#         global listenerKeyboard
#
#         keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")
#
#         btnSilentShotWeaponSwapKeyText.set(keyBind)
#
#         root.update_idletasks()
#         root.update()
#
#         listenerKeyboard.stop()
#         listenerKeyboard = None
#
#     btnSilentShotWeaponSwapKeyText.set(silentShotWeaponSwapKey)
#     entrySilentShotWeaponSwapKey = ttb.Button(master=frameSilentShot, style="success-outline",
#                                               textvariable=btnSilentShotWeaponSwapKeyText, command=getWeaponSwapKey)
#     entrySilentShotWeaponSwapKey.pack(fill=X, expand=True, pady=5, padx=5, anchor=W)
#
#     labelSilentShotLethalKey = ttb.Label(master=frameSilentShot, text="Time Before Lethal (milliseconds)")
#     labelSilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5)
#
#     entryTimeBeforeLethal = ttb.Entry(master=frameSilentShot, style="success")
#     entryTimeBeforeLethal.insert(0, silentShotTimeBefore)
#     entryTimeBeforeLethal.pack(fill=X, expand=True, pady=5, padx=5)
#
#     labelSilentShotLethalKey = ttb.Label(master=frameSilentShot, text="Time After Lethal (milliseconds)")
#     labelSilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5)
#
#     entryTimeAfterLethal = ttb.Entry(master=frameSilentShot, style="success")
#     entryTimeAfterLethal.insert(0, silentShotTimeAfter)
#     entryTimeAfterLethal.pack(fill=X, expand=True, pady=5, padx=5)
#
#     checkboxValue = IntVar()
#
#     if exitScopeAfterSilentShot:
#         checkboxValue.set(1)
#     else:
#         checkboxValue.set(0)
#
#     checkboxExitScope = ttb.Checkbutton(master=frameSilentShot,
#                                         text="Exit scope after silent shot?", command=toggleExitScope,
#                                         variable=checkboxValue, onvalue=1, offvalue=0,
#                                         bootstyle="success-rounded-toggle")
#     checkboxExitScope.pack(fill=X, expand=True, pady=5, padx=5)
#
#     frameSilentShot.pack(expand=True, fill=BOTH, pady=5, padx=5)
#
#     frameSlideCancel = ttb.Frame(notebookConfiguration, padding=5)
#
#     labelSlideCancelActivator = ttb.Label(master=frameSlideCancel, text="Activator Key, e.g. c")
#     labelSlideCancelActivator.pack(fill=X, pady=5, padx=5)
#
#     btnSlideCancelActivatorKeyText = StringVar()
#
#     def getActivatorKey():
#         global listenerKeyboard
#
#         if listenerKeyboard is not None:
#             listenerKeyboard = None
#
#         listenerKeyboard = keyboard.Listener(on_press=handleActivatorPress)
#         listenerKeyboard.start()
#
#     def handleActivatorPress(key):
#         global listenerKeyboard, job
#
#         keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")
#
#         btnSlideCancelActivatorKeyText.set(keyBind)
#
#         root.update_idletasks()
#         root.update()
#
#         listenerKeyboard.stop()
#
#     btnSlideCancelActivatorKeyText.set(slideCancelActivatorKey)
#     btnSlideCancelActivator = ttb.Button(master=frameSlideCancel, style="success-outline",
#                                          textvariable=btnSlideCancelActivatorKeyText, command=getActivatorKey)
#     btnSlideCancelActivator.pack(fill=X, pady=5, padx=5)
#
#     labelSlideCancelSlide = ttb.Label(master=frameSlideCancel, text="Slide Key, e.g. c")
#     labelSlideCancelSlide.pack(fill=X, pady=5, padx=5)
#
#     btnSlideCancelSlideKeyText = StringVar()
#
#     def getSlideKey():
#         global listenerKeyboard
#
#         if listenerKeyboard is not None:
#             listenerKeyboard = None
#
#         listenerKeyboard = keyboard.Listener(on_press=handleSidePress)
#         listenerKeyboard.start()
#
#     def handleSidePress(key):
#         global listenerKeyboard, job
#
#         keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")
#
#         btnSlideCancelSlideKeyText.set(keyBind)
#
#         root.update_idletasks()
#         root.update()
#
#         listenerKeyboard.stop()
#
#     btnSlideCancelSlideKeyText.set(slideCancelSlideKey)
#     btnSlideCancelSlide = ttb.Button(master=frameSlideCancel, style="success-outline",
#                                      textvariable=btnSlideCancelSlideKeyText, command=getSlideKey)
#     btnSlideCancelSlide.pack(fill=X, pady=5, padx=5)
#
#     labelSlideCancelCancel = ttb.Label(master=frameSlideCancel, text="Cancel Key, e.g. space")
#     labelSlideCancelCancel.pack(fill=X, pady=5, padx=5)
#
#     btnSlideCancelCancelKeyText = StringVar()
#
#     def getCancelKey():
#         global listenerKeyboard
#
#         if listenerKeyboard is not None:
#             listenerKeyboard = None
#
#         listenerKeyboard = keyboard.Listener(on_press=handleCancelPress)
#         listenerKeyboard.start()
#
#     def handleCancelPress(key):
#         global listenerKeyboard, job
#
#         keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")
#
#         btnSlideCancelCancelKeyText.set(keyBind)
#
#         root.update_idletasks()
#         root.update()
#
#         listenerKeyboard.stop()
#
#     btnSlideCancelCancelKeyText.set(slideCancelCancelKey)
#     btnSlideCancelCancel = ttb.Button(master=frameSlideCancel, style="success-outline",
#                                       textvariable=btnSlideCancelCancelKeyText, command=getCancelKey)
#     btnSlideCancelCancel.pack(fill=X, pady=5, padx=5)
#
#     frameSlideCancel.pack(expand=True, fill=BOTH, pady=5, padx=5)
#
#     frameSettings = ttb.Frame(notebookConfiguration, padding=5)
#
#     targetGameLabel = ttb.Label(master=frameSettings, text="Target Game")
#     targetGameLabel.pack(fill=X, pady=5, padx=5)
#
#     targetGameCombobox = ttb.Combobox(master=frameSettings, values=['Modern Warfare', 'Modern Warfare 2'],
#                                       bootstyle="success")
#
#     if targetGame == "Modern Warfare":
#         targetGameCombobox.current(0)
#
#         btnSlideCancelActivator.configure(state="success")
#         btnSlideCancelSlide.configure(state="success")
#         btnSlideCancelCancel.configure(state="success")
#     elif targetGame == "HQ":
#         targetGameCombobox.current(1)
#
#         btnSlideCancelActivator.configure(state="disabled")
#         btnSlideCancelSlide.configure(state="disabled")
#         btnSlideCancelCancel.configure(state="disabled")
#     else:
#         targetGameCombobox.current(0)
#
#         btnSlideCancelActivator.configure(state="success")
#         btnSlideCancelSlide.configure(state="success")
#         btnSlideCancelCancel.configure(state="success")
#
#     targetGameCombobox.pack(fill=X, pady=5, padx=5)
#
#     themeLabel = ttb.Label(master=frameSettings, text="App Theme")
#     themeLabel.pack(fill=X, pady=5, padx=5)
#
#     themeCombobox = ttb.Combobox(master=frameSettings, values=["darkly", "vapor", "flatly", "pulse"],
#                                  bootstyle="success")
#
#     if theme == "darkly":
#         themeCombobox.current(0)
#     elif theme == "vapor":
#         themeCombobox.current(1)
#     elif theme == "flatly":
#         themeCombobox.current(2)
#     elif theme == "pulse":
#         themeCombobox.current(3)
#     else:
#         themeCombobox.current(0)
#
#     themeCombobox.pack(fill=X, pady=5, padx=5)
#
#     frameSettings.pack(expand=True, fill=BOTH, pady=5, padx=5)
#
#     notebookConfiguration.add(frameSilentShot, text="Silent Shot")
#     notebookConfiguration.add(frameSlideCancel, text="Slide Cancel")
#     notebookConfiguration.add(frameSettings, text="Settings")
#
#     notebookConfiguration.pack(fill=BOTH, expand=True, pady=5, padx=5)
#
#     def applyChanges():
#         global configuration
#
#         configuration = configFile.getConfiguration()
#
#         if targetGameCombobox.get() == "Modern Warfare":
#             configuration.set("settings", "targetGame", "Modern Warfare")
#
#             btnSlideCancelActivator.configure(state="success")
#             btnSlideCancelSlide.configure(state="success")
#             btnSlideCancelCancel.configure(state="success")
#         elif targetGameCombobox.get() == "Modern Warfare 2":
#             configuration.set("settings", "targetGame", "HQ")
#
#             btnSlideCancelActivator.configure(state="disabled")
#             btnSlideCancelSlide.configure(state="disabled")
#             btnSlideCancelCancel.configure(state="disabled")
#         else:
#             configuration.set("settings", "targetGame", "Modern Warfare")
#
#             btnSlideCancelActivator.configure(state="success")
#             btnSlideCancelSlide.configure(state="success")
#             btnSlideCancelCancel.configure(state="success")
#
#         configuration.set("settings", "theme", themeCombobox.get())
#
#         root.style.theme_use(themeCombobox.get())
#
#         configuration.set("silentshot", "lethalKey", btnSilentShotLethalKeyText.get())
#         configuration.set("silentshot", "weaponSwapKey", btnSilentShotWeaponSwapKeyText.get())
#         configuration.set("silentshot", "timeBefore", entryTimeBeforeLethal.get())
#         configuration.set("silentshot", "timeAfter", entryTimeAfterLethal.get())
#         configuration.set("silentshot", "exitScope", "%d" % checkboxValue.get())
#
#         print(btnSilentShotLethalKeyText.get())
#
#         configuration.set("slidecancel", "activatorKey", btnSlideCancelActivatorKeyText.get())
#         configuration.set("slidecancel", "slideKey", btnSlideCancelSlideKeyText.get())
#         configuration.set("slidecancel", "cancelKey", btnSlideCancelCancelKeyText.get())
#
#         with open('data/configuration.yml', 'w') as configfile:
#             configuration.write(configfile)
#             configfile.flush()
#             configfile.close()
#
#         print("Uninitializing scripts.")
#
#         if configuration.get("silentshot", "enabled") == "1":
#             uninitializeSilentShot()
#
#         if configuration.get("slidecancel", "enabled") == "1":
#             uninitializeSlideCancel()
#
#         print("Initializing scripts.")
#
#         if configuration.get("silentshot", "enabled") == "1":
#             initializeSilentShot()
#
#         if configuration.get("slidecancel", "enabled") == "1":
#             initializeSlideCancel()
#
#     applyChangesButton = ttb.Button(master=root, text="Apply Changes", command=applyChanges, style="success")
#     applyChangesButton.pack(fill=X, expand=True, pady=5, padx=5)
