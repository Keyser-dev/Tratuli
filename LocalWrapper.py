import os

# Temporary blanket coverage for all exceptions
# Closes program
def exceptionBlanket():
    print('Local error occurred!')
    raise SystemExit
    return

def listDir(dir):
    try:
        contents = os.listdir(dir)
    except:
        exceptionBlanket()
    else:
        return contents

def currDir():
    try:
        wd = os.getcwd()
    except:
        exceptionBlanket()
    else:
        return wd

def createDir():
    try:
        os.mkdir(dir)
    except:
        exceptionBlanket()
    return

def delDir(dir):
    try:
        os.rmdir(dir)
    except:
        exceptionBlanket()
    return

def rename(source, dest):
    try:
        os.rename(source, dest)
    except:
        exceptionBlanket()
    return

def cwd(dir):
    try:
        os.chdir(dir)
    except:
        exceptionBlanket()
    return