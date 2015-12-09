# yarns-editor
A software MIDI editor for Mutable Instruments Yarns

## Usage:
Usage is simple:

1. Connect Yarns to a MIDI interface on your computer.
2. Set Yarns to use a remote control channel ("RC" on the panel).
3. Run Yarns Editor, and choose the same RC channel that Yarns is set to.
4. Point and click your way to victory! 

## Features:
* Yarns is deep, and editing complex layouts via the encoder can be cumbersome.  This program makes editing Yarns a snap!
* Open source! Free!
* Randomize anything! Generate complex arpeggios and Euclidean patterns with the click of a button!
* Cross platform! Works on Windows, Mac, & Linux!

## Dependencies:
* python2.7: https://www.python.org/
* wxpython: http://www.wxpython.org/
* rtmidi-python: https://github.com/superquadratic/rtmidi-python
* natsort: https://pypi.python.org/pypi/natsort

## Dev Environment Setup:
* Install Python: download and install the latest version of Python2: https://www.python.org/
* Install wxPython: download and install the latest 32 bit version of wxPython: http://www.wxpython.org/
* Open a command prompt/terminal and upgrade pip: python -m pip install --upgrade pip
* Then run this to install the required modules: pip install rtmidi-python natsort
* Ready to go! Open a command prompt/terminal, change to the project directory, and run: python editor.py