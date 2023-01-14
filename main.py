import time
from os import path, remove

from src.gui.authWindow import AuthWindow
from src.gui.mainWindow import MainWindow
from src.utils.configFile import testConfiguration
from src.utils.updateChecker import UpdateChecker
from src.gui.authWindow import AuthWindow
from src.gui.mainWindow import MainWindow
from src.utils.updateChecker import UpdateChecker


testConfiguration()

if __name__ == '__main__':
    if path.exists("data/session.txt"):
        remove(path.join("data", "session.txt"))

    updateChecker = UpdateChecker()
    updateChecker.mainloop()

    auth = AuthWindow()
    auth.mainloop()

    if path.exists("data/session.txt"):
        main = MainWindow()
        main.mainloop()

