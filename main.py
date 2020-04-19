import json
import os
import importlib

import cli
import game

configFile = open("config.json", "r")
config = json.loads(configFile.read())

configFile.close()

os.chdir(config["serverDirectory"])
os.system("LD_LIBRARY_PATH=.")

cliInstance = cli.CLI([os.path.join(config["serverDirectory"], "bedrock_server")])
gameInterfaceInstance = game.GameInterface(cliInstance)

plugins = []

for pluginName in config["plugins"]:
    plugins.append(__import__("plugins.{}.main".format(pluginName)))
    
    print(hasattr(plugins[-1], "__start__"))

    if hasattr(plugins[-1], "__start__"):
        getattr(plugins[-1], "__start__")(game, gameInterfaceInstance)

while True:
    for plugin in plugins:
        if hasattr(plugin, "__loop__"):
            getattr(plugin, "__loop__")
