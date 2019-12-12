# File Name: FTPWrapper.py
# Purpose: Creates wrapper functions for ftplib module to meet specific needs of the application.
# Author: Keyser

from ftplib import FTP
import math
import sys

#=============================================== Variables =====================================================
filenameList = []
progCount = 0
fSize = 0
lSize = 0
calcProg = 0

#=============================================== Functions =====================================================
# Close FTP object and system exit the program
def exceptionBlanket(ftp):
    print('An error occurred!')
    ftp.close()
    raise SystemExit
    return

# create and return FTP object
def createConn():
    ftp = FTP(timeout=5)
    return ftp

# connect to and login to remote FTP server
def connect(ftp, addr, user, password):
    print('Connecting to ' + addr)
    try:
        ftp.connect(addr)
    except:
        print('ERROR: Unable to connect to server')
    else:
        login(ftp, user, password)
    return

# login to remote FTP server
def login(ftp, user, password):
    print('Logging in as ' + user)
    try:
        ftp.login(user, password)
    except:
        print('ERROR: Failed to login to server')
    return

# change to passed directory on remote FTP server
def nav(ftp, dir):
    try:
        ftp.cwd(dir)
    except:
        print('ERROR: Directory not found')
    return

# create list of remote directory/file names
def dirNameList(s):
    filenameList.append(s)

# retrieve remote directory entries line by line
def dirRetNames(ftp):
    try:
        filenameList.clear()
        ftp.retrlines('NLST', dirNameList)
    except:
        print('ERROR: not connected!')
        return []
    return filenameList

# get the size of passed remote file for progress calc
def getFileSize(ftp, file):
    s = 0
    try:
        s = ftp.size(file)
    except:
        print('ERROR: No server support for file size')
        return 0
    return int(s)

# callback function for binary data retrieval in 8192 byte chunks - handles download and upload
# peforms progress calculations
def dataChunk(d, fname, switch):
    global progCount, calcProg, fSize, lSize
    progCount = progCount + 1
    print(progCount)
    print(sys.getsizeof(d))
    if lSize != sys.getsizeof(d) or lSize == 0:
        print('Aberrant progress value')
    else:
        calcProg = float((progCount / math.ceil(fSize / sys.getsizeof(d))) * 100)
    lSize = sys.getsizeof(d)
    print('progress: ' + str(calcProg))
    try:
        if switch == 1:
            with open(fname, 'wb') as fp:
                fp.write(d)
        else:
            pass
    except:
        print('ERROR: File I/O went wrong')

# begins download process of a file from a remote FTP server
def download(ftp, file):
    global progCount, calcProg, fSize, lSize
    progCount = 0
    calcProg = 0
    fSize = getFileSize(ftp, file)
    print('Downloading ' + file)
    try:
        ftp.retrbinary('RETR ' + file, lambda block: dataChunk(block, file, 1), blocksize=8192)
    except:
        exceptionBlanket(ftp)
    else:
        print(file + ' downloaded successfully')
        calcProg = 100
        lSize = 0
    return

# begins upload process of a file to a remote FTP server
def upload(ftp, file):
    global progCount, calcProg, fSize, lSize
    progCount = 0
    calcProg = 0
    fSize = getFileSize(ftp, file)
    print('Uploading ' + file)
    try:
        with open(file, 'rb') as fp:
            ftp.storbinary('STOR ' + file, fp, blocksize=8192, callback=lambda block: dataChunk(block, file, 0))
    except:
        exceptionBlanket(ftp)
    else:
        print(file + ' uploaded successfully')
        calcProg = 100
        lSize = 0
    return

# returns remote FTP server welcome message
def connInfo(ftp):
    try:
        info = ftp.getwelcome()
    except:
        exceptionBlanket(ftp)
    return info

# sends custom FTP command to remote FTP server and returns the response
def cmd(ftp, command):
    try:
        resp = ftp.sendcmd(command)
    except:
        exceptionBlanket(ftp)
    else:
        respParse(resp)
    return resp

# parses server response code for illegal commands
def respParse(code):
    if str(code)[:1] == 4 or str(code)[:1] == 5:
        print('Server command not accepted')
    return