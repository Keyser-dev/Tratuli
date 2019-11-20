#import pywin32_system32
import globals
import kivy
import AddressBook as ab
kivy.require('1.11.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

Builder.load_file('Window.kv')

class ConnectionInfo(Screen):
    def __init__(self, **kwargs):
        super(ConnectionInfo, self).__init__(**kwargs)
        self.ids.connBut.bind(on_press=lambda x: self.connect())

    def connect(self,):
        globals.vars.append(self.ids.addr.text)
        globals.vars.append(self.ids.user.text)
        globals.vars.append(self.ids.passw.text)

class AddressBook(Screen):
    def __init__(self, **kwargs):
        super(AddressBook, self).__init__(**kwargs)
        self.ids.bookSaveNew.bind(on_press=lambda x: self.saveNewEntry())
        self.data = [{'text': str(x)} for x in range(100)]

    def saveNewEntry(self):
        rawEntry = []
        rawEntry.append(self.ids.bookName.text)
        rawEntry.append(self.ids.bookAddr.text)
        rawEntry.append(self.ids.bookPort.text)
        rawEntry.append(self.ids.bookUser.text)
        rawEntry.append(self.ids.bookPass.text)
        rawEntry.append(self.ids.bookNotes.text)
        ab.addEntry(rawEntry)

    def loadAddressBook(self):
        entries = ab.deserialze()

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    #data = [{'text': str(x)} for x in range(100)]

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

#class Addresses(RecycleView):
    #def __init__(self, **kwargs):
        #super(Addresses, self).__init__(**kwargs)
        #self.data = [{'text': str(x)} for x in range(100)]

sm = ScreenManager()
sm.add_widget(ConnectionInfo(name='ConnectionInfo'))
sm.add_widget(AddressBook(name='AddressBook'))
#sm.add_widget(Addresses(name='Addresses'))

class Application(App):
    def build(self):
        self.title = 'Tratuli'
        return sm
