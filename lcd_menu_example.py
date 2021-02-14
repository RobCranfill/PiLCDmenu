#!/usr/bin/python3
# Simple example.

from midi_cc import MidiCC
from lcd_menu import LCDMenu
import time
import threading


def loadFile(filename):
    """
    Load the indicated JSON file into a list of lists of MIDI objects.
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

    # Since this is just an example, we will just print out the selected item,
    # instead of actually doing something with it.
    #
    print(f"callbackHandler: got object of type {type(midicc_obj)}")
    print(f"callbackHandler: {midicc_obj}") # renders with 'str()'
    print(f"callbackHandler: '{midicc_obj.kitName}', CC {midicc_obj.controlCode}")


# Main code
#
if __name__ == "__main__":

    menuData = loadFile("sr18_small_example.json")
    menu = LCDMenu(menuData, callbackHandler, buttonsOnRight=True)

    # We create this event to wait on, but it never comes. How sad.
    # (The menu handler, and this example, is interrupt driven.)
    #
    waitThread = threading.Event()
    try:
        waitThread.wait()
    except KeyboardInterrupt:
        menu.clearScreen()
        menu.turnOffBacklight()
