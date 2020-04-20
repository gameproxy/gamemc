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
        [0, 0, 1],
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

lastTimes = []
lastRun = 0

def renderCharacter(clock, point, character):
    for x in range(0, 3):
        for y in range(0, 5):
            if config["clocks"][clock]["axis"] == "x":
                setBlock = game.Point(point.x + x, point.y + 4 - y, point.z).toCommandString()
            elif config["clocks"][clock]["axis"] == "y":
                setBlock = game.Point(point.x, point.y + x, point.z + 4 - y).toCommandString()
            elif config["clocks"][clock]["axis"] == "z":
                setBlock = game.Point(point.x, point.y + 4 - y, point.z + x).toCommandString()
            elif config["clocks"][clock]["axis"] == "-x":
                setBlock = game.Point(point.x - x, point.y + 4 - y, point.z).toCommandString()
            elif config["clocks"][clock]["axis"] == "-y":
                setBlock = game.Point(point.x, point.y - x, point.z + 4 - y).toCommandString()
            elif config["clocks"][clock]["axis"] == "-z":
                setBlock = game.Point(point.x, point.y + 4 - y, point.z - x).toCommandString()

            blockType = config["clocks"][clock]["segOffBlock"]

            if characters[character][y][x] == 1:
                blockType = config["clocks"][clock]["segOnBlock"]
            
            interface.sendCommand("setblock {} {}".format(setBlock, blockType), False)

def __start__(gameParameter, interfaceParameter, configParameter):
    global game, interface, config, lastTimes
    
    game = gameParameter
    interface = interfaceParameter
    config = configParameter

    for clock in range(0, len(config["clocks"])):
        lastTimes.append("")

        # Clear area to render blocks
        displayedTime = time.strftime(config["clocks"][clock]["timeFormat"], time.localtime())
        lastTimes[clock] = " " * len(displayedTime)

        dx = 0
        dy = 0
        dz = 0

        if config["clocks"][clock]["axis"] == "x":
            dx = (4 * len(displayedTime)) - 2
            dy = 4
            dz = 0
        elif config["clocks"][clock]["axis"] == "y":
            dx = 0
            dy = (4 * len(displayedTime)) - 2
            dz = 5
        elif config["clocks"][clock]["axis"] == "z":
            dx = 0
            dy = 4
            dz = (4 * len(displayedTime)) - 2
        elif config["clocks"][clock]["axis"] == "-x":
            dx = (-4 * len(displayedTime)) + 2
            dy = 4
            dz = 0
        elif config["clocks"][clock]["axis"] == "-y":
            dx = 0
            dy = (-4 * len(displayedTime)) + 2
            dz = 4
        elif config["clocks"][clock]["axis"] == "-z":
            dx = 0
            dy = 4
            dz = (-4 * len(displayedTime)) + 2

        interface.sendCommand("fill {} {} {} {} {} {} {}".format(
            config["clocks"][clock]["x"],
            config["clocks"][clock]["y"],
            config["clocks"][clock]["z"],
            config["clocks"][clock]["x"] + dx,
            config["clocks"][clock]["y"] + dy,
            config["clocks"][clock]["z"] + dz,
            config["clocks"][clock]["segOffBlock"]
        ), False)

def __loop__():
    global lastRun, lastTimes

    if time.time() > lastRun + config["runEvery"]:
        for clock in range(0, len(config["clocks"])):
            displayedTime = time.strftime(config["clocks"][clock]["timeFormat"], time.localtime())

            for i in range(0, len(displayedTime)):
                dx = 0
                dy = 0
                dz = 0

                if config["clocks"][clock]["axis"] == "x":
                    dx = 4 * i
                    dy = 0
                    dz = 0
                elif config["clocks"][clock]["axis"] == "y":
                    dx = 0
                    dy = 4 * i
                    dz = 0
                elif config["clocks"][clock]["axis"] == "z":
                    dx = 0
                    dy = 0
                    dz = 4 * i
                elif config["clocks"][clock]["axis"] == "-x":
                    dx = -4 * i
                    dy = 0
                    dz = 0
                elif config["clocks"][clock]["axis"] == "-y":
                    dx = 0
                    dy = -4 * i
                    dz = 0
                elif config["clocks"][clock]["axis"] == "-z":
                    dx = 0
                    dy = 0
                    dz = -4 * i

                if lastTimes[clock][i] != displayedTime[i]:
                    renderCharacter(clock, game.Point(
                        config["clocks"][clock]["x"] + dx,
                        config["clocks"][clock]["y"] + dy,
                        config["clocks"][clock]["z"] + dz
                    ), displayedTime[i])

            lastTimes[clock] = displayedTime
        
        lastRun = time.time()