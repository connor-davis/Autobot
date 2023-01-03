import configparser
import shutil
from os import mkdir, path, getenv
from tkinter import IntVar
from zipfile import ZipFile

import requests
import ttkbootstrap as ttb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from dotenv import load_dotenv

load_dotenv()

settings = configparser.ConfigParser()
settings.read("data/settings.ini")


def runUpdater(root):
    updaterFrame = ttb.Frame(master=root)

    image = Image.open("src/assets/logo.png")
    img = image.resize((96, 96))
    file = ImageTk.PhotoImage(img)

    updaterLabel = ttb.Label(master=updaterFrame, image=file)
    updaterLabel.pack(pady=(0, 30), padx=50)

    updaterLabel = ttb.Label(master=updaterFrame, text="Checking for updates", font=("Impact", 13))
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

    currentVersionTag = settings["settings"]["version"]
    currentVersionTagSplit = currentVersionTag.split(".")
    currentVersion = currentVersionTagSplit[0]
    currentVersionMajor = currentVersionTagSplit[1]
    currentVersionMinor = currentVersionTagSplit[2]

    print("Fetching latest release")

    URL = "https://api.github.com/repos/connor-davis/Autobot/releases/latest"

    r = requests.get(url=URL)

    data = r.json()
    downloadUrl = data["assets"][0]["browser_download_url"]
    fileName = data["assets"][0]["name"]
    versionTag = data["tag_name"]
    versionTagSplit = versionTag.split(".")
    version = versionTagSplit[0]
    versionMajor = versionTagSplit[1]
    versionMinor = versionTagSplit[2]

    settings.read("data/settings.ini")

    settings["settings"]["version"] = versionTag

    with open('data/settings.ini', 'w') as configfile:
        settings.write(configfile)

    print("Current Version: %s, Major: %s, Minor: %s" % (currentVersion, currentVersionMajor, currentVersionMinor))
    print("Latest Version: %s, Major: %s, Minor: %s" % (version, versionMajor, versionMinor))

    if version > currentVersion or versionMajor > currentVersionMajor or versionMinor > currentVersionMinor:
        updaterLabel.destroy()

        updaterLabel = ttb.Label(master=updaterFrame, text="Downloading update", font=("Impact", 13))
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

        with open("downloads/%s" % fileName, "wb") as f:
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

        if not path.exists("downloads/"):
            mkdir("downloads/")

        updaterLabel.destroy()

        updaterLabel = ttb.Label(master=updaterFrame, text="Extracting update", font=("Impact", 13))
        updaterLabel.pack()

        updaterProgressbar.destroy()

        updaterFrame.pack()

        root.update_idletasks()
        root.update()

        print("Extracting new version.")

        with ZipFile("downloads/%s" % fileName, 'r') as zObject:
            zObject.extractall(path="downloads/")

        zObject.close()

        print("Extracted new version.")

        if path.exists("src/"):
            shutil.rmtree("src/")

        print("Copying download src directory contents to local src directory.")

        source_folder = r"downloads/Autobot/src/"
        destination_folder = r"src/"

        shutil.copytree(source_folder, destination_folder)

        print("Update has been completed.")

        updaterLabel = ttb.Label(master=updaterFrame, text="Update finished.", font=("Impact", 13))
        updaterLabel.pack()

        updaterFrame.pack()

        root.update_idletasks()
        root.update()

    updaterFrame.destroy()

    root.update_idletasks()
    root.update()
