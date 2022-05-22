# An easy-to-use simple menu system for the Adafruit 1.3" LCD display
# See https://github.com/RobCranfill/PiLCDmenu for more info.
# (c)2022 robcranfill@robcranfill.net

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import RPi.GPIO as GPIO


REGULAR_COLOR   = "#FFFFFF"
HIGHLIGHT_COLOR = "#FF0000"

WIDGET_AREA_WIDTH  =  30
WIDGET_EXECUTE_Y   =  50
WIDGET_MOVE_Y      = 150
HEADER_AREA_HEIGHT =  24


class LCDMenuPage:
    """
    One page's data.
    The string is the page title; the item objects will be rendered using their str method.
    """
    def __init__(self, nameString, objectList):
        self.title = nameString
        self.objects = objectList

    def __str__(self):
        """ Really only used for debugging.
        """
        result = self.title + ": "
        for o in self.objects:
            result += ", " + o
        return result

    def __repr__(self):
        return f"LCDM({self.nameString}, {self.itemObjectList})"
        # return self.__str__()

class LCDMenuData:
    """
    The whole structure to be passed to the menu display system.
    """
    def __init__(self, listOfMenuPages):
        self.pages = listOfMenuPages

    def __str__(self):
        """This is the method that the menu code will use to render each item.
        """
        result = ""
        for p in self.pages:
            result += " " + p.title
        return result

    def __repr__(self):
        return self.__str__()

class LCDMenu:
    """ Being a class that implements an easy-to-use simple menu system
        for the Adafruit 1.3" LCD display.
    """
    def __init__(self, menudata, callback, buttonsOnRight=True):
        """
        Constructor takes the data structure for the items to display, 
        and the method to call back.

        Argments:
          menuDataListOfLists: Basically a list of lists of objects. Each top-level list is a page
            of items to display; each item in the list will be displayed in the menu using
            its str() method. When an item is selected, it will be sent back to the caller
            via the next argument.
         callback: The method to call when an item is selected. That method must take
           one argument: the object that was selected.
         buttonsOnRight: Boolean indicating which way the display is oriented.
        """
        self._callback = callback
        self._menuData = menudata

        if buttonsOnRight:
            self._rotation = 0
        else:
            self._rotation = 180

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

    def _setupGPIO(self):
        """
        Set up the RPi's GPIO pins to support the two pushbuttons on the display.

        Button A is geometrically, and physically, above B. (For now - rotation?)
        """
        BUTTON_A_pin = 24
        BUTTON_B_pin = 23

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if self._rotation == 0:
            GPIO.add_event_detect(BUTTON_A_pin, GPIO.FALLING, callback=self._button_A_callback, bouncetime=300)
            GPIO.add_event_detect(BUTTON_B_pin, GPIO.FALLING, callback=self._button_B_callback, bouncetime=300)
        else: # is this confusing?
            GPIO.add_event_detect(BUTTON_A_pin, GPIO.FALLING, callback=self._button_B_callback, bouncetime=300)
            GPIO.add_event_detect(BUTTON_B_pin, GPIO.FALLING, callback=self._button_A_callback, bouncetime=300)


    def _button_A_callback(self, channelIsIgnored):
        """
        Iterrupt handler to deal with Button A, "do it".
        """
        # print(f"button A - do: {self._selectedPage}.{self._selectedItem}")

        # Next page?
        if self._selectedItem == 0:
            self._selectedPage += 1
            if self._selectedPage == len(self._menuData.pages):
                self._selectedPage = 0
            self._drawMenu()
            return

        # Not 'next page' - it's an item selection.
        menuItemObj = self._menuData.pages[self._selectedPage].objects[self._selectedItem-1]
        self._callback(menuItemObj)


    def _button_B_callback(self, channelIsIgnored):
        """
        Iterrupt handler to deal with button B, "move the cursor" (selectedItem).
        """
        self._selectedItem += 1
        if self._selectedItem == len(self._menuData.pages[self._selectedPage].objects)+1:
            self._selectedItem = 0
        # print(f"button B - selectedItem: {selectedItem}")
        self._drawMenu()


    @staticmethod
    def _textColorForIndex(index, selected):
        return HIGHLIGHT_COLOR if index == selected else REGULAR_COLOR


    def _drawWidgets(self):
        """ These are the non-text things: two separator lines and two button icons.

        Returns the X coord that the menu items can be drawn at.
        """

        # 'go to page #'/menu items horizontal separator
        self._draw.line((0, HEADER_AREA_HEIGHT, self._width, HEADER_AREA_HEIGHT), fill=REGULAR_COLOR)

        # button widget vertical separator
        if self._rotation == 0:
            # print("Rotation is 0");
            widget_left_x = self._width - WIDGET_AREA_WIDTH
            widget_separator_x = widget_left_x
        else:
            # print("Rotation is 180");
            widget_left_x = 0
            widget_separator_x = WIDGET_AREA_WIDTH

        self._draw.line((widget_separator_x, HEADER_AREA_HEIGHT, widget_separator_x, self._height),
                        fill=REGULAR_COLOR)

        # the button icons
        x = widget_left_x + 6
        y = WIDGET_EXECUTE_Y
        s = 20
        self._draw.polygon( (x,y, x+s,y+s/2, x,y+s, x,y), fill=HIGHLIGHT_COLOR)

        y = WIDGET_MOVE_Y
        s = 20
        self._draw.polygon( (x,y, x+s,y, x+s/2,y+s, x,y), fill=REGULAR_COLOR)

        result = 0
        if self._rotation == 180:
            result = WIDGET_AREA_WIDTH
        return result


    def _drawMenu(self):
        """
        Draw the screen with the new state of affairs - something new selected, or new page.
        """
        self.clearScreen()

        # this gets us the left edge of the widget area
        x = self._drawWidgets()
        y = self._yTop

        pageMenu = self._menuData.pages[self._selectedPage]

        self._draw.text((0, y), pageMenu.title, font=self._font, fill=REGULAR_COLOR)

        # TODO: draw a right-arrow triangle, like the button?
        self._draw.text((175, y),
            f"NEXT", font=self._font, fill=LCDMenu._textColorForIndex(0, self._selectedItem))

        y += self._fontHeight
        for i in range(len(pageMenu.objects)):

            # This renders each menu item using its "str()" method.
            #
            self._draw.text((x, y),
                f"{str(pageMenu.objects[i])}", font=self._font, fill=LCDMenu._textColorForIndex(i+1, self._selectedItem))
            y += self._fontHeight

        # Display built image
        self._disp.image(self._image, self._rotation)


    def _initDisplay(self):
        """
        Set up the display board.
        """
        # Create the ST7789 display object
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
        self._draw = ImageDraw.Draw(self._image)

        self.clearScreen()
        padding = -2
        self._yTop = padding
        bottom = self._height - padding

        self._font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        self._fontHeight = self._font.getsize("X")[1]

        self._setupGPIO()

        # Turn on the backlight
        self._backlight = digitalio.DigitalInOut(board.D22)
        self._backlight.switch_to_output()
        self._backlight.value = True
