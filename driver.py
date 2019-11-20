import Window
import globals
import FTPWrapper as fw
import LocalWrapper as lw
import AddressBook as ab

if __name__ == '__main__':
    Window.Application().run()

#------------- CLI -------------

def getInput(message):
    i = input(message)
    return i

#------------- REMOTE -------------
def servInfo():
    print(fw.connInfo(ftp))
    return

def listDir():
    fw.dirRet(ftp)
    getInput('Press enter for menu')
    return

def changeDir():
    fw.nav(ftp, getInput('Please enter directory: '))
    return

def dl():
    file = getInput('Please enter name of file: ')
    fw.download(ftp, file)
    return

def ul():
    file = getInput('Please enter name of file: ')
    fw.upload(ftp, file)
    return

def stop():
    fw.exceptionBlanket(ftp)
    return

def menuRemote():
    fw.connect(ftp, globals.vars[0], globals.vars[1], globals.vars[2])
    servInfo()
    while True:
        print('\n\n' + fw.cmd(ftp, 'PWD'))
        print(
            '0 - Server info, 1 - Directory contents, 2 - Change directory, 3 - Download file, 4 - Upload file, 5 - Local, 6 - Exit')
        inVar = int(getInput('>'))
        if inVar == 5:
            break
        ftpmenu[inVar]()
    menuLocal()
    return

#------------- LOCAL -------------
def listLocal():
    print(lw.listDir(getInput('Please enter directory: ')))
    getInput('Press enter for menu')
    return

def changeLocal():
    lw.cwd(getInput('Please enter directory: '))
    return

def renameLocal():
    lw.rename(getInput('Please enter source: '), getInput('Please enter destination: '))
    return

def deleteLocal():
    lw.delDir(getInput('Please enter directory: '))
    return

def menuLocal():
    while True:
        print('\n\n' + lw.currDir())
        print('0 - Directory contents, 1 - Change directory, 2 - Rename, 3 - Delete directory, 4 - Remote, 5 - Exit')
        inVar = int(getInput('>'))
        if inVar == 4:
            break
        localmenu[inVar]()
    menuRemote()
    return

localmenu = {0 : listLocal,
             1 : changeLocal,
             2 : renameLocal,
             3 : deleteLocal,
             4 : menuRemote,
             5 : stop
}

ftpmenu = {0 : servInfo,
        1 : listDir,
        2 : changeDir,
        3 : dl,
        4 : ul,
        5 : menuLocal,
        6 : stop
}

ab.deserialize()

print("Tratuli - FTP client CLI")
ftp = fw.createConn()
menuRemote()