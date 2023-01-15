import subprocess
import tkinter
from os import path
from tkinter.constants import *

import customtkinter as ctk
import requests
from PIL import Image
from src.utils.userHWID import getUserHWID

import src.utils.configFile as configFile

ctk.set_default_color_theme("green")

userHWID = getUserHWID()


class AuthWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.configuration = configFile.getConfiguration()

        # configure window
        self.title("Autobot")
        self.iconbitmap(path.join("src", "assets", "logo.ico"))
        self.resizable(False, False)

        self.authFrame = ctk.CTkFrame(
            self,
            fg_color="#171717",
            corner_radius=0
        )
        self.loginCardBorder = ctk.CTkFrame(
            self.authFrame,
            fg_color="#404040",
            corner_radius=5
        )
        self.loginCard = ctk.CTkFrame(
            self.loginCardBorder,
            fg_color="#262626",
            corner_radius=4
        )

        self.loginLogo = ctk.CTkLabel(
            self.loginCard,
            text="",
            image=ctk.CTkImage(
                light_image=Image.open("src/assets/logo.png"),
                dark_image=Image.open("src/assets/logo.png"),
                size=(90, 90))
        )
        self.loginLogo.pack(
            padx=100,
            pady=(20, 10)
        )

        authFile = open("data/auth.txt", "r")
        data = authFile.read()
        userEmail = data.split(":")[0]
        userPassword = data.split(":")[1]

        self.loginLabel = ctk.CTkLabel(
            self.loginCard,
            text="Log In",
            text_color="white",
            font=("Arial", 24, "bold")
        )
        self.loginLabel.pack()

        self.loginEmailVar = tkinter.StringVar(
            self,
            value=userEmail
        )

        self.loginEmailLabel = ctk.CTkLabel(self.loginCard, text="Email", text_color="white")
        self.loginEmailLabel.pack(anchor=W, padx=(20, 0), pady=(30, 5))
        self.loginEmailEntry = ctk.CTkEntry(
            self.loginCard,
            textvariable=self.loginEmailVar,
            fg_color="#171717",
            text_color="white",
            border_width=1,
            border_color="#404040",
            corner_radius=5)
        self.loginEmailEntry.pack(
            pady=(0, 5),
            padx=20,
            expand=True,
            fill=X
        )

        self.loginPasswordVar = tkinter.StringVar(
            self,
            value=userPassword
        )

        self.loginPasswordLabel = ctk.CTkLabel(self.loginCard, text="Password", text_color="white")
        self.loginPasswordLabel.pack(anchor=W, padx=(20, 0), pady=(0, 5))
        self.loginPasswordEntry = ctk.CTkEntry(
            self.loginCard,
            show="*",
            textvariable=self.loginPasswordVar,
            fg_color="#171717",
            text_color="white",
            border_width=1,
            border_color="#404040",
            corner_radius=5
        )
        self.loginPasswordEntry.pack(
            pady=(0, 30),
            padx=20,
            expand=True,
            fill=X
        )

        self.loginButton = ctk.CTkButton(self.loginCard, text="Login", text_color="white", fg_color="#191919",
                                         command=self.login)
        self.loginButton.pack(pady=(0, 20), padx=20, expand=True, fill=X)

        self.loginCard.pack(
            padx=1,
            pady=1
        )
        self.loginCardBorder.pack(
            padx=20,
            pady=50
        )
        self.authFrame.pack(
            padx=0,
            pady=0
        )

    def login(self):
        userEmail = self.loginEmailVar.get()
        userPassword = self.loginPasswordVar.get()

        URL = "http://197.81.132.129:1337"
        DATA = {"identifier": "%s" % userEmail.strip(), "password": "%s" % userPassword.strip()}

        authResponse = requests.post(url="%s%s" % (URL, "/api/auth/local"), data=DATA)

        authData = authResponse.json()

        if "error" not in authData:
            authFile = open("data/auth.txt", "w")
            authFile.write('%s:%s' % (userEmail, userPassword))
            authFile.flush()
            authFile.close()

            userId = authData["user"]["id"]

            HEADERS = {"Authorization": "Bearer %s" % authData["jwt"]}

            accountResponse = requests.get(url="%s%s%s" % (URL, "/api/users/", userId), headers=HEADERS)
            accountResponseData = accountResponse.json()

            if "hwid" in accountResponseData:
                if accountResponseData["hwid"] == "" or accountResponseData["hwid"] is None or \
                        accountResponseData["hwid"] == userHWID:
                    updateResponse = requests.put(url="%s%s%s" % (URL, "/api/users/", userId),
                                                  data={"hwid": "%s" % userHWID},
                                                  headers=HEADERS)
                    updateResponseData = updateResponse.json()

                    if "paid" in updateResponseData:
                        if updateResponseData["paid"] is not True:
                            dialog = ctk.CTkToplevel(self)
                            dialog.title("Autobot")
                            dialog.iconbitmap(path.join("src", "assets", "logo.ico"))
                            dialog.resizable(False, False)

                            dialogFrame = ctk.CTkFrame(dialog, fg_color="#191919", corner_radius=0)
                            dialogFrame.pack()

                            dialogMessage = ctk.CTkLabel(dialogFrame, text="You need to pay your license.", text_color="white")
                            dialogMessage.pack(padx=20, pady=(20, 10))

                            okButton = ctk.CTkButton(dialogFrame, text="Ok", command=dialog.destroy)
                            okButton.pack(side=RIGHT, padx=(10, 20), pady=(0, 20))
                        else:
                            sessionFile = open("data/session.txt", "w")
                            sessionFile.write(authData["jwt"])
                            sessionFile.flush()
                            sessionFile.close()

                            self.destroy()
                    else:
                        dialog = ctk.CTkToplevel(self)
                        dialog.title("Autobot")
                        dialog.iconbitmap(path.join("src", "assets", "logo.ico"))
                        dialog.resizable(False, False)

                        dialogFrame = ctk.CTkFrame(dialog, fg_color="#191919", corner_radius=0)
                        dialogFrame.pack()

                        dialogMessage = ctk.CTkLabel(dialogFrame, text="Your pc is invalid.", text_color="white")
                        dialogMessage.pack(padx=20, pady=(20, 10))

                        okButton = ctk.CTkButton(dialogFrame, text="Ok", command=dialog.destroy)
                        okButton.pack(side=RIGHT, padx=(10, 20), pady=(0, 20))
                else:
                    dialog = ctk.CTkToplevel(self)
                    dialog.title("Autobot")
                    dialog.iconbitmap(path.join("src", "assets", "logo.ico"))
                    dialog.resizable(False, False)

                    dialogFrame = ctk.CTkFrame(dialog, fg_color="#191919", corner_radius=0)
                    dialogFrame.pack()

                    dialogMessage = ctk.CTkLabel(dialogFrame, text="Your pc is invalid.", text_color="white")
                    dialogMessage.pack(padx=20, pady=(20, 10))

                    okButton = ctk.CTkButton(dialogFrame, text="Ok", command=dialog.destroy)
                    okButton.pack(side=RIGHT, padx=(10, 20), pady=(0, 20))
            else:
                dialog = ctk.CTkToplevel(self)
                dialog.title("Autobot")
                dialog.iconbitmap(path.join("src", "assets", "logo.ico"))
                dialog.resizable(False, False)

                dialogFrame = ctk.CTkFrame(dialog, fg_color="#191919", corner_radius=0)
                dialogFrame.pack()

                dialogMessage = ctk.CTkLabel(dialogFrame, text="Your pc is invalid.", text_color="white")
                dialogMessage.pack(padx=20, pady=(20, 10))

                okButton = ctk.CTkButton(dialogFrame, text="Ok", command=dialog.destroy)
                okButton.pack(side=RIGHT, padx=(10, 20), pady=(0, 20))
        else:
            print(authData["error"]["message"])

            dialog = ctk.CTkToplevel(self)
            dialog.title("Autobot")
            dialog.iconbitmap(path.join("src", "assets", "logo.ico"))
            dialog.resizable(False, False)

            dialogFrame = ctk.CTkFrame(dialog, fg_color="#191919", corner_radius=0)
            dialogFrame.pack()

            dialogMessage = ctk.CTkLabel(dialogFrame, text=authData["error"]["message"], text_color="white")
            dialogMessage.pack(padx=20, pady=(20, 10))

            okButton = ctk.CTkButton(dialogFrame, text="Ok", command=dialog.destroy)
            okButton.pack(side=RIGHT, padx=(10, 20), pady=(0, 20))
