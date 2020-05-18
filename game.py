import re
import time

UNKNOWN_COMMAND_EMPTY = "Unknown command: . Please check that the command exists and that you have permission to use it."
RE_INFO = "^\[....-..-.. ..:..:.. INFO] .*$"
RE_INFO_SERVER_STARTED = "^\[....-..-.. ..:..:.. INFO] Server started.$"
RE_INFO_PLAYER_CONNECTED = "^\[....-..-.. ..:..:.. INFO] Player connected: (.*), xuid: .*$"
RE_INFO_PLAYER_DISCONNECTED = "^\[....-..-.. ..:..:.. INFO] Player disconnected: (.*), xuid: .*$"
RE_FOUND_PLAYERS = "Found (.*)"
NO_TARGETS = "No targets matched selector"
BLOCK_ERROR = "Cannot place block outside of the world"

players = []

class Event:
    def __init__(self, eventType, eventData = {}):
        self.type = eventType
        self.data = eventData

class Player:
    def __init__(self, name):
        self.name = name

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def toCommandString(self):
        return "{} {} {}".format(self.x, self.y, self.z)
    
    def toSelectorString(self, radius = 1):
        return "[x={},y={},z={},r={}]".format(self.x, self.y, self.z, radius)

class Volume:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
    
    def toCommandString(self):
        return "{} {} {} {} {} {}".format(self.x, self.y, self.z, self.dx, self.dy, self.dz)
    
    def toSelectorString(self):
        return "[x={},y={},z={},dx={},dy={},dz={}]".format(self.x, self.y, self.z, self.dx, self.dy, self.dz)

class GameInterface:
    def __init__(self, cli):
        self.cli = cli

        self.eventStdout = []
    
    def sendCommand(self, command, readOutput = True):
        self.cli.poll()
        self.cli.readstdout()

        self.cli.writestdin(command + "\n")
        self.cli.writestdin("\n") # Send a blank command so that we know when command output is complete

        if readOutput:
            output = ""
            lastMessage = ""
            timeout = time.time() + 1

            while timeout != 0:
                self.cli.poll()
                lastMessage = self.cli.readstdout()
                
                for line in lastMessage.splitlines():
                    if line == UNKNOWN_COMMAND_EMPTY: # Test to see if command output is complete
                        return output.rstrip()
                    elif re.compile(RE_INFO).match(line): # Skip INFO lines, add them to the event queue stdout only
                        self.eventStdout.append(line)

                        continue
                    
                    output += line + "\n"
                
                if time.time() > timeout:
                    break
        else:
            # Clear stdout

            self.cli.poll()
            self.cli.readstdout()
    
    def captureEvents(self):
        events = []

        self.cli.poll()

        stdout = self.cli.readstdout()

        for line in stdout.splitlines():
            if re.compile(RE_INFO).match(line):
                self.eventStdout.append(line)
        
        for line in self.eventStdout:
            if re.compile(RE_INFO_SERVER_STARTED).match(line):
                events.append(Event("serverStart"))
            if re.compile(RE_INFO_PLAYER_CONNECTED).match(line):
                playerName = re.compile(RE_INFO_PLAYER_CONNECTED).match(line).group(1)

                events.append(Event("playerJoin", {
                    "name": playerName
                }))

                players.append(Player(playerName))
            if re.compile(RE_INFO_PLAYER_DISCONNECTED).match(line):
                playerName = re.compile(RE_INFO_PLAYER_DISCONNECTED).match(line).group(1)

                events.append(Event("playerLeave", {
                    "name": playerName
                }))

                for i in range(0, len(players)):
                    if players[i].name == playerName:
                        players.pop(i)

        self.eventStdout = []

        return events
    
    def sendChatMessage(self, message, targetPlayers = None):
        if targetPlayers == None:
            targetPlayers = "@a"

        if isinstance(targetPlayers, str):
            self.sendCommand("tellraw @a {{\"rawtext\": [{{\"text\": \"{}\"}}]}}".format(message.replace("\"", "\\\"")), False)
        else:
            for player in targetPlayers:
                self.sendCommand("tellraw \"{}\" {{\"rawtext\": [{{\"text\": \"{}\"}}]}}".format(player.name, message.replace("\"", "\\\"")), False)
    
    def observeVolume(self, volume):
        playersInVolume = []

        playerResult = self.sendCommand("testfor @e" + volume.toSelectorString())

        if playerResult != NO_TARGETS and playerResult != BLOCK_ERROR and re.compile(RE_FOUND_PLAYERS).match(str(playerResult)) != None:
            playerList = re.compile(RE_FOUND_PLAYERS).match(str(playerResult)).group(1).split(", ")

            for player in players:
                if player.name in playerList:
                    playersInVolume.append(player)
        
        return {
            "players": playersInVolume
        }
    
    def kick(self, message, targetPlayers = None):
        if targetPlayers == None:
            targetPlayers = "@a"

        if isinstance(targetPlayers, str):
            self.sendCommand("kick @a {}".format(message), False)
        else:
            for player in targetPlayers:
                self.sendCommand("kick \"{}\" {}".format(player.name, message), False)