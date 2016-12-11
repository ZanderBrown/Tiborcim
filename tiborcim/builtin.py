import tiborcim.lang as lang

PRINT = lang.Item('PRINT')
PRINT.inline = False
PRINT.argcount = 1
PRINT.replacement = r'display.scroll(str(\1))'

PSET = lang.Item('PSET')
PSET.inline = False
PSET.argcount = 3
PSET.replacement = r'display.set_pixel(\1,\2,\3)'

BUILTINS = [PRINT, PSET]
