import getpass
import hashlib
import os
import uuid

import getmac as gma
import requests
import ttkbootstrap as ttb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import MessageDialog

userHWID = hashlib.sha256(
    (os.name + getpass.getuser() + gma.get_mac_address() + str(hex(uuid.getnode()))).encode()).hexdigest()


def runAuthWindow(root, callback):
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

        if "error" not in authData:
            userId = authData["user"]["id"]

            HEADERS = {"Authorization": "Bearer %s" % authData["jwt"]}

            updateResponse = requests.put(url="%s%s%s" % (URL, "/api/users/", userId), data={"hwid": "%s" % userHWID},
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
                    exit()
        else:
            md = MessageDialog(parent=root, title="Autobot Message", message=authData["error"]["message"],
                               buttons=["Ok"])
            md.show()

            authFrame.destroy()
            exit()

    emailLabel = ttb.Label(master=authFrame, text="Email")
    emailLabel.pack(pady=5, padx=5, fill=X, expand=True)
    emailEntry = ttb.Entry(master=authFrame, bootstyle="success")
    emailEntry.pack(pady=5, padx=5, fill=X, expand=True)

    passwordLabel = ttb.Label(master=authFrame, text="Password")
    passwordLabel.pack(pady=5, padx=5, fill=X, expand=True)
    passwordEntry = ttb.Entry(master=authFrame, bootstyle="success", show="*")
    passwordEntry.pack(pady=5, padx=5, fill=X, expand=True)

    continueButton = ttb.Button(master=authFrame, text="Continue", bootstyle="success", command=setUserKey)
    continueButton.pack(pady=5, padx=5, fill=X, expand=True)

    authFrame.pack(padx=5, pady=50)

    root.update_idletasks()
    root.update()

    root.resizable(False, False)
    root.mainloop()