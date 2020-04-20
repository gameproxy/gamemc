import time

def __start__(gameParameter, interfaceParameter, configParameter):
    global game, interface, config
    
    game = gameParameter
    interface = interfaceParameter
    config = configParameter

def __loop__():
    print(time.strftime(config["timeFormat"], time.localtime()))
    interface.sendCommand("title @a actionbar " + time.strftime(config["timeFormat"], time.localtime()))