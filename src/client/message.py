from datetime import datetime

"""
Recipients are for private messages, you could also use special keyword to designate special recipient:

- all    : send the message to everyone.
- server : send the message to the server only (commands).
- last   : send the message to the last client group you talked to,
           if no group has been contacted previously the message is sent to everyone.
"""

class Message:
    def __init__(self, sender, recipients, data):
        self.sender = sender
        self.recipients = recipients
        self.data = data
        self.time = datetime.now()
        self.uuid = uuid.uuid4()

    def serialize(self):
        return "{sender:" + self.sender + "recipients" + ";".join(str(x) for x in self.recipients) + ", time:" + self.time.strftime("%d;%m;%Y;%H;%M;%S") + "uuid:" + self.uuid.hex + ", data:" + self.data + "}"

    def encode(self):
        return self.serialize.encode
