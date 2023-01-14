import os
import sys
import time
from os import mkdir
from os import path
from tkinter.constants import *

import customtkinter as ctk
import requests
from PIL import Image
from dotenv import load_dotenv

import src.utils.configFile as configFile

ctk.set_default_color_theme("green")

load_dotenv()


class UpdateChecker(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Autobot Updater")
        self.iconbitmap(path.join("src", "assets", "logo.ico"))
        self.resizable(False, False)

        self.dialog = None
        self.dialogFrame = None
        self.updaterLabel = None
        self.updaterProgressbar = None
        self.data = None
        self.configuration = configFile.getConfiguration()

        self.currentVersionTag = self.configuration.get("settings", "version")
        self.currentVersionTagSplit = self.currentVersionTag.split(".")
        self.currentVersion = self.currentVersionTagSplit[0]
        self.currentVersionMajor = self.currentVersionTagSplit[1]
        self.currentVersionMinor = self.currentVersionTagSplit[2]

        self.versionTag = None
        self.versionTagSplit = None
        self.version = None
        self.versionMajor = None
        self.versionMinor = None

        self.updaterFrame = ctk.CTkFrame(self, fg_color="#191919", corner_radius=0)
        self.updaterInfoFrame = ctk.CTkFrame(self.updaterFrame, fg_color="#191919", corner_radius=0)
        self.updaterInfoFrame.pack(padx=10, pady=20)
        self.updaterFrame.pack()

        self.updaterLogo = ctk.CTkLabel(
            self.updaterInfoFrame,
            text="",
            image=ctk.CTkImage(
                light_image=Image.open("src/assets/logo.png"),
                dark_image=Image.open("src/assets/logo.png"),
                size=(90, 90))
        )
        self.updaterLogo.pack(
            padx=50,
            pady=(0, 10)
        )

        self.setMessage(text="Checking for updates.")

        if self.hasNewVersion():
            self.dialog = ctk.CTkToplevel(self)
            self.dialog.title("Autobot Updater")
            self.dialog.iconbitmap(path.join("src", "assets", "logo.ico"))
            self.dialog.resizable(False, False)

            self.dialogFrame = ctk.CTkFrame(self.dialog, fg_color="#191919", corner_radius=0)
            self.dialogFrame.pack()

            messageLabel = ctk.CTkLabel(self.dialogFrame,
                                        text="An update has been found, would you like to download it?")
            messageLabel.pack(padx=20, pady=(20, 10))

            yesButton = ctk.CTkButton(self.dialogFrame, text="Yes", command=self.downloadLatestUpdate)
            yesButton.pack(side=RIGHT, padx=(10, 20), pady=(0, 20), expand=True, fill=X)

            noButton = ctk.CTkButton(self.dialogFrame, text="No", command=self.destroy)
            noButton.pack(side=RIGHT, padx=(20, 0), pady=(0, 20), expand=True, fill=X)
        else:
            self.destroy()

    def downloadLatestUpdate(self):
        self.dialog.destroy()

        if not path.exists("downloads/"):
            mkdir("downloads/")

        self.dialog = ctk.CTkToplevel(self)
        self.dialog.title("Autobot Updater")
        self.dialog.iconbitmap(path.join("src", "assets", "logo.ico"))
        self.dialog.resizable(False, False)

        self.dialogFrame = ctk.CTkFrame(self.dialog, fg_color="#191919", corner_radius=0)
        self.dialogFrame.pack()

        messageLabel = ctk.CTkLabel(self.dialogFrame,
                                    text="Please do not use your pc during this process. It will corrupt the installation.")
        messageLabel.pack(padx=20, pady=(20, 10))

        okButton = ctk.CTkButton(self.dialogFrame, text="Ok", command=self.beginDownload)
        okButton.pack(side=RIGHT, padx=(10, 20), pady=(0, 20))

    def beginDownload(self):
        self.dialog.destroy()

        downloadUrl = self.data["assets"][1]["browser_download_url"]
        fileName = self.data["assets"][1]["name"]

        self.setMessage("Downloading updater.")

        self.updaterProgressbar = ctk.CTkProgressBar(
            master=self.updaterInfoFrame,
        )
        self.updaterProgressbar.set(0)
        self.updaterProgressbar.pack(fill=X, expand=True)

        self.update_idletasks()
        self.update()

        with open("%s" % fileName, "wb") as f:
            response = requests.get(downloadUrl, stream=True)
            totalLength = response.headers.get('content-length')

            if totalLength is None:
                f.write(response.content)
            else:
                dl = 0
                totalLength = int(totalLength)

                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(100 * dl / totalLength)

                    self.updaterProgressbar.set(done / 100)
                    self.update_idletasks()
                    self.update()

        self.setMessage("Launching updater.")

        self.updaterProgressbar.destroy()

        self.update_idletasks()
        self.update()

        time.sleep(1)

        os.startfile("%s\\AutobotUpdater.exe" % os.curdir)

        sys.exit(0)

    def hasNewVersion(self):
        URL = "https://api.github.com/repos/connor-davis/Autobot/releases/latest"

        r = requests.get(url=URL)

        self.data = r.json()

        self.versionTag = self.data["tag_name"]
        self.versionTagSplit = self.versionTag.split(".")
        self.version = self.versionTagSplit[0]
        self.versionMajor = self.versionTagSplit[1]
        self.versionMinor = self.versionTagSplit[2]

        return (
            self.version,
            self.versionMajor,
            self.versionMinor
        ) > (
            self.currentVersion,
            self.currentVersionMajor,
            self.currentVersionMinor
        )

    def setMessage(self, text: str):
        if self.updaterLabel:
            self.updaterLabel.destroy()

        self.updaterLabel = ctk.CTkLabel(self.updaterInfoFrame, text=text)
        self.updaterLabel.pack()
        self.update_idletasks()
        self.update()
