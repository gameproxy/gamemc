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

for plugin in config["plugins"]:
    plugins.append(importlib.import_module("plugins.{}.main".format(plugin["name"]), plugin["name"]))

    if hasattr(plugins[-1], "__start__"):
        plugins[-1].__start__(game, gameInterfaceInstance, plugin["config"])

while True:
    for plugin in plugins:
        if hasattr(plugin, "__loop__"):
            plugin.__loop__()