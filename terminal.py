import subprocess

class Terminal():

    def __init__(self):
        pass
    #executa o terminal
    def execTerminal(self):
        p = subprocess.Popen(["start", "cmd", "/k", "{command here}"], shell = True) # Needs to be shell since start isn't an executable, its a shell cmd
        p.wait()