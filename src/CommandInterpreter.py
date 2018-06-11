import os


class CommandInterpreter:
    def __init__(self):
        pass

    def run(self, cmd):
        os.system("start " + cmd)
 