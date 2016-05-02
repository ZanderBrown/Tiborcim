from enum import Enum

class TibcStatus(Enum):
    HEX_GEN_ERROR = 1
    NOT_FOUND = 2
    SUCCESS = 3

class compiler:
    def __init__(self, file, output = None):
        import re
        self.inputFile = open(file, "r")
        if output is None:
            output = file + '.py'
        self.outputFile = open(output, "w")
        self.content = self.inputFile.readlines()

        self.indentLevel = 0;
        self.python_block = False

        self.print_output('from microbit import *')
        for line in self.content:
            if self.python_block is False:
                m = re.search('(?:^PRINT)', line)
                if m is not None:
                    self.print_output('display.scroll(' + str.strip(line[5:]) + ')')
                    continue

                m = re.search('(?:^IF)', line)
                if m is not None:
                    line = re.sub('=', ' is ', line)
                    print(">" + line)
                    self.print_output('if (' + str.strip(line[2:-5]) + '):')
                    self.indentLevel += 1
                    continue

                m = re.search('(?:^\')', line)
                if m is not None:
                    self.print_output('#' + line)
                    continue

                m = re.search('(?:^END IF)', line)
                if m is not None:
                    self.indentLevel -= 1
                    self.print_output("")
                    continue

                m = re.search('(?:^PYTHON)', line)
                if m is not None:
                    self.python_block = True
                    continue

            else:

                m = re.search('(?:^END PYTHON)', line)
                if m is not None:
                    self.python_block = False
                    continue
                else:
                    self.print_output(line)
        #(?:^PRINT)\W(["'])(?:(?=(\\?))\2.)*?\1
        self.inputFile.close()
        self.outputFile.close()
    def print_output(self, text = ''):
        indents = ""
        for i in range(0, self.indentLevel):
            indents += "\t"
        print(indents + text)
        self.outputFile.write(indents + text + "\n")
        

def flash(file, path = None):
    import uflash, os

    # Make a hex
    try:
        # Load File contents
        f = open(file, "r")
        script = f.read()
        # Actually hex it
        python_hex = uflash.hexlify(script.encode('utf-8'))
    except:
        # Opps that didnt work...
        return TibcStatus.HEX_GEN_ERROR;

    # Add it to MicroPython
    micropython_hex = uflash.embed_hex(uflash._RUNTIME, python_hex)

    # Did they manually specify path?
    if path is None:
        path = uflash.find_microbit()
        if path is None:
            # Cant find it!
            return TibcStatus.NOT_FOUND

    # So does it really ecist?
    if path and os.path.exists(path):
        hex_file = os.path.join(path, 'micropython.hex')
        # Save to microbit
        uflash.save_hex(micropython_hex, hex_file)
        # Yay it worked!
        return TibcStatus.SUCCESS;
    else:
        # Still doesnt exist
        return TibcStatus.NOT_FOUND

_HELP_TEXT = """
Tibc - Tiborcim Transpiler / MicroPython Flasher\r\n
 (C) Copyright Alexander Brown 2016\r\n

 Uses uFlash (http://uflash.readthedocs.org/) for flashing a Micro:Bit\r\n
"""

if __name__ == "__main__":
    import sys
    import argparse
    argv = sys.argv[1:]
    try:
        parser = argparse.ArgumentParser(description=_HELP_TEXT)
        parser.add_argument('source', nargs='?', default=None, help="File to transpile & flash. use -p if source is python")
        parser.add_argument('target', nargs='?', default=None, help="Path to Micro:Bit for when multiple are connected or not found")
        parser.add_argument('-p', '--python', default=False, action='store_true',
                            help="File is already Python.")
        args = parser.parse_args(argv)
        if args.python is False:
            compiler(args.source)
            args.source += '.py'
        flash(args.source, args.target)
    except Exception as ex:
        # The exception of no return. Print the exception information.
        print(ex)