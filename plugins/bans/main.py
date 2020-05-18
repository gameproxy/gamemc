import json
import os.path
import time

DEFAULT_BAN_MESSAGE = "You've been banned from this server!"

rawBanList = {
    "bannedPlayers": [],
    "bannedPlayerAttributes": {}
}

def readRawBanList():
    if os.path.isfile("plugins/bans/banList.json"):
        json.load(open("plugins/bans/banList.json", "r"))

def writeRawBanList():
    json.dump(rawBanList, open("plugins/bans/banList.json", "w"))

def playerAlreadyOnBanList(targetPlayer):
    return targetPlayer.name in rawBanList["bannedPlayers"]

def addToBanList(targetPlayers = None, timePeriod = None, message = None, subsequentMessage = None):
    if message == None:
        if "banMessage" in config:
            message = config["banMessage"]
        else:
            message = DEFAULT_BAN_MESSAGE

    if subsequentMessage == None:
        if "subsequentBanMessage" in config:
            subsequentMessage = config["subsequentBanMessage"]
        else:
            subsequentMessage = DEFAULT_BAN_MESSAGE

    readRawBanList()

    if targetPlayers == None:
        targetPlayers = game.players

    for player in targetPlayers:
        if not playerAlreadyOnBanList(player):
            rawBanList["bannedPlayers"].append(player.name)
            rawBanList["bannedPlayerAttributes"][player.name] = {"subsequentMessage": subsequentMessage}

            if timePeriod == None:
                rawBanList["bannedPlayerAttributes"][player.name]["bannedUntil"] = None
            else:
                rawBanList["bannedPlayerAttributes"][player.name]["bannedUntil"] = time.time() + timePeriod
    
    writeRawBanList()

    interface.kick(message, targetPlayers)

def __start__(gameParameter, interfaceParameter, configParameter):
    global game, interface, config
    
    game = gameParameter
    interface = interfaceParameter
    config = configParameter

    readRawBanList()

def __loop__(events):
    for event in events:
        if event.type == "playerJoin":
            for playerName in rawBanList["bannedPlayers"]:
                if event.data["name"] == playerName:
                    if rawBanList["bannedPlayerAttributes"][playerName]["bannedUntil"] == None or rawBanList["bannedPlayerAttributes"][playerName]["bannedUntil"] > time.time():
                        interface.kick(rawBanList["bannedPlayerAttributes"][playerName]["subsequentMessage"], [game.Player(playerName)])
                    else:
                        rawBanList["bannedPlayers"].remove(playerName)
                        
                        del rawBanList["bannedPlayerAttributes"][playerName]

                        writeRawBanList()