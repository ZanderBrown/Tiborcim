#! /usr/bin/env python3

from enum import Enum

class TibcStatus(Enum):
    HEX_GEN_ERROR = 1
    NOT_FOUND = 2
    SUCCESS = 3

class TiborcimSyntaxError(Exception):
    def __init__(self, text):
        super(text)

_VERSION = (0, 1, 7, "BETA")

def get_version():
    return '.'.join([str(i) for i in _VERSION])

class compiler:
    def __init__(self, file, output = None):
        import re
        self.file_input = open(file, "r")
        if output is None:
            output = file + '.py'
        self.file_output = open(output, "w")
        self.content = self.file_input.readlines()

        self.indent_level = 0
        self.tmp_vars = 0
        self.python_block = False
        self.function_block = False
        self.code_input_used = False
        self.random_imported = False
        self.radio_imported = False
        
        self.functions = []
        self.code_header = [
            '# Generated by Tiborcim' + "\n",
            'from microbit import *' + "\n"
        ]
        self.code_input = [
            'def read_keys():' + "\n",
            "\t" +  'if button_a.is_pressed() and button_b.is_pressed():' + "\n",
            "\t\t" +  'return \'C\'' + "\n",
            "\t" +  'elif button_a.is_pressed():' + "\n",
            "\t\t" +  'return \'A\'' + "\n",
            "\t" +  'elif button_b.is_pressed():' + "\n",
            "\t\t" +  'return \'B\'' + "\n",
            "\t" +  'else:' + "\n",
            "\t\t" +  'return \'\'' + "\n"
        ]
        self.code = ["\n"]

        self.regexs = {
            'OR':           r'\bOR\b(?=([^\"]*\"[^\"]*\")*[^\"]*$)',
            'AND':          r'\bAND\b(?=([^\"]*\"[^\"]*\")*[^\"]*$)',
            'NOT':          r'\bNOT\b(?=([^\"]*\"[^\"]*\")*[^\"]*$)',
            'PSET':         r'PSET\W([0-5]|.*)\W?,\W?([0-5]|.*)\W?,\W?([0-9]|.*)$(?=([^\"]*\"[^\"]*\")*[^\"]*$)',
            'PRINT':        r'^PRINT\W(.*)',
            'BROADCAST':    r'^BROADCAST\W(.*)'
        }
        
        for line in self.content:
            stripedline = line.strip()
            if self.python_block is False:
                # INKEY
                if re.search("INKEY\$(?=([^\"]*\"[^\"]*\")*[^\"]*$)", line.strip()) is not None:
                    self.code_input_used = True
                line = re.sub("INKEY\$(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "read_keys()", line.strip())

                # SCREEN
                line = re.sub("SCREEN(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "display.get_pixel", line.strip())

                # STR$
                line = re.sub("STR\$(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "str", line.strip())

                # INT
                line = re.sub("(?<!PR)INT(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "int", line.strip())

                # RECEIVE$
                m = re.search('(?:^RECEIVE\$(?=([^\"]*\"[^\"]*\")*[^\"]*$))', line.strip())
                if m is not None:
                    if not self.radio_imported:
                        self.code_header.append('import radio' + "\n")
                        self.radio_imported = True
                line = re.sub("RECEIVE\$(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "radio.receive()", line.strip())

                # RND
                if re.search("RND(?=([^\"]*\"[^\"]*\")*[^\"]*$)", line.strip()) is not None:
                    if not self.random_imported:
                        self.code_header.append('import random' + "\n")
                        self.random_imported = True
                line = re.sub("RND(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "random.random()", line.strip())

                # SCREEN
                line = re.sub("SHAKEN(?=([^\"]*\"[^\"]*\")*[^\"]*$)", "accelerometer.was_gesture(\"shake\")", line.strip())

                # NOT
                if re.search(self.regexs['NOT'], stripedline) is not None:
                    self.print_output(re.sub(self.regexs['NOT'], '!', stripedline))
                    continue

                # AND
                if re.search(self.regexs['AND'], stripedline) is not None:
                    self.print_output(re.sub(self.regexs['AND'], 'and', stripedline))
                    continue

                # OR
                if re.search(self.regexs['OR'], stripedline) is not None:
                    self.print_output(re.sub(self.regexs['OR'], 'or', stripedline))
                    continue

                # PRINT
                if re.search(self.regexs['PRINT'], stripedline) is not None:
                    # Wrap the argument in str() because display.scroll only accepts strings
                    self.print_output(re.sub(self.regexs['PRINT'], r'display.scroll(str(\1))', stripedline))
                    continue

                # BROADCAST
                if re.search(self.regexs['BROADCAST'], stripedline) is not None:
                    self.print_output(re.sub(self.regexs['BROADCAST'], r'radio.send(str(\1))', stripedline))
                    if not self.radio_imported:
                        self.code_header.append('import radio' + "\n")
                        self.radio_imported = True
                    continue

                # RADIO
                m = re.search('(?:^RADIO)', line.strip())
                if m is not None:
                    if not self.radio_imported:
                        self.code_header.append('import radio' + "\n")
                        self.radio_imported = True
                    if line.strip()[6:].strip() == 'ON':
                        self.print_output('radio.on()')
                    else:
                        self.print_output('radio.off()')
                    continue

                # SHOW
                m = re.search('(?:^SHOW)', line.strip())
                if m is not None:
                    self.print_output('display.show(str(' + line.strip()[4:].strip() + '))')
                    continue

                # IMAGE
                m = re.search('(?:^IMAGE)', line.strip())
                if m is not None:
                    # cast string (of form "12345:67890....") to Micro:Bit image
                    self.print_output('display.show(Image(' + line.strip()[5:].strip() + '))')
                    continue

                # SLEEP
                m = re.search('(?:^SLEEP)', line.strip())
                if m is not None:
                    # Multiply the argument by 1000 to convert to miliseconds
                    self.print_output('sleep((' + line.strip()[5:].strip() + ')*1000)')
                    continue

                # SUB
                m = re.search('(?:^SUB) (\w+)', line.strip())
                if m is not None:
                    self.functions.append(m.group(1))
                    self.function_block = True
                    if line.strip()[-1:] == ')':
                        self.print_output('def ' + line.strip()[3:].strip() + ':')
                    else:
                        self.print_output('def ' + line.strip()[3:].strip() + '():')
                    self.indent_level_old = self.indent_level
                    self.indent_level = 1
                    continue

                # END SUB
                m = re.search('(?:^END SUB)', line.strip())
                if m is not None:
                    self.function_block = False
                    self.print_output('')
                    self.indent_level = self.indent_level_old
                    continue

                for fun in self.functions:
                    m = re.search('(?:^' + fun + ')', line.strip())
                    if m is not None:
                        self.print_output(line.strip())

                # PSET
                if re.search(self.regexs['PSET'], stripedline) is not None:
                    self.print_output(re.sub(self.regexs['PSET'], r'display.set_pixel(\1,\2,\3)', line.strip()))
                    continue

                # IF
                m = re.search('(?:^IF)', line.strip())
                if m is not None:
                    line = re.sub('=', ' == ', line)
                    self.print_output()
                    self.print_output('if (' + str.strip(line[2:-5]) + '):')
                    self.indent_level += 1
                    continue

                # ELSEIF
                m = re.search('(?:^ELSEIF)', line.strip())
                if m is not None:
                    line = re.sub('=', ' == ', line)
                    self.indent_level -= 1
                    self.print_output()
                    self.print_output('elif (' + str.strip(line[6:-5]) + '):')
                    self.indent_level += 1
                    continue

                # Comment
                m = re.search('(?:^\')', line.strip())
                if m is not None:
                    self.print_output('#' + line)
                    continue

                # END IF
                m = re.search('(?:^END IF)', line.strip())
                if m is not None:
                    self.indent_level -= 1
                    continue

                # ELSE
                m = re.search('(?:^ELSE)', line.strip())
                if m is not None:
                    self.indent_level -= 1
                    self.print_output("else:")
                    self.indent_level += 1
                    continue

                # FOR
                m = re.search('(?:^FOR) ([^\s]+)\s?=\s?([^\s]+) TO ([^\s]+)', line.strip())
                if m is not None:
                    self.print_output("for " + m.group(1) + " in range(" + m.group(2) + ",(" + m.group(3) + ")+1):")
                    self.indent_level += 1
                    continue

                # NEXT
                m = re.search('(?:^NEXT)', line.strip())
                if m is not None:
                    self.indent_level -= 1
                    continue

                # WHILE
                m = re.search('(?:^WHILE)', line.strip())
                if m is not None:
                    line = re.sub('(?<!\<)(?<!\>)(?<!\!)=', ' == ', line)
                    self.print_output()
                    self.print_output('while (' + str.strip(line[5:]) + '):')
                    self.indent_level += 1
                    continue

                # WEND (End While)
                m = re.search('(?:^WEND)', line.strip())
                if m is not None:
                    self.indent_level -= 1
                    continue

                # PYTHON
                m = re.search('(?:^PYTHON)', line.strip())
                if m is not None:
                    self.python_block = True
                    continue

                # Variable Assignment
                m = re.search('\=(?=([^\"]*\"[^\"]*\")*[^\"]*$)', line.strip())
                if m is not None:
                    self.print_output(line.strip())
                    continue
            else:
                # END PYTHON
                m = re.search('(?:^END PYTHON)', line.strip())
                if m is not None:
                    self.python_block = False
                    continue
                else:
                    self.print_output(line)

        self.save_output();
        self.file_input.close()
        self.file_output.close()
    def print_output(self, text = ''):
        indents = ""
        for i in range(0, self.indent_level):
            indents += "\t"
        if self.function_block:
            self.code_header.append(indents + text + "\n")
        else:
            self.code.append(indents + text + "\n")
    def save_output(self):
        for line in self.code_header:
            print(line)
            self.file_output.write(line)

        if self.code_input_used:
            for line in self.code_input:
                print(line)
                self.file_output.write(line)

        for line in self.code:
            print(line)
            self.file_output.write(line)

def flash(file, path = None):
    import tiborcim.contrib.uflash as uflash, os

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

def run():
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


if __name__ == "__main__":
    run()