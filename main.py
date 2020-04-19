import os # TODO: Remove this

import cli
import game

os.chdir("/home/pi/MCServer") # TODO: Make this user-configurable
os.system("LD_LIBRARY_PATH=.")

newCli = cli.CLI(["/home/pi/MCServer/bedrock_server"])
newGameIf = game.GameInterface(newCli)

while True:
    command = input("> ")
    
    print(newGameIf.sendCommand(command))