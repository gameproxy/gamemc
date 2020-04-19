import time

def __start__(gameParameter, interfaceParameter):
    global game, interface
    
    game = gameParameter
    interface = interfaceParameter

def __loop__():
    print(time.strftime("%H:%M:%S", time.gmtime()))
    interface.sendCommand("title @a actionbar " + time.strftime("%H:%M:%S", time.gmtime()))
