import src.utils.configFile as configFile
from src.gui.authWindow import AuthWindow
from src.gui.mainWindow import MainWindow
from src.utils.updateChecker import UpdateChecker

configuration = configFile.getConfiguration()

if __name__ == '__main__':
    # updateChecker = UpdateChecker()
    # updateChecker.mainloop()
    #
    # auth = AuthWindow()
    # auth.mainloop()

    main = MainWindow()
    main.mainloop()
