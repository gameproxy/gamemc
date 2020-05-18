import time
import re

RE_NO_ITEMS = "^Could not clear the inventory of .*, no items to remove$"

lastRun = 0

def replenishItems():
    for item in range(0, len(config["items"])):
        interface.sendCommand("clear @a {}".format(config["items"][item]["item"]))
        interface.sendCommand("give @a {} 1".format(config["items"][item]["item"]))

def __start__(gameParameter, interfaceParameter, configParameter):
    global game, interface, config

    game = gameParameter
    interface = interfaceParameter
    config = configParameter

    replenishItems()

def __loop__(events):
    global lastRun

    for event in events:
        if event.type == "playerJoin":
            for item in range(0, len(config["items"])):
                interface.sendCommand("clear \"{}\" {}".format(event.data["name"], config["items"][item]["item"]))
                interface.sendCommand("give \"{}\" {} 1".format(event.data["name"], config["items"][item]["item"]))

    if time.time() > lastRun + config["runEvery"]:
        for item in range(0, len(config["items"])):
            for player in game.players:
                interface.cli.poll()
                interface.cli.readstdout()

                result = interface.sendCommand("clear \"{}\" {}".format(player.name, config["items"][item]["item"]))
                hasMatched = False

                for line in result.split("\n"):
                    if re.compile(RE_NO_ITEMS).match(line):
                        hasMatched = True

                if hasMatched:
                    interface.sendCommand("execute \"{}\" ~ ~ ~ kill @e[type=item,r=5]".format(player.name))

                    for command in range(0, len(config["items"][item]["commands"])):
                        interface.sendCommand(config["items"][item]["commands"][command].replace("@p", player.name))
                    
        replenishItems()

        lastRun = time.time()