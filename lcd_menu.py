#!/bin/python3
# a wrapper for LCD menus
# FIXME: NOT separated from the LCD drawing stuff.

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import RPi.GPIO as GPIO

class LCDMenu:
    """
    Being a class that implements an easy-to-use simple menu system for the Adafruit 1.3" LCD display.


    """
    def __init__(self, menuDataListOfLists, callback):
        """
        Constructor takes the data structure for the items to display, and the method to call back.

        Argments:
          menuDataListOfLists: A list of lists of objects. Each top-level list is a page
            of items to display; each item in the list will be displayed in the menu using
            its str() method. When an item is selected, it will be sent back to the caller
            via the next argument.
         callback: The method to call when an item is selected. That method must take
           one argument: the object that was selected.

        """
        self._callback = callback
        self._menuPages = menuDataListOfLists

        self._selectedPage = 0
        self._selectedItem = 0 # this could be the page-nav-item, or a menu-item

        self._initDisplay()
        self._drawMenu()


    ##################################################
    # Public methods

    def clearScreen(self):
        """
        Clear the entire screen to black.
        """
        self._draw.rectangle((0, 0, self._width, self._height), outline=0, fill=(0, 0, 0))
        self._disp.image(self._image, self._rotation)

    def turnOffBacklight(self):
        """
        Turn off the display's backlight. Saves power; extends life?
        """
        self._backlight.value = False


    ##################################################
    # Private methods

    @staticmethod
    def _init_button(pin):
        button = digitalio.DigitalInOut(pin)
        button.switch_to_input()
        button.pull = digitalio.Pull.UP
        return button

    def _setupGPIO(self):
        """
        Set up the RPi's GPIO pins to support the two pushbuttons on the display.

        Button A is geometrically, and physically, above B. For now.
        """
        global BUTTON_A_pin, BUTTON_B_pin
        BUTTON_A_pin = 24
        BUTTON_B_pin = 23

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(BUTTON_A_pin, GPIO.FALLING, callback=self._button_A_callback, bouncetime=300)
        GPIO.add_event_detect(BUTTON_B_pin, GPIO.FALLING, callback=self._button_B_callback, bouncetime=300)


    def _button_A_callback(self, channelIsIgnored):
        """
        Iterrupt handler to deal with Button A, "do it".
        """
        # print(f"button A - do: {self._selectedPage}.{self._selectedItem}")

        # Next page?
        if self._selectedItem == 0:
            self._selectedPage += 1
            if self._selectedPage == len(self._menuPages):
                self._selectedPage = 0
            self._drawMenu()
            return

        # Not 'next page' - it's an item selection.
        menuItemObj = self._menuPages[self._selectedPage][self._selectedItem-1]
        # print(f" LCDMeeu -> SEND CC {ccObj.controlCode} ({ccObj.kitName})")
        self._callback(menuItemObj)


    def _button_B_callback(self, channel):
        """
        Iterrupt handler to deal with button B, "move the cursor" (selectedItem).
        """
        self._selectedItem += 1
        if self._selectedItem == len(self._menuPages[self._selectedPage])+1:
            self._selectedItem = 0
        # print(f"button B - selectedItem: {selectedItem}")
        self._drawMenu()


    @staticmethod
    def _textColorForIndex(index, selected):
        return "#FF0000" if index == selected else "#FFFFFF"

    def _drawWidgets(self, yTop):
        """ These are the non-text menu things.
        """
        WIDGET_VERTICAL_X = 210
        WIDGET_EXECUTE_Y  =  45
        WIDGET_MOVE_Y     = 150

        # header/menuitems separator
        self._draw.line((0, self._yTop+1) + (WIDGET_VERTICAL_X, self._yTop+1), fill="#FFFFFF")

        self._draw.line((WIDGET_VERTICAL_X, 0, WIDGET_VERTICAL_X, 240), fill="#FFFFFF")

        x = WIDGET_VERTICAL_X + 6
        y = WIDGET_EXECUTE_Y
        s = 20
        self._draw.polygon( (x,y, x+s,y+s/2, x,y+s, x,y), fill="#FFFFFF")

        x = WIDGET_VERTICAL_X + 6
        y = WIDGET_MOVE_Y
        s = 20
        self._draw.polygon( (x,y, x+s,y, x+s/2,y+s, x,y), fill="#FFFFFF")

    # uses globals: selectedPage, selectedItem
    def _drawMenu(self):
        self.clearScreen()
        y = self._yTop

        dispPage = self._selectedPage + 1 # the current page's "display" value - not zero-based
        nextP = dispPage + 1
        if nextP == len(self._menuPages)+1:
            nextP = 1
        self._draw.text((30, y),
            f"Go to Page {nextP}", font=self._font, fill=LCDMenu._textColorForIndex(0, self._selectedItem))
        y += self._fontHeight

        self._drawWidgets(y)

        pageMenu = self._menuPages[self._selectedPage]
        for i in range(len(pageMenu)):

            # This renders the menu item using it's "str" method.
            #
            self._draw.text((0, y),
                f"{str(pageMenu[i])}", font=self._font, fill=LCDMenu._textColorForIndex(i+1, self._selectedItem))
            y += self._fontHeight

        # Display built image
        self._disp.image(self._image)

    def _initDisplay(self):
        ############################################################
        # Create the ST7789 display object

        # global _disp, _draw, _width, _height, _image, _rotation, _yTop, _font, _fontHeight
        # global _backlight

        self._disp = st7789.ST7789(
            board.SPI(),
            cs=digitalio.DigitalInOut(board.CE0),
            dc=digitalio.DigitalInOut(board.D25),
            rst=None,
            baudrate=64000000,
            width=240,
            height=240,
            x_offset=0,
            y_offset=80,
        )
        # for convenience
        self._width  = self._disp.height
        self._height = self._disp.width

        self._image = Image.new("RGB", (self._width, self._height))
        self._rotation = 0
        self._draw = ImageDraw.Draw(self._image)

        buttonA = self._init_button(board.D23)
        buttonB = self._init_button(board.D24)

        self.clearScreen()
        self._setupGPIO()

        padding = -2
        self._yTop = padding
        bottom = self._height - padding

        self._font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        self._fontHeight = self._font.getsize("X")[1]

        # Turn on the backlight
        self._backlight = digitalio.DigitalInOut(board.D22)
        self._backlight.switch_to_output()
        self._backlight.value = True
