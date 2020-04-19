import re

UNKNOWN_COMMAND_EMPTY = "Unknown command: . Please check that the command exists and that you have permission to use it."
RE_INFO = "^\[....-..-.. ..:..:.. INFO] .*$"
RE_INFO_PLAYER_CONNECTED = "^\[....-..-.. ..:..:.. INFO] Player connected: (.*), xuid: .*$"
RE_INFO_PLAYER_DISCONNECTED = "^\[....-..-.. ..:..:.. INFO] Player disconnected: (.*), xuid: .*$"

class Event:
    def __init__(self, eventType, eventData = {}):
        self.type = eventType
        self.data = eventData


class GameInterface:
    def __init__(self, cli):
        self.cli = cli

        self.eventStdout = []
    
    def sendCommand(self, command):
        self.cli.poll()
        self.cli.readstdout()

        self.cli.writestdin(command + "\n")
        self.cli.writestdin("\n") # Send a blank command so that we know when command output is complete

        output = ""
        lastMessage = ""
        timeout = 10000

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
    
    def captureEvents(self):
        events = []

        self.cli.poll()

        stdout = self.cli.readstdout()

        for line in stdout.splitlines():
            if re.compile(RE_INFO).match(line):
                self.eventStdout.append(line)
        
        for line in self.eventStdout:
            if re.compile(RE_INFO_PLAYER_CONNECTED).match(line):
                events.append(Event("playerJoin", {
                    "name": re.compile(RE_INFO_PLAYER_CONNECTED).match(line).group(1)
                }))
            if re.compile(RE_INFO_PLAYER_DISCONNECTED).match(line):
                events.append(Event("playerLeave", {
                    "name": re.compile(RE_INFO_PLAYER_DISCONNECTED).match(line).group(1)
                }))

        self.eventStdout = []

        return events
