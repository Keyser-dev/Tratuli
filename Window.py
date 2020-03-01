# File Name: Window.py
# Purpose: Serves as the bulk of creation for GUI elements and interaction with them.
# Author: Keyser

import threading
import kivy
import AddressBook as ab
import LocalWrapper as lw
import FTPWrapper as fw
kivy.require('1.11.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

# Load Kivy KV file into memory
Builder.load_file('Window.kv')

#=============================================== Variables ====================================================
connections = {}
entryNames = {}
localSelected = {}
remoteSelected = {}
downQueue = []
upQueue = []
queue = "Queue"
ftp = fw.createConn()

#========================================== Kivy Classes ======================================================
# Main Kivy window
class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        global queue
        self.ids.queueBox.text = queue
        self.ids.localNavBut.bind(on_press=lambda x: self.changeDirLocal())
        self.ids.localUpBut.bind(on_press=lambda x: self.upDirLocal())
        self.ids.refreshBut.bind(on_press=lambda x: Application.refreshMain())
        self.ids.remoteNavBut.bind(on_press=lambda x: self.changeDirRemote())
        self.ids.downloadBut.bind(on_press=lambda x: self.downThread())
        self.ids.uploadBut.bind(on_press=lambda x: self.upThread())
        Clock.schedule_interval(self.updateProgress, 1.0 / 30)

    # Dynamically update progress bar
    def updateProgress(self, x):
        self.ids.progBar.value = fw.calcProg

    # Navigate up one local level
    def upDirLocal(self):
        lw.upLevel()
        Application.refreshMain()

    # Navigate local current working directory to provided
    def changeDirLocal(self):
        global localSelected, queue
        print(localSelected)
        print(str(lw.isFile(localSelected[next(iter(localSelected))]['text'])))
        if len(localSelected.keys()) > 1 or len(localSelected.keys()) < 1 or \
                lw.isFile(localSelected[next(iter(localSelected))]['text']) == True:
            queue = queue + '\nPlease select only a directory'
            self.ids.queueBox.text = queue
            return
        lw.cwd(localSelected[next(iter(localSelected))]['text'])
        Application.refreshMain()

    # Navigate remote working directory to provided
    def changeDirRemote(self):
        global ftp, remoteSelected, queue
        print(remoteSelected)
        if len(remoteSelected.keys()) > 1 or len(remoteSelected.keys()) < 1:
            queue = queue + '\nPlease select only a directory'
            self.ids.queueBox.text = queue
            return
        fw.nav(ftp, remoteSelected[next(iter(remoteSelected))]['text'])
        Application.refreshMain()

    # create download thread
    def downThread(self):
        self.t1 = threading.Thread(target=self.download, args=())
        if self.t1.isAlive():
            self.t1.join()
        self.t1.start()

    # create upload thread
    def upThread(self):
        self.t2 = threading.Thread(target=self.upload, args=())
        if self.t2.isAlive():
            self.t2.join()
        self.t2.start()

    # create download queue then download from it
    def download(self):
        global downQueue, ftp, queue
        for x in remoteSelected.values():
            downQueue.append(str(x['text']))
        self.updateQueue()

        for f in downQueue:
            fw.download(ftp, f)
            Application.refreshMain()

        downQueue.clear()
        queue = queue + '\nDownloads complete'
        self.ids.queueBox.text = queue
        Application.refreshMain()

    # create upload queue then upload from it
    def upload(self):
        global upQueue, ftp, queue
        for x in localSelected.values():
            upQueue.append(str(x['text']))
        self.updateQueue()

        for f in upQueue:
            fw.upload(ftp, f)
            Application.refreshMain()

        upQueue.clear()
        queue = queue + '\nUploads complete'
        self.ids.queueBox.text = queue

    # update queue GUI element as down/uploads progress
    def updateQueue(self):
        global queue
        for x in downQueue:
            queue = queue + '\nDownloading - ' + x
            self.ids.queueBox.text = queue

        for x in upQueue:
            queue = queue + '\nUploading - ' + x
            self.ids.queueBox.text = queue

#======================================= Local File Browsing =====================================================
# Kivy specific local layout without overriding
class FileLocalLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass

# selectable label interaction for local file system
class FileLocalLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    # override Kivy function to pass local data attributes
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(FileLocalLabel, self).refresh_view_attrs(
            rv, index, data)

    # override Kivy function to create local selection capability
    def on_touch_down(self, touch):
        if super(FileLocalLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    # override Kivy function to define local selection behavior - adding to local list of entries
    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        global localSelected
        if is_selected:
            localSelected[index] = rv.data[index]
        else:
            try:
                localSelected.pop(index)
            except:
                print("ERROR: Unable to remove item " + str(index) + " " + str(rv.data[index]))

# create Kivy specific view - declaring data read from local file system
class FileLocal(RecycleView):
    def __init__(self, **kwargs):
        super(FileLocal, self).__init__(**kwargs)
        curLocalDirList = lw.listDir(lw.currDir())
        self.data.clear()
        self.data = [{'text': str(x)} for x in curLocalDirList]

#========================================= Remote File Browsing ==================================================
# Kivy specific remote layout without overriding
class FileRemoteLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass

# selectable label interaction for remote file system
class FileRemoteLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    # override Kivy function to pass remote data attributes
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(FileRemoteLabel, self).refresh_view_attrs(
            rv, index, data)

    # override Kivy function to create remote selection capability
    def on_touch_down(self, touch):
        if super(FileRemoteLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    # override Kivy function to define remote selection behavior - adding to remote list of entries
    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        global remoteSelected
        if is_selected:
            remoteSelected[index] = rv.data[index]
        else:
            try:
                remoteSelected.pop(index)
            except:
                print("ERROR: Unable to remove item " + str(index) + " " + str(rv.data[index]))

# create Kivy specific view - declaring data retrieval from remote file system
class FileRemote(RecycleView):
    def __init__(self, **kwargs):
        super(FileRemote, self).__init__(**kwargs)
        global ftp
        curRemoteDirList = fw.dirRetNames(ftp)
        self.data.clear()
        self.data = [{'text': str(x)} for x in curRemoteDirList]

#============================================ Address Book ======================================================
#  Kivy screen for Address Book
class AddressBook(Screen):
    def __init__(self, **kwargs):
        super(AddressBook, self).__init__(**kwargs)
        self.ids.bookConnect.bind(on_press=lambda x: self.connect())
        self.ids.bookSaveNew.bind(on_press=lambda x: self.saveNewEntry())
        self.ids.bookDelete.bind(on_press=lambda x: self.deleteEntry())

    # connect to remote FTP server using entry field data
    def connect(self):
        global ftp
        fw.connect(ftp, self.ids.bookAddr.text, self.ids.bookUser.text, self.ids.bookPass.text)

    # get entry field data and save as new connection
    def saveNewEntry(self):
        rawEntry = []
        rawEntry.append(self.ids.bookName.text)
        rawEntry.append(self.ids.bookAddr.text)
        rawEntry.append(self.ids.bookPort.text)
        rawEntry.append(self.ids.bookUser.text)
        rawEntry.append(self.ids.bookPass.text)
        rawEntry.append(self.ids.bookNotes.text)
        global connections
        connections = ab.addEntry(rawEntry, connections)
        ab.serialize(connections)
        refreshAddr()

    # iterate entries to user selected and destroy - serialize new data set
    def deleteEntry(self):
        count = 0
        for x in entryNames:
            if count == curEntry:
                print('popping at ' + str(count) + ' for ' + str(connections[x]))
                connections.pop(x)
                break
            count = count + 1
        ab.serialize(connections)
        refreshAddr()

# selectable label interaction for address book
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass

# selectable label interaction for address book
class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    # override Kivy function to pass address book attributes
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    # override Kivy function to create address book entry selection capability
    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    # override Kivy function to define address book selection behavior
    # displays retrieved connection information in corresponding text entry fields
    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            global curEntry
            curEntry = index
            count = 0
            for x in entryNames:
                if count == curEntry:
                    self.parent.parent.parent.parent.ids.bookName.text = connections[x][0]['name']
                    self.parent.parent.parent.parent.ids.bookAddr.text = connections[x][0]['address']
                    self.parent.parent.parent.parent.ids.bookPort.text = connections[x][0]['port']
                    self.parent.parent.parent.parent.ids.bookUser.text = connections[x][0]['user']
                    self.parent.parent.parent.parent.ids.bookPass.text = connections[x][0]['password']
                    self.parent.parent.parent.parent.ids.bookNotes.text = connections[x][0]['note']
                    break
                count = count + 1
        else:
            pass

# create Kivy specific view - populating the address book
class Addresses(RecycleView):
    def __init__(self, **kwargs):
        super(Addresses, self).__init__(**kwargs)
        for e in connections:
            key = str(e)
            entryNames[key] = (str(connections[key][0]['name']))

        self.data.clear()
        self.data = [{'text': str(x)} for x in entryNames.values()]

#========================================= Common Functions =====================================================
# deserializes persistent JSON data and returns to memory object
def loadAddressBook():
    return ab.deserialize()

# refreshes AddressBook screen
def refreshAddr():
    sm.remove_widget(sm.get_screen(sm.current))
    connections = loadAddressBook()
    entryNames.clear()
    sm.add_widget(AddressBook(name='AddressBook'))
    sm.current = 'AddressBook'

#===================================== Application Prep and Start ================================================

connections = loadAddressBook()
curEntry = ""

# define and setup ScreenManager
sm = ScreenManager(transition=NoTransition())
sm.add_widget(MainWindow(name='MainWindow'))
sm.add_widget(AddressBook(name='AddressBook'))

# main driving app
class Application(App):
    # build the application and launch into ScreenManager object
    def build(self):
        self.title = 'Tratuli'
        self.icon = 'resources\\icon.png'
        return sm

    # refreshes MainWindow screen
    def refreshMain(*_):
        sm.remove_widget(sm.get_screen(sm.current))
        localSelected.clear()
        remoteSelected.clear()
        sm.add_widget(MainWindow(name='MainWindow'))
        sm.current = 'MainWindow'