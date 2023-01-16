import os
import win32security


def getUserHWID():
    winuser = os.getlogin()
    sid = win32security.LookupAccountName(None, winuser)[0]
    hwid = win32security.ConvertSidToStringSid(sid)

    return hwid
