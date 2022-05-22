#!/usr/bin/python3
# Simple example.

from lcd_menu import LCDMenu, LCDMenuPage, LCDMenuData

import os # for shutting down the machine
import signal
import sys
import threading
import time


class LCDAction():
    """
    A somewhat ad-hoc class for implementing a "shut down" menu item.
    This could have been done more simply, using a String object, I suppose.
    """
    # Values for magicActionThing:
    ACTION_SHUT_DOWN = 0
    ACTION_EXIT = 1

    def __init__(self, displayString, magicActionThing):
        self.displayString = displayString
        self.magicActionThing = magicActionThing

    def __str__(self):
        """This is the method that the menu code will use to render each item.
        """
        return self.displayString

    def __repr__(self):
        return self.__str__()


def tidyUp():
    menu.clearScreen()
    menu.turnOffBacklight()


def callbackHandler(menu_obj):
    """
    This is the method that will be invoked when the "do it" button is pressed.
    """

    if isinstance(menu_obj, LCDAction):
        if menu_obj.magicActionThing == LCDAction.ACTION_EXIT:
            print("Exiting....")
            tidyUp()
            sys.exit(LCDAction.ACTION_EXIT)
        elif menu_obj.magicActionThing == LCDAction.ACTION_SHUT_DOWN:
            print("Halting system....")
            tidyUp()
            os.system('sudo shutdown -h now')
        else:
            print("Unknown action: ", menu_obj) # shouldn't happen
        return
    
    # Must be one of the 'regular' menu items.
    # You could check its type and Do The Right Thing with it.
    # Since this is just an example, we will simply print out the selected item,
    # instead of actually doing something with it.
    #
    print(f"callbackHandler: {menu_obj}") # renders with 'str()'


# Handler for 'die' signal.
def gotSIGWhatever(foo, fum):
    # If we get the signal, process an EXIT action.
    callbackHandler(LCDAction("mox nix", LCDAction.ACTION_EXIT))


# Main code
#
if __name__ == "__main__":

    # create some simple data...
    p1 = LCDMenuPage("Page One", ["Thing A", "Thing B", "Thing C"])
    p2 = LCDMenuPage("Page Two", ["Alpha", "Beta", "Gamma"])

    # ...and some fancier data.
    p3 = LCDMenuPage("Utils", 
     [LCDAction("Exit menu app", LCDAction.ACTION_EXIT),
      LCDAction("Shut down Pi",  LCDAction.ACTION_SHUT_DOWN)])

    data = LCDMenuData([p1, p2, p3])

    menu = LCDMenu(data, callbackHandler, buttonsOnRight=True)

    # When running headless, we can send this signal to stop the app.
    # (We are supposed to be able to send a SIGINT to get the same thing as ctrl-C,
    # but it doesn't seem to work. SIGUSR1 works.)
    signal.signal(signal.SIGUSR1, gotSIGWhatever)

    # We create this event to wait on, but it never comes.
    # (The menu handler, and this example, is interrupt driven.)
    #
    waitThread = threading.Event()
    try:
        waitThread.wait()
    except KeyboardInterrupt:
        print("\nExiting....")
        tidyUp()
