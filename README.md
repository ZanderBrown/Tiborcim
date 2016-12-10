![Logo](cim.png "Tiborcim Logo")

# Tiborcim
[![Build Status](https://travis-ci.org/ZanderBrown/Tiborcim.svg?branch=master)](https://travis-ci.org/ZanderBrown/Tiborcim)

BASIC for the Micro:Bit

The plan is to a create a source to source (or trans-)complier to take Tiborcim a custom language with syntax as close to BBC BASIC as possible and generate MicroPython code for the BBC Micro:Bit

Targeted and tested on Python 3.5

## Install

Tiborcim is packaged with python setup tools and can be installed with the command `python setup.py install` 

## tibc
Only accessable when Tiborcim is installed

The 'compiler'. Why the name? cc, vbc, valac, tsc... sort of set a trend and tiborcimc was a bit long.

### Usage
`tibc [-h] [-p] [source] [target]`

where -h prints help, -p for flashing a file that is already python, source being the file name and source being the location of your Micro:Bit (only needed if it's not found)

## Cim
A simple editor for Tiborcim

When Tiborcim is installed Cim can be accesed with the command `cim` or linux user can find it in the applications menu

If you have choosen not to install Tiborcim you can still access Cim by executing `run.py`

### Usage
The main window consists of a menu bar and two tabs
the first tabs is for Tiborcim source where as the second shows the generated MicroPython source
The menu-bar provide standard controls for managing file and options to flash the code

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
no prizes for guessing what the Micro:Bit does...

### Current Tiborcim statements
#### PRINT
Equivalent to display.scroll()
```
PRINT "Some string"
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
##### WHILE .. WEND
Repeat code while condition is true
```
x = 0
WHILE x < 10
	x = x + 1
WEND
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
#### Buttons
##### INKEY$
returns the current held button in the for of A, B or C with A & B representing their corresponding buttons while C is A+B simultaneously
if nothing is pressed '' is returned
```
WHILE 1
	x = INKEY$
	IF x = 'A' THEN
		PRINT 'A'
	ELSEIF x = 'B' THEN
		PRINT 'B'
	ELSEIF x = 'C' THEN
		PRINT 'A+B'
	END IF
END WHILE
```
#### Variables
Most standard Python operations are available although ++ += -- -= are discouraged as they are not available in BASIC
Comparison operations are a little more complicated. Currently supported are = < >. >= => <> NOT() are planned
##### STR$
Casts a value to string
```
a = 10
b = STR$(a)
' b is '10' not 10
```

##### INT
Casts a value to integer
```
a = 10.6789
b = INT(a)
' b is 10 not 10.6789
```

##### RND
Returns a random number between 0 & 1
```
dice = INT(RND * 6 + 1)
```

##### SHAKEN
True or False depending on whether or not the device was shaken since it was last called
```
WHILE 1
	IF SHAKEN THEN
		times = times + 1
		SHOW times
	END IF
WEND
```

##### RECEIVE$
Returns the latest message received by the radio
```
IF RECEIVE$ = "hi" THEN
	PRINT "hi"
END IF
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

#### SUB .. END SUB
Create a subroutine. subroutines are like functions but do not return a value.
SUBs 
```
SUB test
	PRINT "Hi"
END SUB

test()
```

#### FOR .. NEXT

// TODO: explain


## What is it written in?
The 'compiler' and sample DE (I would say IDE but it isn't) are written in Python 3. I aim to be as Pythonic a possible.

### Dependencies
The goal is to have a few dependencies as possible outside the package itself hence our current editor uses Tkinter although a GTK3 (PyGObject) environment is planned as an optional extra.

## Why the name?
Write it backwards.

### Seriously
Imaginative I know. Other name's were considered but just didn't feel right

### How do you say that?!
`Tib - or - kim` is how I say it aloud. I'm aware that is not how it's written but as the author i retain the right to be akward with my naming

## Notes
GitHub shows commits at weird times. unfortunately this occurred through a combination of a incorrectly set clock and a corrupted `.git` directory. long story short some commits show twice, some not at all & others at 1 o'clock in the morning for no apparent reason.