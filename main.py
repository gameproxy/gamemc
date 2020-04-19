import os # TODO: Remove this
import time

import cli
import game

os.chdir("/home/pi/MCServer") # TODO: Make this user-configurable
os.system("LD_LIBRARY_PATH=.")

newCli = cli.CLI(["/home/pi/MCServer/bedrock_server"])
newGameIf = game.GameInterface(newCli)

while True:
    events = newGameIf.captureEvents()
    
    for event in events:
        if event.type == "playerJoin":
            print("Player joined", event.data["name"])
            time.sleep(5)
            newGameIf.sendCommand("say Hello, " + event.data["name"] + "!")
        if event.type == "playerLeave":
            print("Player left", event.data["name"])
            newGameIf.sendCommand("say Bye, " + event.data["name"] + "!")
