#!/usr/bin/python3
# Simple example.

from midi_cc import MidiCC
from lcd_menu import LCDMenu
import time
import threading


def loadFile(filename):
    """
    Load the indicated JSON file
    """
    print(f"Parsing JSON file '{filename}'....")
    f = open(filename, "r")
    fcontents = f.read()
    # print(f" read: {fcontents}\n")
    # print(f" json: {json.loads(fcontents)}\n")
    return MidiCC.decodeFromJSON(fcontents)

def callbackHandler(midicc_obj):
    """
    This is the method that will be invoked when the "do it" button is pressed.
    """
    print(f"callbackHandler: got object of type {type(midicc_obj)}")
    print(f"callbackHandler: {midicc_obj}") # renders with 'str()'
    print(f"callbackHandler: '{midicc_obj.kitName}', CC {midicc_obj.controlCode}")


# Main code
#
if __name__ == "__main__":

    menuData = loadFile("sr18_small_example.json")
    menu = LCDMenu(menuData, callbackHandler)

    # We create this event to wait on, but it never comes. How sad.
    # This program is interrupt driven.
    waitThread = threading.Event()

    try:
        menu.drawMenu()
        waitThread.wait()
    except KeyboardInterrupt:
        menu.clearScreen()
        menu.turnOffBacklight()
