class TiborcimDataTypes ():
    NONE = 0
    NUMBER = 1
    INT = 2
    FLOAT = 3
    STRING = 4
    # RECORD = 5 -- Possible future function 

class TiborcimItem ():
    def __init__ (self, name):
        self.name = name

    def emit (self):
        return [''];

class TiborcimBlock (TiborcimItem):
    def __init__ (self, name):
        TiborcimItem.__init__(name)
        self.items = []

    def add (self, item):
        self.items.append(item)

    def start_block (self):
        return ['']
        
    def emit (self):
        lines = []
        line.append(self.start_block())
        for item in self.items:
            lines.append(item.emit())
        return lines

class TiborcimRootBlock (TiborcimBlock):
    def __init__ (self, name):
        TiborcimBlock.__init__(name)
        self.functions = []
        self.subroutines = []

    def add_subroutine (self, sub):
        self.functions.append(sub)

    def add_function (self, funct):
        self.functions.append(funct)

    def emit (self)
        lines = []
        for funct in self.functions:
            lines.append(funct.emit())

        for sub in self.subroutines:
            lines.append(sub.emit())

        for item in self.items:
            lines.append(item.emit())

        return lines

class TiborcimSubroutine (TiborcimBlock):
    def __init__ (self, name):
        TiborcimBlock.__init__(name)
        self.argcount = 0
        self.argtype = []
        self.arguments = []

    def start_block (self):
        arglist = ''
        for arg in self.arguments:
            arglist = arglist + arg.name

        if len(self.arguments) is not self.argcount:
            raise Exception('Argument Mismatch')

        for expectedtype in self.argtype and arg in self.arguments:
            if expectedtype is not arg.returntype:
                raise Exception('Argument Mismatch')
        
        return 'def ' + self.name + '(' + arglist + '):'

class TiborcimFunction (TiborcimSubroutine):
    def __init__ (self, name, returntype):
        TiborcimSubroutine.__init__(name)
        self.arguments = []
        self.returntype = returntype


class TiborcimVariable (TiborcimItem):
    def __init__ (self, name, datatype):
        TiborcimItem.__init__(name)
        self.returntype = datatype

root = TiborcimRootBlock()
