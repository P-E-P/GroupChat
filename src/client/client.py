import socket

class Client:
    def __init__(self, username):
        # Create a new TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = username

    def connect(self, hostname, port):
        try:
            self.socket.connect((hostname,port))
            self.socket.send(Message("NULL", "SERVER", self.username).encode())
            return True
        except socket.error as ex:
            self.socket.close()
            print("[ERR]:", ex)
            return False
            

    def disconnect(self):
        socket.send(Message(usrName, "SERVER", "BYE").encode())

    def __determineRecipients(data):
        ret = ""
        
        return ret
        
    def send(self, data):
        # Send the message
        input("Press enter to send the message...")
        self.socket.send(Message(self.username,"ALL", data).encode())
