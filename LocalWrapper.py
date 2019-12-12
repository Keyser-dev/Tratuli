# File Name: LocalWrapper.py
# Purpose: Creates wrapper functions for os module to meet specific lcoal file system needs of the application.
# Author: Keyser

import os

#=============================================== Functions =====================================================
# Closes program in event of critical local file system error
def exceptionBlanket():
    print('Local error occurred!')
    raise SystemExit
    return

# get and returns the local directory contents of the passed path
def listDir(dir):
    try:
        contents = os.listdir(dir)
    except:
        print("ERROR: Path not valid")
    else:
        return contents

# gets and returns the path of the local current working directory
def currDir():
    try:
        wd = os.getcwd()
    except:
        exceptionBlanket()
    else:
        return wd

# creates a local directory with the specified path
def createDir(dir):
    try:
        os.mkdir(dir)
    except:
        print("ERROR: Path not valid")
    return

# deletes a local directory with the specified path
def delDir(dir):
    try:
        os.rmdir(dir)
    except:
        print("ERROR: Path not valid")
    return

# renames/moves a file from the source path to destination path
def rename(source, dest):
    try:
        os.rename(source, dest)
    except:
        exceptionBlanket()
    return

# checks if specified name is a file
def isFile(file):
    try:
        return os.path.isfile(currDir() + "\\" + file)
    except:
        exceptionBlanket()

# changes local current working directory up one level
def upLevel():
    try:
        os.chdir("..")
    except:
        print("ERROR: Unable to access parent directory")
    return

# changes local current working directory to the specified path
def cwd(dir):
    try:
        os.chdir(dir)
    except:
        print("ERROR: Path not valid")
    return