import subprocess

def getUserHWID():
    productOutput = subprocess.getoutput("wmic csproduct get")
    productOutputRows = productOutput.split("\n")
    productOutputCols = productOutputRows[2].split(" ")

    return productOutputCols[27]
