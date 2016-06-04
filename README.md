# Tiborcim
BASIC for the Micro:Bit

The plan is to a create a source to source (or trans-)complier to take Tiborcim a custom language with syntax as close to BBC BASIC as possible and generate MicroPython code for the BBC Micro:Bit

## Tibc.py
The 'compiler'. Why the name? cc, vbc, valax, tsc... sort of set a trend and tiborcimc was a bit long.

### Usage
`tibc.py [-h] [-p] [source] [target]`

where -h print's help, -p for flashing a file that is already python, source being the filename and source being the location of your microbit (only needed if it's not found)

## Tiborcim.py
A simple editor

### Usage
The main window consists of a menu bar and two tabs
the first tabs is for Tiborcim source where as the second shows the generated MicroPython source
The menubar provide standard controls for managing file and options to flash the code

## Language
### Hello World
The Tiborcim
```
PRINT "Hello, World!"
```
represents the following MicroPython
```
from microbit import *

display.scroll("Hello, World!")
```
no prizes for quessing what the microbit does...

### Current Tiborcim statements
#### PRINT
Equivalent to display.scroll()
```
PRINT "Somestring"
```

#### Flow
##### IF .. ELSEIF .. ELSE .. END IF
Simple logic
```
IF (1 < 10) THEN
PRINT "1 is less than 10"
ELSEIF (2 < 5) THEN
PRINT "1 is not less then 10 but 2 is less than 5"
ELSE
PRINT "You need to work on your Maths"
END IF
```
#### Pixels
##### SCREEN
Returns the brightness of the pixel at x, y
```
PRINT SCREEN (x, y)
```
##### PSET
Sets the brightness of pixel x, y to z
```
PSET x, y, z
```

#### PYTHON .. END PYTHON
allows the use of pure python code in a Tiborcim script
e.g.:
```
PYTHON
a = 'hi'
a += ' again'
END PYTHON

PRINT a
```


#### Planned
| Function        | Does                                                                                            |
| --------------- | ------------------------------                                                                  |
| Variables       | Currently vaiables can only be created and modified within PYTHON blocks (can be used anywhere) |
| DO .. WHILE     | Loop code while condition is true                                                               |

## Whats it written in?
The 'compiler' and sample DE (i would say IDE but it isn't) are written in Python3. I am to be as Pythonic a possible.

### Dependencies
The goal is to have a few dependencies as possible outside the package itself hence our current editor uses Tkinter although a GTK3 (PyGObject) environment is planned as an optional extra.

## Why the name?
Write it backwards.

### Seriousley
Imaginative i know. Other name's were considred but just didn't feel right

### How do you say that?!
Tib - or - kim is how i say it aloud.
