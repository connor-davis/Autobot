from src.gui.window import *
from src.scripts.silentShot import *
from src.scripts.slideCancel import *
from src.scripts.toggler import *

if __name__ == '__main__':
    print("Initializing scripts.")

    initializeSilentShot()
    initializeSlideCancel()
    initializeToggler()

    print("Running window.")

    runWindow()

    print("Application has finished.")
