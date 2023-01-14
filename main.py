from os import path, remove

import src.utils.configFile as configFile
from src.gui.authWindow import AuthWindow
from src.gui.mainWindow import MainWindow
from src.utils.updateChecker import UpdateChecker

configuration = configFile.getConfiguration()

if __name__ == '__main__':
    if path.exists("data/session.txt"):
        remove(path.join("data", "session.txt"))

    configFile.testConfiguration()

    updateChecker = UpdateChecker()
    updateChecker.mainloop()

    auth = AuthWindow()
    auth.mainloop()

    if path.exists("data/session.txt"):
        main = MainWindow()
        main.mainloop()
