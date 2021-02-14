# PiLCDmenu
Simple menu system for Adafruit 1.3” LCD display.

The [Adafruit 1.3" TFT LCD](https://www.adafruit.com/product/4484) 240x240 pixel display has two buttons on it that can be accessed via the Pi's
GPIO interface. This library implements a simple, easy-to-use menu system that allows you to
have a rudimentary GUI in a tiny package.

The menu is specified using a JSON file. The menu system consists of one or more pages, each with one to nine selectable items. (TODO: Allow more than 9 items? See 'issues' for ideas.)

Each menu item is associated with an object that is passed back when that item is selected from the menu.

Here's what it looks like in action:

![screenshot](screenshot.jpg)

My initial use for this is as a front-end for selecting drum kit samples on an SR18 drum machine. :-)

Requirements
* Raspberry Pi and Raspbian OS (I used 10/Buster) or some other Linux would probably be fine
* Python 3.7 (?) or better (I used 3.7.3)
* [Adafruit 1.3" TFT LCD](https://www.adafruit.com/product/4484)
* Python Imaging Library - I used 'Pillow', a fork by Alex Clark and contributors (https://github.com/python-pillow/Pillow/)
* Adafruit libraries:
  * [CircuitPython](https://github.com/adafruit/circuitpython)
  * Adafruit_PureIO
  * adafruit_blinka
  * adafruit_bus_device
  * adafruit_platformdetect
  * adafruit_rgb_display

Some (all?) of the above dependencies may come automagically with CircuitPython. Would someone like to document what-all needs to be installed, minimally?
