import re

class GameInterface:
    def __init__(self, cli):
        self.cli = cli
    
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
                if line == "Unknown command: . Please check that the command exists and that you have permission to use it.": # Test to see if command output is complete
                    return output.rstrip()
                
                output += line + "\n"
