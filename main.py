import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout

class InitScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(InitScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Shared Secret Value', size_hint=(None, None), pos_hint={'top':0.95, 'right':0.3}))
        self.shared_secret_value = TextInput(password=True, multiline=False, size_hint=(0.46, 0.15), pos_hint={'top':0.85, 'right':0.5})
        self.add_widget(self.shared_secret_value)

        self.add_widget(Label(text='Mode', size_hint=(0.5, 0.05), pos_hint={'top':0.70, 'right':0.5}))
        client_button = ToggleButton(text='Client', group='Mode', size_hint=(.22, .05), pos_hint={'top':0.60, 'right':0.25})
        server_button = ToggleButton(text='Server', group='Mode', state='down', size_hint=(.22, .05), pos_hint={'top':0.60, 'right':0.5})
        self.add_widget(client_button)
        self.add_widget(server_button)

        self.add_widget(Label(text='TCP Connection', size_hint=(.5, .05), pos_hint={'top':0.50, 'right':0.5}))
        self.add_widget(Button(text='Open Connection', size_hint=(.22, .05), pos_hint={'top':0.40, 'right':0.25}))
        self.add_widget(Button(text='Close Connection', size_hint=(.22, .05), pos_hint={'top':0.40, 'right':0.5}))
        
        self.add_widget(Label(text='Data To Be Sent', size_hint=(.5, .05), pos_hint={'top':0.30, 'right':0.5}))
        self.data_to_send = TextInput(password=False, multiline=True, size_hint=(.46, .15), pos_hint={'top':0.25, 'right':0.5})
        self.add_widget(self.data_to_send)
        self.add_widget(Button(text='Send Data', size_hint=(.46, .05), pos_hint={'top':0.07, 'right':0.5}))

        self.add_widget(Label(text='Console', size_hint=(.4, .05), pos_hint={'top':0.95, 'right':0.95}))
        self.console = TextInput(password=False, multiline=True, size_hint=(.40, .8), pos_hint={'top':0.90, 'right':0.95})
        self.add_widget(self.console)
        self.add_widget(Button(text='Continue', size_hint=(.40, .05), pos_hint={'top':0.07, 'right':0.95}))
        

class MyApp(App):

    def build(self):
        init = InitScreen()
        return init

if __name__ == '__main__':
    MyApp().run()