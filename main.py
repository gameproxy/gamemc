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
started = False

while not started:
    events = gameInterfaceInstance.captureEvents()

    for event in events:
        if event.type == "serverStart":
            started = True

gameInterfaceInstance.sendChatMessage("§eLoading plugins...")
print("Loading plugins...")

for plugin in config["plugins"]:
    plugins.append(importlib.import_module("plugins.{}.main".format(plugin["name"]), plugin["name"]))

    if hasattr(plugins[-1], "__start__"):
        try:
            plugins[-1].__start__(game, gameInterfaceInstance, plugin["config"])
        except Exception as e:
            gameInterfaceInstance.sendChatMessage("§4Plugin {} failed: uncaught {}".format(plugins[-1].__name__, e.__class__.__name__))
            print("Plugin {} failed at start: uncaught {}: {}".format(plugins[-1].__name__, e.__class__.__name__, e.message))
    
    gameInterfaceInstance.sendChatMessage("§ePlugin {} loaded".format(plugins[-1].__name__))
    print("Plugin {} loaded".format(plugins[-1].__name__))

if len(plugins) == 1:
    gameInterfaceInstance.sendChatMessage("§aLoaded 1 plugin")
else:
    gameInterfaceInstance.sendChatMessage("§aLoaded {} plugins".format(len(plugins)))

while True:
    for plugin in plugins:
        if hasattr(plugin, "__loop__"):
            try:
                plugin.__loop__()
            except Exception as e:
                gameInterfaceInstance.sendChatMessage("§4Plugin {} failed: uncaught {}".format(plugin.__name__, e.__class__.__name__))
                print("Plugin {} failed at loop: uncaught {}: {}".format(plugin.__name__, e.__class__.__name__, e.message))