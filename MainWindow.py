#import pywin32_system32
import globals
import kivy
kivy.require('1.11.0')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

class ConnectionInfo(GridLayout):

    def __init__(self, **kwargs):
        super(ConnectionInfo, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text='Address'))
        self.address = TextInput(multiline=False)
        self.add_widget(self.address)

        self.add_widget(Label(text='Username'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.btn = Button(text='OK')
        self.btn.bind(on_press=self.buttonClicked)
        self.add_widget(self.btn)

    def buttonClicked(self, btn):
        #I know. Globals are ugly. It's only temporary for testing
        globals.vars.append(self.address.text)
        globals.vars.append(self.username.text)
        globals.vars.append(self.password.text)
        App.get_running_app().stop()

class Application(App):

    def build(self):
        self.title = 'Tratuli'
        return ConnectionInfo()