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
            self.socket.sendMsg(Message("NULL", "SERVER", self.username).encode())
            # Receive the answer from the server.
            answer = message.fromStr(self.socket.recv(1024).decode())

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

    def sendMsg(self, msg):
        # Send a message.
        self.socket.send(msg.encode())

    def send(self, data):
        self.socket.send(Message(self.username, __determineRecipients(data), data))

    def receive(self):
        # Receive a message and parse it.
        return messagefromStr(self.socket.recv(4096).decode())
     
    def disconnect(self):
        socket.send(Message(usrName, "SERVER", "BYE").encode())
        self.running = False

    def __determineRecipients(data):
        ret = ""
        # TODO: parse the string to get all recipients
        return ret

