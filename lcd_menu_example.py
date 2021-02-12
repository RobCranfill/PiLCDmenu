#!/usr/bin/python3
# Simple example.

from midi_cc import MidiCC
from lcd_menu import LCDMenu
import time


def callbackHandler(midicc):
    """
    This is the method that will be invoked when the "do it" button is pressed.
    """
    print(f"callbackHandler: {midicc}")


# Main code
#
if __name__ == "__main__":

    menu = LCDMenu(callbackHandler, filename="sr18_small_example.json")

    try:
        # TODO not really needed - replace with some kind of wait?
        while True:
            menu.drawMenu()
            # print("(main loop sleeping)")
            time.sleep(6000)
    except KeyboardInterrupt:
        menu.clearScreen()
        menu._backlight.value = False
