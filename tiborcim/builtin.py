import tiborcim.lang as lang

PRINT = lang.Item('PRINT')
PRINT.inline = False
PRINT.argcount = 1
PRINT.replacement = r'display.scroll(str(\1))'

PSET = lang.Item('PSET')
PSET.inline = False
PSET.argcount = 3
PSET.replacement = r'display.set_pixel(\1,\2,\3)'

AND = lang.Item('AND')
AND.inline = True
AND.argcount = 0
AND.replacement = r'and'

OR = lang.Item('OR')
OR.inline = True
OR.argcount = 0
OR.replacement = r'or'

NOT = lang.Item('NOT')
NOT.inline = True
NOT.argcount = 0
NOT.replacement = r'not'

SHOW = lang.Item('SHOW')
SHOW.inline = False
SHOW.argcount = 1
SHOW.replacement = r'display.show(str(\1))'

IMAGE = lang.Item('IMAGE')
IMAGE.inline = False
IMAGE.argcount = 1
IMAGE.replacement = r'display.show(Image(\1))'

SLEEP = lang.Item('SLEEP')
SLEEP.inline = False
SLEEP.argcount = 1
SLEEP.replacement = r'sleep((\1)*1000)'

SHAKEN = lang.Item('SHAKEN')
SHAKEN.inline = True
SHAKEN.argcount = 0
SHAKEN.replacement = r'accelerometer.was_gesture("shake")'

STR = lang.Item('STR\$')
STR.inline = True
STR.argcount = 1
STR.replacement = r'str(\1)'

INT = lang.Item('(?<!PR)INT')
INT.inline = True
INT.argcount = 1
INT.replacement = r'int(\1)'

SCREEN = lang.Item('SCREEN')
SCREEN.inline = True
SCREEN.argcount = 2
SCREEN.replacement = r'display.get_pixel(\1,\2)'

BUILTINS = [PRINT,
            PSET,
            AND,
            OR,
            NOT,
            SHOW,
            IMAGE,
            SLEEP,
            SHAKEN,
            STR,
            INT,
            SCREEN]
