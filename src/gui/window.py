from src.scripts.silentShot import *
from src.scripts.slideCancel import *
from src.scripts.toggler import *

import src.gui.mainWindow as mainWindow
import src.gui.authWindow as authWindow

import src.utils.configFile as configFile

def initializeApp(root):
    mainWindow.runMainWindow(root)

    print("Initializing scripts.")

    configuration = configFile.getConfiguration()

    if configuration.getboolean("silentshot", "enabled"):
        initializeSilentShot()
    else:
        uninitializeSilentShot()

    if configuration.getboolean("slidecancel", "enabled"):
        initializeSlideCancel()
    else:
        uninitializeSlideCancel()

    initializeToggler()

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

def runWindow(root):
    authWindow.runAuthWindow(root, initializeApp)
