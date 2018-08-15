import sys


class CommandManager(object):
    def __init__(self):
        self.commands = []
        self.track = 'python'

    def register(self, function):
        self.commands.append(function)
        self.commands.sort(key=lambda f: f.__name__)
        return function

    def find_best(self, s):
        matches = [
            c for c in self.commands
            if c.__name__.startswith(s)
        ]
        if len(matches) == 1:
            return matches[0].__name__
        elif len(matches) == 0:
            print(f"Unknown command '{s}'")
        else:
            print(f"Ambigious command '{s}'; choose from the following:")
            for match in matches:
                print(f'  {match.__name__}')
        sys.exit(1)

    def __iter__(self):
        return (f.__name__ for f in self.commands)
