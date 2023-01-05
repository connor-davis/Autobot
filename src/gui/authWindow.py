import configparser
import getpass
import hashlib
import os
import sys
import uuid

import requests
import ttkbootstrap as ttb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import MessageDialog

userHWID = hashlib.sha256(
    (os.name + getpass.getuser() + str(hex(uuid.getnode()))).encode()).hexdigest()

def runAuthWindow(root, callback):
    settings = configparser.ConfigParser()
    settings.read("data/settings.ini")

    authFrame = ttb.Frame(master=root)

    labelHeading = ttb.Label(master=authFrame, text="Autobot Auth", font=("Impact", 24))
    labelHeading.pack(pady=10, padx=10)

    labelDescription = ttb.Label(
        master=authFrame,
        text="Please enter your license key to use the app.",
        font="Arial", wraplength=400)
    labelDescription.pack(pady=(5, 50), padx=5)

    def setUserKey():
        userEmail = emailEntry.get()
        userPassword = passwordEntry.get()

        URL = "https://autobot.valupak.co.za"
        DATA = {"identifier": "%s" % userEmail, "password": "%s" % userPassword}

        authResponse = requests.post(url="%s%s" % (URL, "/api/auth/local"), data=DATA)

        authData = authResponse.json()

        settings = configparser.ConfigParser()
        settings.read("data/settings.ini")

        settings["settings"]["email"] = userEmail
        settings["settings"]["password"] = userPassword

        with open('data/settings.ini', 'w') as configfile:
            settings.write(configfile)

        if "error" not in authData:
            userId = authData["user"]["id"]

            HEADERS = {"Authorization": "Bearer %s" % authData["jwt"]}

            accountResponse = requests.get(url="%s%s%s" % (URL, "/api/users/", userId), headers=HEADERS)
            accountResponseData = accountResponse.json()

            if "hwid" in accountResponseData:
                if accountResponseData["hwid"] == "" or accountResponseData["hwid"] is None or accountResponseData[
                    "hwid"] == userHWID:
                    updateResponse = requests.put(url="%s%s%s" % (URL, "/api/users/", userId),
                                                  data={"hwid": "%s" % userHWID},
                                                  headers=HEADERS)
                    updateResponseData = updateResponse.json()

                    if "paid" in updateResponseData:
                        if updateResponseData["paid"] is True:
                            authFrame.destroy()
                            callback(root)
                        else:
                            md = MessageDialog(parent=root, title="Autobot Message",
                                               message="You have not paid for your license.",
                                               buttons=["Ok"])
                            md.show()

                            authFrame.destroy()
                            root.destroy()
                            sys.exit(0)
                else:
                    md = MessageDialog(parent=root, title="Autobot Message",
                                       message="Invalid account HWID.",
                                       buttons=["Ok"])
                    md.show()

                    authFrame.destroy()
                    root.destroy()
                    sys.exit(0)
        else:
            md = MessageDialog(parent=root, title="Autobot Message", message=authData["error"]["message"],
                               buttons=["Ok"])
            md.show()

            authFrame.destroy()
            root.destroy()
            sys.exit(0)

    emailLabel = ttb.Label(master=authFrame, text="Email")
    emailLabel.pack(pady=5, padx=5, fill=X, expand=True)
    emailEntry = ttb.Entry(master=authFrame, bootstyle="success")
    emailEntry.insert(0, settings["settings"]["email"])
    emailEntry.pack(pady=5, padx=5, fill=X, expand=True)

    passwordLabel = ttb.Label(master=authFrame, text="Password")
    passwordLabel.pack(pady=5, padx=5, fill=X, expand=True)
    passwordEntry = ttb.Entry(master=authFrame, bootstyle="success", show="*")
    passwordEntry.insert(0, settings["settings"]["password"])
    passwordEntry.pack(pady=5, padx=5, fill=X, expand=True)

    continueButton = ttb.Button(master=authFrame, text="Continue", bootstyle="success", command=setUserKey)
    continueButton.pack(pady=5, padx=5, fill=X, expand=True)

    authFrame.pack(padx=5, pady=50)

    root.update_idletasks()
    root.update()

    root.resizable(False, False)
    root.mainloop()
