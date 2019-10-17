from ftplib import FTP

# Temporary blanket coverage for all exceptions
# Close FTP object and system exit the program
def exceptionBlanket(ftp):
    print('An error occurred!')
    ftp.close()
    raise SystemExit
    return

def createConn():
    ftp = FTP()
    return ftp

def connect(ftp, addr, user, password):
    print('Connecting to ' + addr)
    try:
        ftp.connect(addr)
    except:
        exceptionBlanket(ftp)
    else:
        login(ftp, user, password)
    return

def login(ftp, user, password):
    print('Logging in as ' + user)
    try:
        ftp.login(user, password)
    except:
        exceptionBlanket(ftp)
    return

def nav(ftp, dir):
    try:
        ftp.cwd(dir)
    except:
        exceptionBlanket(ftp)
    return

def dirRet(ftp):
    try:
        ftp.retrlines('LIST')
    except:
        exceptionBlanket(ftp)
    return

def download(ftp, file):
    print('Downloading ' + file)
    try:
        with open(file, 'wb') as fp:
            ftp.retrbinary('RETR ' + file, fp.write)
    except:
        exceptionBlanket(ftp)
    else:
        print(file + ' downloaded successfully')
    return

def upload(ftp, file):
    print('Uploading ' + file)
    try:
        with open(file, 'rb') as fp:
            ftp.storbinary('STOR ' + file, fp)
    except:
        exceptionBlanket(ftp)
    else:
        print(file + ' uploaded successfully')
    return

def connInfo(ftp):
    try:
        info = ftp.getwelcome()
    except:
        exceptionBlanket(ftp)
    return info

def cmd(ftp, command):
    try:
        resp = ftp.sendcmd(command)
    except:
        exceptionBlanket(ftp)
    else:
        respParse(resp)
    return resp

def respParse(code):
    if str(code)[:1] == 4 or str(code)[:1] == 5:
        print('Server command not accepted')
    return