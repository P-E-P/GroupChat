from enum import Enum

class CommandIdentifiers(Enum):
    PREFIX = "/"
    SEPARATOR = " "

class CommandList(Enum):
    QUIT = "quit"
    LIST = "list"
    KICK = "kick"
