import socket
from threading import Thread
from queue import *
from message import *

class Client:
    def __init__(self, username, socket, address):
        self.address = address
        self.username = username
        self.socket = socket
        self.awaiting_messages = Queue()
        self.running = True
        
    def start(self, users):
        self.running = True
        self.thread = Thread(target = self.receive, args=(users,))
        self.thread.start()
        
    def receive(self, users):
        while self.running:
            try:
                data = self.socket.recv(4096).decode()
                msg = fromStr(data)
                if "SERVER" in msg.recipients and msg.data == "QUIT":
                    print("[INFO]: Client", msg.sender,"disconnected")
                    self.running = False
                    break
                
                print("Received a new message from ", msg.sender, "to", msg.recipients, ": (", msg.time, ")", msg.data)
                # If no recipient specified, send to all
                if msg.recipients == set(['']):
                    for key in users:
                        if key != self.username.upper():
                            users[key].awaiting_messages.put(msg)
                
                # Handle messages for server exclusively
                elif msg.recipients == set(['SERVER']):
                    if(msg.data == "LIST"):
                        print("[INFO]:", msg.sender, "requested the list of user")
                        answer = ">>"
                        for i in users.values():
                            answer += "->" + i.username
                        self.awaiting_messages.put(Message("SERVER",[self.username], answer))

                # Handle messages with specific recipient
                else:
                    for recip in msg.recipients:
                        if recip.upper() in users:
                            users[recip.upper()].awaiting_messages.put(msg)

            except Exception as e:
                print(e)
                print("Connection to", self.username, "has been lost")
                self.running = False
                break

    def sendAwaiting(self):
        if not self.awaiting_messages.empty():
            self.socket.send(self.awaiting_messages.get().serialize().encode())
            #print("[INFO]: Message transmitted to", self.username)
