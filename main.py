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
        self.add_widget(Label(text='Shared Secret Value', size_hint=(.5, .05), pos=(20, 1120)))
        self.shared_secret_value = TextInput(password=True, multiline=False, size_hint=(.46, .10), pos=(20, 1000))
        self.add_widget(self.shared_secret_value)

        self.add_widget(Label(text='Mode', size_hint=(.5, .05), pos=(20, 900)))
        client_button = ToggleButton(text='Client', group='Mode', size_hint=(.22, .05), pos=(20, 800))
        server_button = ToggleButton(text='Server', group='Mode', state='down', size_hint=(.22, .05), pos=(400, 800))
        self.add_widget(client_button)
        self.add_widget(server_button)

        self.add_widget(Label(text='TCP Connection', size_hint=(.5, .05), pos=(20, 700)))
        self.add_widget(Button(text='Open Connection', size_hint=(.22, .05), pos=(20, 600)))
        self.add_widget(Button(text='Close Connection', size_hint=(.22, .05), pos=(400, 600)))
        
        self.add_widget(Label(text='Data To Be Sent', size_hint=(.44, .05), pos=(20, 500)))
        self.data_to_send = TextInput(password=False, multiline=True, size_hint=(.46, .15), pos=(20, 300))
        self.add_widget(self.data_to_send)
        self.add_widget(Button(text='Send Data', size_hint=(.46, .05), pos=(20, 200)))

        self.add_widget(Label(text='Console', size_hint=(.4, .05), pos=(800, 1120)))
        self.console = TextInput(password=False, multiline=True, size_hint=(.47, .8), pos=(800, 100))
        self.add_widget(self.console)
        self.add_widget(Button(text='Continue', size_hint=(.47, .05), pos=(800, 10)))
        

class MyApp(App):

    def build(self):
        init = InitScreen()
        return init

if __name__ == '__main__':
    MyApp().run()