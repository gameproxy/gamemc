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

while True:
    for plugin in config["plugins"]:
        plugins.append(importlib.import_module("plugins.{}.main".format(plugin["name"]), plugin["name"]))

        if hasattr(plugins[-1], "__start__"):
            try:
                plugins[-1].__start__(game, gameInterfaceInstance, plugin["config"])
            except Exception as e:
                gameInterfaceInstance.sendChatMessage("§4Plugin {} failed: uncaught {}".format(plugins[-1].__name__.split(".")[1], e.__class__.__name__))
                print("Plugin {} failed at start: uncaught {}: {}".format(plugins[-1].__name__.split(".")[1], e.__class__.__name__, e.message))
        
        gameInterfaceInstance.sendChatMessage("§ePlugin {} loaded".format(plugins[-1].__name__.split(".")[1]))
        print("Plugin {} loaded".format(plugins[-1].__name__.split(".")[1]))

    if len(plugins) == 1:
        gameInterfaceInstance.sendChatMessage("§aLoaded 1 plugin")
        print("Loaded 1 plugin")
    else:
        gameInterfaceInstance.sendChatMessage("§aLoaded {} plugins".format(len(plugins)))
        print("Loaded {} plugins".format(len(plugins)))

    while True:
        configFile = open("config.json", "r")
        newConfig = json.loads(configFile.read())

        configFile.close()

        if newConfig != config:
            break

        for plugin in plugins:
            if hasattr(plugin, "__loop__"):
                try:
                    plugin.__loop__()
                except Exception as e:
                    gameInterfaceInstance.sendChatMessage("§4Plugin {} failed: uncaught {}".format(plugin.__name__.split(".")[1], e.__class__.__name__))
                    print("Plugin {} failed at loop: uncaught {}: {}".format(plugin.__name__.split(".")[1], e.__class__.__name__, e.message))
    
    gameInterfaceInstance.sendChatMessage("§ePlugin configuration modified, reloading plugins...")
    print("Plugin configuration modified, reloading plugins...")