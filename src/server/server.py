from socket import *
from threading import Thread
from client import *
from message import *


class Server:
    def __init__(self, port):
        self.running = False
        self.accepting = False
        # This dict contains the users, to access a user
        # we need to use it's username in uppercase letter
        self.users = dict()
        # Create a TCP socket
        self.ssocket = socket.socket(AF_INET,SOCK_STREAM)
        self.port = port

    # Start the accepting thread and retransmission thread
    def start(self):
        self.running = True
        # Assign IP address and port number to socket
        self.ssocket.bind(('', self.port))
        self.ssocket.listen(1)
        
        # Creating and starting the thread that will send messages
        self.rThread = Thread(target = self.processMessages)
        self.rThread.start()

        self.aThread = Thread(target = self.accept)
        self.aThread.start()
        
        print ('[INFO]: The server is ready to receive')

        
    def accept(self):
        self.accepting = True
        while self.accepting:
            # Create a new thread with that connectionSocket and start it.
            # This new thread will attempt to receive all messages.
            try:
                csocket,addr = self.ssocket.accept()
                self.addConnection(csocket, addr)
            except Exception:
                if self.accepting:
                    print('[ERR]: Error while accepting')
            

    # This function stop the server
    def close(self):
        self.accepting = False
        print("[WARN]: Stopping server")
        
        # Closing the accepting server socket
        self.ssocket.close()
        
        # Stopping accepting thread
        self.aThread.join()
        print("[INFO]: Not accepting new connection anymore...")

        # TODO: send a disconnection message to all remaining clients
        
        self.running = False
        print("[WARN]: Stopping retransmission")
        # Stopping retransmit thread
        self.rThread.join()
        print("[INFO]: Server stopped")



    # This function has it's own thread,
    # it iterates over all users and send
    # the oldest untransmitted message to
    # the user.
    def processMessages(self):
        while self.running:
            for i in list(self.users.keys()):
                self.users[i].sendAwaiting()
                if not self.users[i].running:
                    self.users.pop(i, None)

    # This function handle the new connection,
    # to do so it gives a username to the client
    # according to his request. Then it add the
    # client to the list
    def addConnection(self,clientSocket, addr):
        print("[INFO]: New connection from", addr)
        # Get the initial message
        data = clientSocket.recv(4096).decode()
        msg = fromStr(data)
        username = msg.data
        # Checking if username is already registered in user list.
        if msg.data.upper() in self.users.keys():
            print("[WARN]: User already recorded, attributing a new username...")
            # The server append a number to the username until
            # the generated username is not registered.
            username = msg.data + "1"
            i = 2
            while username.upper() in self.users.keys():
                username = msg.data + str(i)
                i += 1

        # Creating the message to send confirmation to the client
        message = Message("SERVER", [username], username).serialize()
        # Sending back the attributed username
        print("[INFO]: Sending confirmation for ", addr)
        clientSocket.send(message.encode())

        # Temporary variable to hold the uppercase version of the username
        upper = username.upper()
        # Adding the client to the dict
        self.users[upper] = Client(username, clientSocket, addr)
        # Starting to receive messages from the client
        self.users[upper].start(self.users)
        print("[INFO]: Added user", username,"with address",addr,"to the list")
