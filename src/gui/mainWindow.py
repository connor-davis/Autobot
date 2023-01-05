from tkinter import IntVar, StringVar

import ttkbootstrap as ttb
from ttkbootstrap.constants import *

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


job = None
listenerKeyboard = None
entrySilentShotLethalKey = None


def runMainWindow(root):
    global entrySilentShotLethalKey

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

    btnSilentShotLethalKeyText = StringVar()

    def getLethalKey():
        global listenerKeyboard

        if listenerKeyboard is not None:
            listenerKeyboard = None

        listenerKeyboard = keyboard.Listener(on_press=handleLethalPress)
        listenerKeyboard.start()

    def handleLethalPress(key):
        global listenerKeyboard, job

        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        btnSilentShotLethalKeyText.set(keyBind)

        root.update_idletasks()
        root.update()

        listenerKeyboard.stop()

    btnSilentShotLethalKeyText.set(silentShotLethalKey)
    entrySilentShotLethalKey = ttb.Button(master=frameSilentShot, style="success-outline",
                                          textvariable=btnSilentShotLethalKeyText, command=getLethalKey)
    entrySilentShotLethalKey.pack(fill=X, expand=True, pady=5, padx=5, anchor=W)

    labelSilentShotWeaponSwap = ttb.Label(master=frameSilentShot, text="Weapon Swap Key, e.g. 1")
    labelSilentShotWeaponSwap.pack(fill=X, expand=True, pady=5, padx=5)

    btnSilentShotWeaponSwapKeyText = StringVar()

    def getWeaponSwapKey():
        global listenerKeyboard

        if listenerKeyboard is not None:
            listenerKeyboard = None

        listenerKeyboard = keyboard.Listener(on_press=handleActivatorPress)
        listenerKeyboard.start()

    def handleActivatorPress(key):
        global listenerKeyboard, job

        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        btnSilentShotWeaponSwapKeyText.set(keyBind)

        root.update_idletasks()
        root.update()

        listenerKeyboard.stop()

    btnSilentShotWeaponSwapKeyText.set(silentShotWeaponSwapKey)
    entrySilentShotWeaponSwapKey = ttb.Button(master=frameSilentShot, style="success-outline",
                                              textvariable=btnSilentShotWeaponSwapKeyText, command=getWeaponSwapKey)
    entrySilentShotWeaponSwapKey.pack(fill=X, expand=True, pady=5, padx=5, anchor=W)

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
                                        variable=checkboxValue, onvalue=1, offvalue=0,
                                        bootstyle="success-rounded-toggle")
    checkboxExitScope.pack(fill=X, expand=True, pady=5, padx=5)

    frameSilentShot.pack(expand=True, fill=BOTH, pady=5, padx=5)

    frameSlideCancel = ttb.Frame(notebookConfiguration, padding=5)

    labelSlideCancelActivator = ttb.Label(master=frameSlideCancel, text="Activator Key, e.g. c")
    labelSlideCancelActivator.pack(fill=X, pady=5, padx=5)

    btnSlideCancelActivatorKeyText = StringVar()

    def getActivatorKey():
        global listenerKeyboard

        if listenerKeyboard is not None:
            listenerKeyboard = None

        listenerKeyboard = keyboard.Listener(on_press=handleActivatorPress)
        listenerKeyboard.start()

    def handleActivatorPress(key):
        global listenerKeyboard, job

        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        btnSlideCancelActivatorKeyText.set(keyBind)

        root.update_idletasks()
        root.update()

        listenerKeyboard.stop()

    btnSlideCancelActivatorKeyText.set(slideCancelActivatorKey)
    btnSlideCancelActivator = ttb.Button(master=frameSlideCancel, style="success-outline",
                                         textvariable=btnSlideCancelActivatorKeyText, command=getActivatorKey)
    btnSlideCancelActivator.pack(fill=X, pady=5, padx=5)

    labelSlideCancelSlide = ttb.Label(master=frameSlideCancel, text="Slide Key, e.g. c")
    labelSlideCancelSlide.pack(fill=X, pady=5, padx=5)

    btnSlideCancelSlideKeyText = StringVar()

    def getSlideKey():
        global listenerKeyboard

        if listenerKeyboard is not None:
            listenerKeyboard = None

        listenerKeyboard = keyboard.Listener(on_press=handleSidePress)
        listenerKeyboard.start()

    def handleSidePress(key):
        global listenerKeyboard, job

        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        btnSlideCancelSlideKeyText.set(keyBind)

        root.update_idletasks()
        root.update()

        listenerKeyboard.stop()

    btnSlideCancelSlideKeyText.set(slideCancelSlideKey)
    btnSlideCancelSlide = ttb.Button(master=frameSlideCancel, style="success-outline",
                                     textvariable=btnSlideCancelSlideKeyText, command=getSlideKey)
    btnSlideCancelSlide.pack(fill=X, pady=5, padx=5)

    labelSlideCancelCancel = ttb.Label(master=frameSlideCancel, text="Cancel Key, e.g. space")
    labelSlideCancelCancel.pack(fill=X, pady=5, padx=5)

    btnSlideCancelCancelKeyText = StringVar()

    def getCancelKey():
        global listenerKeyboard

        if listenerKeyboard is not None:
            listenerKeyboard = None

        listenerKeyboard = keyboard.Listener(on_press=handleCancelPress)
        listenerKeyboard.start()

    def handleCancelPress(key):
        global listenerKeyboard, job

        keyBind = "{0}".format(key).replace("'", "").replace("Key.", "")

        btnSlideCancelCancelKeyText.set(keyBind)

        root.update_idletasks()
        root.update()

        listenerKeyboard.stop()

    btnSlideCancelCancelKeyText.set(slideCancelCancelKey)
    btnSlideCancelCancel = ttb.Button(master=frameSlideCancel, style="success-outline",
                                      textvariable=btnSlideCancelCancelKeyText, command=getCancelKey)
    btnSlideCancelCancel.pack(fill=X, pady=5, padx=5)

    frameSlideCancel.pack(expand=True, fill=BOTH, pady=5, padx=5)

    frameSettings = ttb.Frame(notebookConfiguration, padding=5)

    targetGameLabel = ttb.Label(master=frameSettings, text="Target Game")
    targetGameLabel.pack(fill=X, pady=5, padx=5)

    targetGameCombobox = ttb.Combobox(master=frameSettings, values=['Modern Warfare', 'Modern Warfare 2'],
                                      bootstyle="success")

    if targetGame == "Modern Warfare":
        targetGameCombobox.current(0)

        btnSlideCancelActivator.configure(state="success")
        btnSlideCancelSlide.configure(state="success")
        btnSlideCancelCancel.configure(state="success")
    elif targetGame == "HQ":
        targetGameCombobox.current(1)

        btnSlideCancelActivator.configure(state="disabled")
        btnSlideCancelSlide.configure(state="disabled")
        btnSlideCancelCancel.configure(state="disabled")
    else:
        targetGameCombobox.current(0)

        btnSlideCancelActivator.configure(state="success")
        btnSlideCancelSlide.configure(state="success")
        btnSlideCancelCancel.configure(state="success")

    targetGameCombobox.pack(fill=X, pady=5, padx=5)

    themeLabel = ttb.Label(master=frameSettings, text="App Theme")
    themeLabel.pack(fill=X, pady=5, padx=5)

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

            btnSlideCancelActivator.configure(state="success")
            btnSlideCancelSlide.configure(state="success")
            btnSlideCancelCancel.configure(state="success")
        elif targetGameCombobox.get() == "Modern Warfare 2":
            settingsConfig["settings"]["targetGame"] = "HQ"

            btnSlideCancelActivator.configure(state="disabled")
            btnSlideCancelSlide.configure(state="disabled")
            btnSlideCancelCancel.configure(state="disabled")
        else:
            settingsConfig["settings"]["targetGame"] = "Modern Warfare"

            btnSlideCancelActivator.configure(state="success")
            btnSlideCancelSlide.configure(state="success")
            btnSlideCancelCancel.configure(state="success")

        settingsConfig["settings"]["theme"] = themeCombobox.get()

        root.style.theme_use(themeCombobox.get())

        silentShotConfig["config"]["enabled"] = silentShotConfig["config"]["enabled"]
        silentShotConfig["config"]['lethalKey'] = btnSilentShotLethalKeyText.get()
        silentShotConfig["config"]['weaponSwapKey'] = btnSilentShotWeaponSwapKeyText.get()
        silentShotConfig["config"]['timeBefore'] = entryTimeBeforeLethal.get()
        silentShotConfig["config"]['timeAfter'] = entryTimeAfterLethal.get()
        silentShotConfig["config"]['exitScope'] = "%d" % checkboxValue.get()

        slideCancelConfig["config"]["enabled"] = slideCancelConfig["config"]["enabled"]
        slideCancelConfig["config"]['activatorKey'] = btnSlideCancelActivatorKeyText.get()
        slideCancelConfig["config"]['slideKey'] = btnSlideCancelSlideKeyText.get()
        slideCancelConfig["config"]['cancelKey'] = btnSlideCancelCancelKeyText.get()

        with open('data/settings.ini', 'w') as configfile:
            settingsConfig.write(configfile)
        with open('data/silentShot.ini', 'w') as configfile:
            silentShotConfig.write(configfile)
        with open('data/slideCancel.ini', 'w') as configfile:
            slideCancelConfig.write(configfile)

    applyChangesButton = ttb.Button(master=root, text="Apply Changes", command=applyChanges, style="success")
    applyChangesButton.pack(fill=X, expand=True, pady=5, padx=5)
