lastPortalChecks = []

def __start__(gameParameter, interfaceParameter, configParameter):
    global game, interface, config, lastPortalChecks

    game = gameParameter
    interface = interfaceParameter
    config = configParameter

    lastPortalChecks = [[]] * len(config["portals"])

def __loop__(events):
    global lastPortalChecks

    for portal in range(0, len(config["portals"])):
        playersInPortal = interface.observeVolume(game.Volume(
            config["portals"][portal]["target"]["x"],
            config["portals"][portal]["target"]["y"],
            config["portals"][portal]["target"]["z"],
            config["portals"][portal]["target"]["dx"],
            config["portals"][portal]["target"]["dy"],
            config["portals"][portal]["target"]["dz"]
        ))

        if playersInPortal != lastPortalChecks[portal]:
            for player in playersInPortal["players"]:
                for command in range(0, len(config["portals"][portal]["commands"])):
                    interface.sendCommand(config["portals"][portal]["commands"][command].replace("@p", player.name), False)

            lastPortalChecks[portal] = playersInPortal