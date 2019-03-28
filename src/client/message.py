from datetime import datetime
import uuid

"""
Recipients are for private messages, you could also use special keyword to designate special recipient:

- all    : send the message to everyone.
- server : send the message to the server only (commands).
- last   : send the message to the last client group you talked to,
           if no group has been contacted previously the message is sent to everyone.
"""

MSG_SEP = "\u001f"
RECIPIENT_SEP = ";"
TIME_SEP = "/"

TIME_FORMAT = "%d" +  TIME_SEP + "%m" + TIME_SEP + "%Y" + TIME_SEP + "%H" + TIME_SEP + "%M" + TIME_SEP +"%S"

class Message:
    def __init__(self, sender, recipients, data, time=None, msgUUID=None):
        self.sender = sender
        self.recipients = recipients
        self.data = data
        self.time = time if time is not None else datetime.now()
        self.uuid = msgUUID if msgUUID is not None else uuid.uuid4()
        
    def serialize(self):
        return self.sender + MSG_SEP + \
            RECIPIENT_SEP.join(str(x) for x in self.recipients) + MSG_SEP + \
            self.time.strftime(TIME_FORMAT) + MSG_SEP + \
            str(self.uuid) + MSG_SEP + \
            self.data
    
def fromStr(data):
    # Getting sender
    parse = data.partition(MSG_SEP)
    sender = parse[0]
    # Getting recipients
    parse = parse[2].partition(MSG_SEP)
    recipients = parse[0].split(RECIPIENT_SEP)
    # Getting time
    parse = parse[2].partition(MSG_SEP)
    time = datetime.strptime(parse[0], TIME_FORMAT)
    # Getting uuid
    parse = parse[2].partition(MSG_SEP)
    msgUUID = uuid.UUID(parse[0])
    # Return Message
    return Message(sender, recipients, parse[2], time, msgUUID)
