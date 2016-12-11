class DataType:
    NONE = 0
    NUMBER = 1
    STRING = 2

import re

class Item:
    def __init__(self, name):
        self.name = name
        self.argcount = 0
        self.inline = True
        self.statement = False
        self.datatype = DataType.NONE
        self.replacement = ''

    def run(self, line):
        regex = r''
        if self.inline:
            regex += r'\b'
        else:
            regex += r'^'
        regex += self.name
        if self.inline:
            if self.argcount > 0:
                regex += r'\b\(\W?([^,]s*)\W?'
                for x in range(1, self.argcount):
                    regex += ',\W?([^,]*)\W?'
                regex += r'\)\b'
            else:
                regex += r'\b'
        elif not self.inline:
            if self.argcount > 0:
                regex += r'\b\W?([^,]*)\W?'
                for x in range(1, self.argcount):
                    regex += ',\W?([^,]*)\W?'
            else:
                regex += r'\b'
        line = re.sub(regex, self.replacement, line)
        return line
