import socket

from message import *
import log

class Client:
    def __init__(self, username):
        # Create a new TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.running = False

    def connect(self, hostname, port):
        try:
            self.socket.connect((hostname,port))

            # Ask the server if the username was already taken.
            log.info("Requesting username...")
            message = Message("NULL", ["SERVER"], self.username)
            serial = message.serialize()
            self.socket.send(serial.encode())
            # Receive the answer from the server.
            answerdata = self.socket.recv(1024).decode()
            answer = fromStr(answerdata)
            # Changing the client username if it was taken.
            if(answer.data != self.username):
                log.warn("Server indicate your username was taken, your new username is", answer.data)
                self.username = answer.data

            self.running = True
        except socket.error as ex: # Connection error
            self.socket.close()
            log.err(ex)
        finally:
            return self.running

    def send(self, data):
        self.socket.send(Message(self.username, self.__parseRecipients(data), data).serialize().encode())

    def receive(self):
        # Receive a message and parse it.
        try:
            msg = self.socket.recv(4096).decode()
        except Exception as e:
            print(e)
        return fromStr(msg)
            
    def disconnect(self):
        log.info("Disconnecting...")
        self.socket.send(Message(self.username, ["SERVER"], "QUIT").serialize().encode())
        self.socket.close()

    def __parseRecipients(self, data):
        recipients = []
        wordlist = data.split(" ")
        for elt in wordlist:
            if elt[0] == '@':
                recipients.append(elt[1:])
        return recipients

