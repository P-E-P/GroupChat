import os

'''
This class regroup either blacklist and whitelist
'''
class Userlist:
    def __init__(self, whitelist, path):
        self.whitelist = whitelist
        self.path = path

        if os.path.isfile(path):
            return path
        else:
            print("[ERR]:", "Whitelist" if self.whitelist else "Blacklist", "file path not valid")
    
