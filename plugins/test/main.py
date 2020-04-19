game = None
interface = None

def __start__(gameParameter, interfaceParameter):
    game = gameParameter
    interface = interfaceParameter

def __loop__():
    interface.sendCommand("title @a actionbar Hello, world!")