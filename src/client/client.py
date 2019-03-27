import socket

import log

class Client:
    def __init__(self, username):
        # Create a new TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username
        self.connected = False

    def connect(self, hostname, port):
        try:
            self.socket.connect((hostname,port))

            # Ask the server if the username was already taken.
            self.socket.send(Message("NULL", "SERVER", self.username).encode())
            # Receive the answer from the server.
            answer = message.fromStr(seld.socket.recv(1024).decode())

            # Changing the client username if it was taken.
            if(answer.data != self.username):
                log.warn("Server indicate your username was taken, your new username is", answer.data)
                self.username = answer.data

            self.connected = True
        except socket.error as ex: # Connection error
            self.socket.close()
            log.err(ex)
        finally:
            return self.connected

    def send(self, msg):
        self.socket.send(msg.encode())

    def disconnect(self):
        socket.send(Message(usrName, "SERVER", "BYE").encode())
        self.connected = False

    def __determineRecipients(data):
        ret = ""
        # TODO: parse the string to get all recipients
        return ret
        
    def send(self, data):
        # Send a new message
        self.socket.send(Message(self.username,"ALL", data).encode())
