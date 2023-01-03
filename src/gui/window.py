from os import path
from tkinter import IntVar

import ttkbootstrap as ttb
from ttkbootstrap.constants import *

from src.scripts.silentShot import *
from src.scripts.slideCancel import *
from src.scripts.toggler import *

settingsConfig = configparser.ConfigParser()
settingsConfig.read("data/settings.ini")

silentShotConfig = configparser.ConfigParser()
silentShotConfig.read("data/silentShot.ini")

slideCancelConfig = configparser.ConfigParser()
slideCancelConfig.read("data/slideCancel.ini")

targetGame = settingsConfig["settings"]["targetGame"]
theme = settingsConfig["settings"]["theme"]

silentShotLethalKey = silentShotConfig["config"]["lethalKey"]
silentShotWeaponSwapKey = silentShotConfig["config"]["weaponSwapKey"]
silentShotTimeBefore = silentShotConfig["config"]["timeBefore"]
silentShotTimeAfter = silentShotConfig["config"]["timeAfter"]
exitScopeAfterSilentShot = silentShotConfig["config"]["exitScope"] == "1"

slideCancelActivatorKey = slideCancelConfig["config"]["activatorKey"]
slideCancelSlideKey = slideCancelConfig["config"]["slideKey"]
slideCancelCancelKey = slideCancelConfig["config"]["cancelKey"]


def toggleExitScope():
    global exitScopeAfterSilentShot

    if exitScopeAfterSilentShot:
        exitScopeAfterSilentShot = False
    else:
        exitScopeAfterSilentShot = True


def runWindow(root):
    print("Initializing scripts.")

    initializeSilentShot()
    initializeSlideCancel()
    initializeToggler()

    labelHeading = ttb.Label(text="Autobot Macros", font=("Impact", 24))
    labelHeading.pack(pady=10, padx=10)

    labelDescription = ttb.Label(
        text="Autobot Macros help you with lazily performing the silent shot and slide cancel.",
        font="Arial", wraplength=400)
    labelDescription.pack(pady=5, padx=5)

    notebookConfiguration = ttb.Notebook(root)

    frameSilentShot = ttb.Frame(notebookConfiguration, padding=5)

    labelSilentShotLethalKey = ttb.Label(master=frameSilentShot, text="Lethal Key, e.g. f")
    labelSilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5)

    entrySilentShotLethalKey = ttb.Entry(master=frameSilentShot, style="success")
    entrySilentShotLethalKey.insert(0, silentShotLethalKey)
    entrySilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5)

    labelSilentShotWeaponSwap = ttb.Label(master=frameSilentShot, text="Weapon Swap Key, e.g. 1")
    labelSilentShotWeaponSwap.pack(fill=X, expand=True, pady=5, padx=5)

    entrySilentShotWeaponSwap = ttb.Entry(master=frameSilentShot, style="success")
    entrySilentShotWeaponSwap.insert(0, silentShotWeaponSwapKey)
    entrySilentShotWeaponSwap.pack(fill=X, expand=True, pady=5, padx=5)

    labelSilentShotLethalKey = ttb.Label(master=frameSilentShot, text="Time Before Lethal (milliseconds)")
    labelSilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5)

    entryTimeBeforeLethal = ttb.Entry(master=frameSilentShot, style="success")
    entryTimeBeforeLethal.insert(0, silentShotTimeBefore)
    entryTimeBeforeLethal.pack(fill=X, expand=True, pady=5, padx=5)

    labelSilentShotLethalKey = ttb.Label(master=frameSilentShot, text="Time After Lethal (milliseconds)")
    labelSilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5)

    entryTimeAfterLethal = ttb.Entry(master=frameSilentShot, style="success")
    entryTimeAfterLethal.insert(0, silentShotTimeAfter)
    entryTimeAfterLethal.pack(fill=X, expand=True, pady=5, padx=5)

    checkboxValue = IntVar()

    if exitScopeAfterSilentShot:
        checkboxValue.set(1)
    else:
        checkboxValue.set(0)

    checkboxExitScope = ttb.Checkbutton(master=frameSilentShot,
                                        text="Exit scope after silent shot?", command=toggleExitScope,
                                        variable=checkboxValue, onvalue=1, offvalue=0, bootstyle="success-rounded-toggle")
    checkboxExitScope.pack(fill=X, expand=True, pady=5, padx=5)

    frameSilentShot.pack(expand=True, fill=BOTH, pady=5, padx=5)

    frameSlideCancel = ttb.Frame(notebookConfiguration, padding=5)

    labelSlideCancelActivator = ttb.Label(master=frameSlideCancel, text="Activator Key, e.g. c")
    labelSlideCancelActivator.pack(fill=X, pady=5, padx=5)

    entrySlideCancelActivatorKey = ttb.Entry(master=frameSlideCancel, style="success")
    entrySlideCancelActivatorKey.insert(0, slideCancelActivatorKey)
    entrySlideCancelActivatorKey.pack(fill=X, pady=5, padx=5)

    labelSlideCancelSlide = ttb.Label(master=frameSlideCancel, text="Slide Key, e.g. c")
    labelSlideCancelSlide.pack(fill=X, pady=5, padx=5)

    entrySlideCancelSlideKey = ttb.Entry(master=frameSlideCancel, style="success")
    entrySlideCancelSlideKey.insert(0, slideCancelSlideKey)
    entrySlideCancelSlideKey.pack(fill=X, pady=5, padx=5)

    labelSlideCancelCancel = ttb.Label(master=frameSlideCancel, text="Cancel Key, e.g. space")
    labelSlideCancelCancel.pack(fill=X, pady=5, padx=5)

    entrySlideCancelCancelKey = ttb.Entry(master=frameSlideCancel, style="success")
    entrySlideCancelCancelKey.insert(0, slideCancelCancelKey)
    entrySlideCancelCancelKey.pack(fill=X, pady=5, padx=5)

    frameSlideCancel.pack(expand=True, fill=BOTH, pady=5, padx=5)

    frameSettings = ttb.Frame(notebookConfiguration, padding=5)

    targetGameCombobox = ttb.Combobox(master=frameSettings, values=['Modern Warfare', 'Modern Warfare 2'],
                                      bootstyle="success")

    if targetGame == "Modern Warfare":
        targetGameCombobox.current(0)

        entrySlideCancelActivatorKey.configure(state="success")
        entrySlideCancelSlideKey.configure(state="success")
        entrySlideCancelCancelKey.configure(state="success")
    elif targetGame == "HQ":
        targetGameCombobox.current(1)

        entrySlideCancelActivatorKey.configure(state="disabled")
        entrySlideCancelSlideKey.configure(state="disabled")
        entrySlideCancelCancelKey.configure(state="disabled")
    else:
        targetGameCombobox.current(0)

        entrySlideCancelActivatorKey.configure(state="success")
        entrySlideCancelSlideKey.configure(state="success")
        entrySlideCancelCancelKey.configure(state="success")

    targetGameCombobox.pack(fill=X, pady=5, padx=5)

    themeCombobox = ttb.Combobox(master=frameSettings, values=["darkly", "vapor", "flatly", "pulse"],
                                 bootstyle="success")

    if theme == "darkly":
        themeCombobox.current(0)
    elif theme == "vapor":
        themeCombobox.current(1)
    elif theme == "flatly":
        themeCombobox.current(2)
    elif theme == "pulse":
        themeCombobox.current(3)
    else:
        themeCombobox.current(0)

    themeCombobox.pack(fill=X, pady=5, padx=5)

    frameSettings.pack(expand=True, fill=BOTH, pady=5, padx=5)

    notebookConfiguration.add(frameSilentShot, text="Silent Shot")
    notebookConfiguration.add(frameSlideCancel, text="Slide Cancel")
    notebookConfiguration.add(frameSettings, text="Settings")

    notebookConfiguration.pack(fill=BOTH, expand=True, pady=5, padx=5)

    def applyChanges():
        settingsConfig.read("data/settings.ini")
        silentShotConfig.read("data/silentShot.ini")
        slideCancelConfig.read("data/slideCancel.ini")

        if targetGameCombobox.get() == "Modern Warfare":
            settingsConfig["settings"]["targetGame"] = "Modern Warfare"

            entrySlideCancelActivatorKey.configure(state="success")
            entrySlideCancelSlideKey.configure(state="success")
            entrySlideCancelCancelKey.configure(state="success")
        elif targetGameCombobox.get() == "Modern Warfare 2":
            settingsConfig["settings"]["targetGame"] = "HQ"

            entrySlideCancelActivatorKey.configure(state="disabled")
            entrySlideCancelSlideKey.configure(state="disabled")
            entrySlideCancelCancelKey.configure(state="disabled")
        else:
            settingsConfig["settings"]["targetGame"] = "Modern Warfare"

            entrySlideCancelActivatorKey.configure(state="success")
            entrySlideCancelSlideKey.configure(state="success")
            entrySlideCancelCancelKey.configure(state="success")

        settingsConfig["settings"]["theme"] = themeCombobox.get()

        root.style.theme_use(themeCombobox.get())

        silentShotConfig["config"]["enabled"] = silentShotConfig["config"]["enabled"]
        silentShotConfig["config"]['lethalKey'] = entrySilentShotLethalKey.get()
        silentShotConfig["config"]['weaponSwapKey'] = entrySilentShotWeaponSwap.get()
        silentShotConfig["config"]['timeBefore'] = entryTimeBeforeLethal.get()
        silentShotConfig["config"]['timeAfter'] = entryTimeAfterLethal.get()
        silentShotConfig["config"]['exitScope'] = "%d" % checkboxValue.get()

        slideCancelConfig["config"]["enabled"] = slideCancelConfig["config"]["enabled"]
        slideCancelConfig["config"]['activatorKey'] = entrySlideCancelActivatorKey.get()
        slideCancelConfig["config"]['slideKey'] = entrySlideCancelSlideKey.get()
        slideCancelConfig["config"]['cancelKey'] = entrySlideCancelCancelKey.get()

        with open('data/settings.ini', 'w') as configfile:
            settingsConfig.write(configfile)
        with open('data/silentShot.ini', 'w') as configfile:
            silentShotConfig.write(configfile)
        with open('data/slideCancel.ini', 'w') as configfile:
            slideCancelConfig.write(configfile)

    applyChangesButton = ttb.Button(master=root, text="Apply Changes", command=applyChanges, style="success")
    applyChangesButton.pack(fill=X, expand=True, pady=5, padx=5)

    root.update_idletasks()
    root.update()

    root.withdraw()
    root.update_idletasks()

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))

    root.deiconify()
    root.resizable(False, False)
    root.mainloop()
