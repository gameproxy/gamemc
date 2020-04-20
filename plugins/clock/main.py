import time

characters = {
    "0": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    "1": [
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    "2": [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1]
    ],
    "3": [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 3],
        [1, 1, 1]
    ],
    "4": [
        [1, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    "5": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1]
    ],
    "6": [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    "7": [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    "8": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    "9": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1]
    ],
    ":": [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
}

def renderCharacter(point, character):
    for x in range(0, 3):
        for y in range(0, 5):
            if characters[character][y][x] == 0:
                interface.sendCommand("setblock {} {}".format(game.Point(point.x + x, point.y + y, point.z).toCommandString(), config["segOffBlock"]))
            elif characters[character][y][x] == 1:
                interface.sendCommand("setblock {} {}".format(game.Point(point.x + x, point.y + y, point.z).toCommandString(), config["segOnBlock"]))

def __start__(gameParameter, interfaceParameter, configParameter):
    global game, interface, config
    
    game = gameParameter
    interface = interfaceParameter
    config = configParameter

def __loop__():
    displayedTime = time.strftime(config["timeFormat"], time.localtime())
    
    for i in range(0, len(displayedTime)):
        renderCharacter(config["x"] + (4 * i), config["y"], config["z"])