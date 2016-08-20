**Introduction**

The chat app utilizes TCP/IP together with Diffie-Hellman mutual authentication protocol and md5 HMAC for message integrity. Diffie-Hellman was also chosen for establishing session key for perfect forward secrecy. The integrity-protection in the app utilizes a md5 hash which hashes our message using the pre-established shared secret. The receiver checks the decrypted message against the HMAC to detect alteration on the message.

<img src="appScreenshot.jpg" width="400" />

**Requirement**

- Python 2.7
- kivy 1.9.0
- pycrypto

**Run from command line**

>> python main.py

**Usage**

- Run server instance, the default is in server mode. Click Open Connection button and type in a listening port number.
- Run another instance as client, click Client button to change to client mode. Click Open Connection button and type in respective host and port to connect to server.
- Enter shared secret value into client and click Use Secret button
- Enter shared secret value into server and click Use Secret button
- The server and client should now be mutually authenticated.
- Type in message to send between client and server, the message exchanged is displayed in console.
- Close client and server connection and quit program.


