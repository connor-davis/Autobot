import configparser
import os
import shutil
import sys
import time
from os import mkdir, path
from zipfile import ZipFile

import requests
import ttkbootstrap as ttb
from PIL import Image, ImageTk
from dotenv import load_dotenv
from ttkbootstrap.constants import *

import src.utils.configFile as configFile

load_dotenv()

if __name__ == '__main__':
    root = ttb.Window(themename="darkly")
    root.title("Autobot")
    iconFile = path.join("src", "assets", "logo.ico")
    root.iconbitmap(iconFile)

    if not path.exists("downloads/"):
        mkdir("downloads/")

    image = Image.open("src/assets/logo.png")
    img = image.resize((96, 96))
    file = ImageTk.PhotoImage(img)

    updaterFrame = ttb.Frame(master=root)

    updaterLabel = ttb.Label(master=updaterFrame, image=file)
    updaterLabel.pack(pady=(0, 30), padx=50)

    updaterLabel = ttb.Label(master=updaterFrame, text="Downloading Autobot", font=("Impact", 13))
    updaterLabel.pack()

    updaterProgressbar = ttb.Progressbar(master=updaterFrame, bootstyle="success", maximum=100,
                                         value=0)
    updaterProgressbar.pack(fill=X, expand=True)

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

    URL = "https://api.github.com/repos/connor-davis/Autobot/releases/latest"

    r = requests.get(url=URL)

    data = r.json()
    downloadUrl = data["assets"][0]["browser_download_url"]
    fileName = data["assets"][0]["name"]
    versionTag = data["tag_name"]

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

    print("Copying download src directory contents to local src directory.")

    source_file = r"downloads/Autobot/Autobot.exe"
    destination_file = r"Autobot.exe"

    shutil.copy2(source_file, destination_file)

    print("Update has been completed.")

    configuration = configFile.getConfiguration()

    configuration.set("settings", "version", versionTag)

    with open('data/configuration.yml', 'w') as configfile:
        configuration.write(configfile)
        configfile.flush()
        configfile.close()

    updaterLabel = ttb.Label(master=updaterFrame, text="Update finished.", font=("Impact", 13))
    updaterLabel.pack()

    updaterFrame.pack()

    root.update_idletasks()
    root.update()

    time.sleep(2)

    updaterFrame.destroy()

    root.update_idletasks()
    root.update()

    os.startfile("%s\\Autobot.exe" % os.curdir)

    sys.exit(0)
