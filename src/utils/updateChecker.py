import configparser
import os
import sys
from os import mkdir, path

import requests
import ttkbootstrap as ttb
from PIL import Image, ImageTk
from dotenv import load_dotenv
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import src.utils.configFile as configFile

load_dotenv()

configuration = configFile.getConfiguration()

def runUpdateChecker(root):
    updaterFrame = ttb.Frame(master=root)

    image = Image.open("src/assets/logo.png")
    img = image.resize((96, 96))
    file = ImageTk.PhotoImage(img)

    updaterLabel = ttb.Label(master=updaterFrame, image=file)
    updaterLabel.pack(pady=(0, 30), padx=50)

    updaterLabel = ttb.Label(master=updaterFrame, text="Checking for updates.", font=("Impact", 13))
    updaterLabel.pack()

    updaterFrame.pack(pady=30, padx=30)

    root.update_idletasks()
    root.update()

    root.withdraw()
    root.update_idletasks()

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))

    root.deiconify()
    root.update_idletasks()
    root.update()

    currentVersionTag = configuration.get("settings", "version")
    currentVersionTagSplit = currentVersionTag.split(".")
    currentVersion = currentVersionTagSplit[0]
    currentVersionMajor = currentVersionTagSplit[1]
    currentVersionMinor = currentVersionTagSplit[2]

    print("Fetching latest release")

    URL = "https://api.github.com/repos/connor-davis/Autobot/releases/latest"

    r = requests.get(url=URL)

    data = r.json()

    versionTag = data["tag_name"]
    versionTagSplit = versionTag.split(".")
    version = versionTagSplit[0]
    versionMajor = versionTagSplit[1]
    versionMinor = versionTagSplit[2]

    print("Current Version: %s, Major: %s, Minor: %s" % (currentVersion, currentVersionMajor, currentVersionMinor))
    print("Latest Version: %s, Major: %s, Minor: %s" % (version, versionMajor, versionMinor))

    if version > currentVersion or versionMajor > currentVersionMajor or versionMinor > currentVersionMinor:
        okNo = Messagebox.yesno(parent=root, title="Autobot Updater",
                                message="An update has been found, would you like to download it?")

        if okNo == "Yes":
            if not path.exists("downloads/"):
                mkdir("downloads/")

            downloadUrl = data["assets"][1]["browser_download_url"]
            fileName = data["assets"][1]["name"]

            updaterLabel.destroy()

            updaterLabel = ttb.Label(master=updaterFrame, text="Downloading updater.", font=("Impact", 13))
            updaterLabel.pack(pady=(0, 10))

            updaterProgressbar = ttb.Progressbar(master=updaterFrame, bootstyle="success", maximum=100,
                                                 value=0)
            updaterProgressbar.pack(fill=X, expand=True)

            updaterFrame.pack()

            root.update_idletasks()
            root.update()

            print("New version found. Downloading.")

            root.update_idletasks()
            root.update()

            with open("%s" % fileName, "wb") as f:
                print("Downloading %s" % fileName)

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

                        updaterProgressbar.destroy()
                        updaterProgressbar = ttb.Progressbar(master=updaterFrame, bootstyle="success",
                                                             maximum=100, value=done, mode="determinate")
                        updaterProgressbar.pack(fill=X, expand=True)

                        updaterFrame.pack()

                        root.update_idletasks()
                        root.update()

            updaterLabel.destroy()

            updaterLabel = ttb.Label(master=updaterFrame, text="Launching updater.", font=("Impact", 13))
            updaterLabel.pack()

            updaterProgressbar.destroy()

            updaterFrame.pack()

            root.update_idletasks()
            root.update()

            updaterFrame.destroy()

            os.startfile("%s\\AutobotUpdater.exe" % os.curdir)

            sys.exit(0)

    updaterFrame.destroy()

    root.update_idletasks()
    root.update()
