import os, sys, platform

__SUPPORT_ANSI__ = False

class style:
    RESET_ALL         = "\033[0m"

    # Style set
    BOLD              = "\033[1m"
    DIM               = "\033[2m"
    UNDERLINED        = "\033[4m"
    BLINK             = "\033[5m"
    REVERSE           = "\033[7m"
    HIDDEN            = "\033[8m"

    # Style reset
    RESET_BOLD        = "\033[21m"
    RESET_DIM         = "\033[22m"
    RESET_UNDERLINED  = "\033[24m"
    RESET_BLINK       = "\033[25m"
    RESET_REVERSE     = "\033[27m"
    RESET_HIDDEN      = "\033[28m"

    # Foreground color
    DEFAULT           = "\033[39m"
    BLACK             = "\033[30m"
    RED               = "\033[31m"
    GREEN             = "\033[32m"
    YELLOW            = "\033[33m"
    BLUE              = "\033[34m"
    MAGENTA           = "\033[35m"
    CYAN              = "\033[36m"
    LIGHT_GRAY        = "\033[37m"
    DARK_GRAY         = "\033[90m"
    LIGHT_RED         = "\033[91m"
    LIGHT_GREEN       = "\033[92m"
    LIGHT_YELLOW      = "\033[93m"
    LIGHT_BLUE        = "\033[94m"
    LIGHT_MAGENTA     = "\033[95m"
    LIGHT_CYAN        = "\033[96m"
    WHITE             = "\033[97m"

    # Background color
    BCK_DEFAULT       = "\033[49m"
    BCK_BLACK         = "\033[40m"
    BCK_RED           = "\033[41m"
    BCK_GREEN         = "\033[42m"
    BCK_YELLOW        = "\033[43m"
    BCK_BLUE          = "\033[44m"
    BCK_MAGENTA       = "\033[45m"
    BCK_CYAN          = "\033[46m"
    BCK_LIGHT_GRAY    = "\033[47m"
    BCK_DARK_GRAY     = "\033[100m"
    BCK_LIGHT_RED     = "\033[101m"
    BCK_LIGHT_GREEN   = "\033[102m"
    BCK_LIGHT_YELLOW  = "\033[103m"
    BCK_LIGHT_BLUE    = "\033[104m"
    BCK_LIGHT_MAGENTA = "\033[105m"
    BCK_LIGHT_CYAN    = "\033[106m"
    BCK_WHITE         = "\033[107m"

class flags:
    ENDC = style.DEFAULT
    WARN = style.YELLOW
    INFO = style.BLUE
    ERR  = style.RED

def checkANSI():
        if platform.system() == 'Windows' and not ('TERM' in os.environ and os.environ['TERM']=='ANSI'):
            __SUPPORT_ANSI__ = False
        else:
            __SUPPORT_ANSI__ = True
    
def warn(*args, **kwargs):
    if __SUPPORT_ANSI__:
        print(flags.WARN + "[WARN]:" + flags.ENDC + " ".join(map(str,args)), **kwargs)
    else:
        print("[WARN]:" + " ".join(map(str, args)), **kwargs)
        

def err(*args, **kwargs):
    if __SUPPORT_ANSI__:
        print(flags.ERR + "[ERR]:" + flags.ENDC + " ".join(map(str,args)), **kwargs)
    else:
        print("[ERR]:" + " ".join(map(str, args)), **kwargs)

def info(*args, **kwargs):
    if __SUPPORT_ANSI__:
        print(flags.INFO + "[INFO]:" + flags.ENDC+ " ".join(map(str,args)), **kwargs)
    else:
        print("[INFO]:" + " ".join(map(str, args)), **kwargs)
