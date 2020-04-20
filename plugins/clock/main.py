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
    ]
}

lastTime = ""

def renderCharacter(point, character):
    for x in range(0, 3):
        for y in range(0, 5):
            setBlock = game.Point(point.x + x, point.y + y, point.z).toCommandString()
            blockType = config["segOffBlock"]

            if characters[character][y][x] == 1:
                blockType = config["segOnBlock"]
            
            interface.sendCommand("setblock {} {}".format(setBlock, blockType), False)

def __start__(gameParameter, interfaceParameter, configParameter):
    global game, interface, config, lastTime
    
    game = gameParameter
    interface = interfaceParameter
    config = configParameter

    # Clear area to render blocks
    displayedTime = time.strftime(config["timeFormat"], time.localtime())
    lastTime = displayedTime

    time.sleep(10)

    interface.sendCommand("fill {} {} {} {} {} {} {}".format(config["x"], config["y"], config["z"], config["x"] + (4 * len(displayedTime)), config["y"] + 5, config["z"], config["segOffBlock"]), False)

def __loop__():
    global lastTime

    displayedTime = time.strftime(config["timeFormat"], time.localtime())

    print(displayedTime)
    
    for i in range(0, len(displayedTime)):
        if lastTime[i] != displayedTime[i]:
            renderCharacter(game.Point(config["x"] + (4 * i), config["y"], config["z"]), displayedTime[i])

    lastTime = displayedTime