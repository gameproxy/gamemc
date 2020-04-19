import os
import subprocess
import select

class CLI:
    def __init__(self, command):
        self.command = command

        self.stdout = ""
        self.stderr = ""
        self.finished = False

        self.subprocess = subprocess.Popen(self.command, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    
    def poll(self):
        if not self.finished:
            broken = False

            while self.subprocess.stdout in select.select([self.subprocess.stdout], [], [], 0)[0]:
                line = self.subprocess.stdout.readline()

                if line and line != b"":
                    self.stdout += line.decode()
                else:
                    broken = True

                    break
            
            if broken:
                self.finished = True

                return False
            else:
                while self.subprocess.stderr in select.select([self.subprocess.stderr], [], [], 0)[0]:
                    line = self.subprocess.stderr.readline()

                    if line and line != b"":
                        self.stdout += line.decode("utf-8")
                    else:
                        broken = True

                        break
                
                if broken:
                    self.finished = True

                    return False
                else:
                    return True
        else:
            return False
    
    def writestdin(self, text):
        if not self.finished:
            try:
                self.subprocess.stdin.write(text.encode())
                self.subprocess.stdin.flush()

                return True
            except BrokenPipeError:
                return False
    
    def readstdout(self):
        stdout = self.stdout
        self.stdout = ""

        return stdout
    
    def readstderr(self):
        stderr = self.stderr
        self.stderr = ""

        return stderr