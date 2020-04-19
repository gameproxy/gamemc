class GameInterface:
    def __init__(self, cli):
        self.cli = cli
    
    def sendCommand(self, command):
        self.cli.poll()
        self.cli.readstdout()

        self.cli.writestdin(command + "\n")
        self.cli.writestdin("\n") # Send a blank command so that we know when command output is complete
        self.cli.poll()

        output = ""
        lastMessage = ""
        timeout = 10

        while timeout != 0:
            lastMessage = self.cli.readstdout()

            if lastMessage.startswith("Unknown command: . "): # Test to see if command output is complete
                break
            
            output += lastMessage
            timeout -= 1
        
        return output