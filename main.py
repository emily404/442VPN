import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from functools import partial
import socket
import threading
import sys

import cbc as CBC
from mutual_auth import MutualAuth
from diffie_hellman import DiffieHellman

class InitScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(InitScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Shared Secret Value', size_hint=(None, None), pos_hint={'top':0.95, 'right':0.3}))
        self.shared_secret_value = TextInput(password=False, multiline=False, size_hint=(0.46, 0.10), pos_hint={'top':0.88, 'right':0.5})
        self.add_widget(self.shared_secret_value)
        send_secret_button = Button(text='Use Secret', size_hint=(.46, .05), pos_hint={'top':0.75, 'right':0.5})
        self.add_widget(send_secret_button)


        self.add_widget(Label(text='Mode', size_hint=(0.5, 0.05), pos_hint={'top':0.65, 'right':0.5}))
        client_button = ToggleButton(text='Client', group='Mode', size_hint=(.22, .05), pos_hint={'top':0.60, 'right':0.25})
        server_button = ToggleButton(text='Server', group='Mode', state='down', size_hint=(.22, .05), pos_hint={'top':0.60, 'right':0.5})
        self.add_widget(client_button)
        self.add_widget(server_button)

        self.add_widget(Label(text='TCP Connection', size_hint=(.5, .05), pos_hint={'top':0.50, 'right':0.5}))
        open_connection_button  = Button(text='Open Connection', size_hint=(.22, .05), pos_hint={'top':0.40, 'right':0.25})
        close_connection_button = Button(text='Close Connection', size_hint=(.22, .05), pos_hint={'top':0.40, 'right':0.5})
        self.add_widget(open_connection_button)
        self.add_widget(close_connection_button)
        
        self.add_widget(Label(text='Data To Be Sent', size_hint=(.5, .05), pos_hint={'top':0.30, 'right':0.5}))
        self.data_to_send = TextInput(password=False, multiline=True, size_hint=(.46, .15), pos_hint={'top':0.25, 'right':0.5})
        self.add_widget(self.data_to_send)
        send_data_button = Button(text='Send Data', size_hint=(.46, .05), pos_hint={'top':0.07, 'right':0.5}, disabled='true')
        self.add_widget(send_data_button)

        self.add_widget(Label(text='Console', size_hint=(.4, .05), pos_hint={'top':0.95, 'right':0.95}))
        self.console = TextInput(password=False, multiline=True, size_hint=(.40, .9), pos_hint={'top':0.90, 'right':0.95})
        self.add_widget(self.console)
        
        self.server_button = server_button
        self.send_data_button = send_data_button
        self.open_connection_button = open_connection_button

        # bind event handlers
        open_connection_button.bind(on_press=partial(self.connectionPrompt))
        close_connection_button.bind(on_press=self.closeConnection)
        send_secret_button.bind(on_press=self.useSharedSecret)
        send_data_button.bind(on_press=self.sendData)


    def connectionPrompt(self, obj):
        prompt    = BoxLayout(size=(250,250),orientation="vertical",spacing=20,padding=20)
        self.mode = 'server' if self.server_button.state == 'down' else 'client'

        if self.mode == 'client':
            self.host_input = TextInput(size_hint=(.8,.15))
            prompt.add_widget(Label(text='Host:',size_hint=(.7,.1)))
            prompt.add_widget(self.host_input)

        self.port_input = TextInput(size_hint=(.8,.15))    
        prompt.add_widget(Label(text='Port:',size_hint=(.7,.1)))
        prompt.add_widget(self.port_input)

        connect_button = Button(text='Connect',size_hint=(.4,.1),pos_hint={'right':.7})
        self.connect_button= connect_button
        prompt.add_widget(connect_button)

        popup = Popup(title='Connect',content=prompt, size_hint=(.5,.5)) 
        self.connection_popup = popup
        popup.open()

        connect_button.bind(on_press=self.connect)

    def connectThread(self):
        #todo: host and port input validation

        if self.mode == 'client':
            sock = self.clientConnect(socket.gethostname(), 7677)
        else:
            sock = self.serverConnect(7677)
        
        # if self.mode == 'client':
        #     sock = self.clientConnect(self.host_input.text, int(self.port_input.text))
        # else:
        #     sock = self.serverConnect(int(self.port_input.text))

        self.connection_popup.dismiss()

        if not sock:
            return

        self.socket = sock  
        self.open_connection_button.disabled = True

        # todo: mutual authentication
        
        # receive messages
        # while 1:
        #     #todo: how much to receive?
        #     data = self.socket.recv(5)
        #     if data:
        #         self.console.text = self.console.text + '\n' + 'Text received:' + data

    def messageReceivingService(self):
        recieved = self.receiveData()
        #TODO: add stuff like HMAC, DH etc etc etc
        print "cipherText received: " + received.encode("hex_codec")
        plainText = CBC.decrypt(self.cipher, recieved)
        print "plainText received: " + plainText


    def receiveData(self):
        data = ''
        newchar = ''
        five_terminators = '\0\0\0\0\0'
        last_five = 'abcde' 

        while last_five != five_terminators:
            #todo: how much to receive?
            newchar = self.socket.recv(1)
            data = data + newchar
            if(len(data) > 5):
                last_five = data[len(data)-5:]
            else:
                last_five = 'abcde' 

        # self.console.text = self.console.text + '\n' + 'Text received:' + data
        print 'data received:'+data[:len(data)-5]
        return data[:len(data)-5]

    def mutualAuthentication(self):
        bits = 16
        nonce = self.mutual_auth.generate_nonce(bits)
        five_terminators = '\0\0\0\0\0'

        # print 'nonce generated:' + str(nonce)
        
        if self.mode == 'client':
            self.socket.sendall('im alice,' + str(nonce)+five_terminators)

            server_response = self.receiveData()
            server_nonce = server_response.split(',')[0]
            server_encrypted = server_response.split(',')[1]
            
            plaintext = self.mutual_auth.decrypt_ciphertext(server_encrypted)
            if(not self.mutual_auth.check_name(plaintext) and self.mutual_auth.check_nonce(plaintext)):
                #client
                server_partial_session_key = self.mutual_auth.get_partner_dh_value(plaintext)
                dh = DiffieHellman.defaultInstance()
                client_partial_session_key = dh.partialSessionKeyGen()[0]
                self.total_session_key = dh.computeTotalSessionKey(server_partial_session_key)
                print 'client total session key:' + str(self.total_session_key)

                encrypted = self.mutual_auth.encrypt_nonce(server_nonce, client_partial_session_key)
                self.socket.sendall(encrypted+five_terminators)
                print 'success in authenticating server'
                threading.Thread(target=self.messageReceivingService).start()

                return True
            else:
                print 'cannot authenticate server, check falied'
                return False

        else:
            #server
            client_response = self.receiveData()
            client_nonce = client_response.split(',')[1]
            # print 'client_nonce:'+str(client_nonce)

            dh = DiffieHellman.defaultInstance()
            server_partial_session_key = dh.partialSessionKeyGen()[0]

            encrypted = self.mutual_auth.encrypt_nonce(client_nonce, server_partial_session_key)
            self.socket.sendall(str(nonce)+','+encrypted+five_terminators)
            # print 'server sending nonce and encrypted:' + str(nonce)+','+encrypted

            client_second_response = self.receiveData()
            # print 'client_second_response:' + str(client_second_response)
            threading.Thread(target=self.messageReceivingService).start()
            plaintext = self.mutual_auth.decrypt_ciphertext(client_second_response)
            if(not self.mutual_auth.check_name(plaintext) and self.mutual_auth.check_nonce(plaintext)):
                client_partial_session_key = self.mutual_auth.get_partner_dh_value(plaintext)
                self.total_session_key = dh.computeTotalSessionKey(client_partial_session_key)
                print 'server total session key:' + str(self.total_session_key)
                print 'success in authenticating client'
                return True    
            else:
                print 'cannot authenticate client, check falied'
                return False
            
            
        
    def useSharedSecret(self, obj):
        # if(self.shared_secret_value.text != ''):
            # self.mutual_auth = MutualAuth(self.shared_secret_value.text, self.mode)
        
        self.mutual_auth = MutualAuth('secretsecretsecretsecret', self.mode)
         
        if(self.mutualAuthentication()):    
            self.send_data_button.disabled = False

    
    def connect(self, obj):
        self.connect_button.text = "Connecting..."
        self.connect_button.disabled = True

        threading.Thread(target=self.connectThread).start()

    def closeConnection(self, obj):
        self.socket.close()
        
        self.send_data_button.disabled = True
        self.data_to_send.text = ''

        self.open_connection_button.disabled = False

    def sendData(self, obj):
        #todo: encryption here?
        cipherText = CBC.encrypt(self.cipher, self.data_to_send)
        self.console.text = self.console.text + '\n' + 'Text to be sent:' + self.data_to_send.text

        print "encrypted cipherText to send"+cipherText.encode("hex_codec")
        self.socket.sendall(cipherText)
        self.data_to_send.text = ''

    # returns socket or nothing on failure    
    def clientConnect(self, host, port):
        # create the client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to given ip and port
        try:
            client_socket.connect((host, port))
        except socket.error, msg:
            print msg
            return

        return client_socket

    # returns socket or nothing on failure  
    def serverConnect(self, port):
        # create the server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print socket.gethostname()
        # bind the socket to host and port
        try:
            server_socket.bind((socket.gethostname(), port))
        except socket.error, msg:
            print msg    
            return
        # listen for a connection
        server_socket.listen(1)

        sock, addr = server_socket.accept()
        return sock   


class MyApp(App):

    def build(self):
        init = InitScreen()
        return init

if __name__ == '__main__':
    MyApp().run()