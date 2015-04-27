# LED Controller class
#
# This is just a place holder for now. Future revisons should run as a singleton thread with locking
# The WSHandler will than dispatch the effect to this controller
# 
# Author: Sebastian Meyer <https://github.com/archi>

import threading
import time
from neopixel import *

# LED configuration, based on examples by Jeremy Garff:
LED_COUNT      = 40      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 32      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = True    # True to invert the signal (when using NPN transistor level shift)

class LEDController ():
    def __init__ (self):
        # Create NeoPixel object with appropriate configuration.
        self.leds = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.leds.begin()

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.leds.numPixels()):
            self.leds.setPixelColor(i, color)
            self.leds.show()
            time.sleep(wait_ms/1000.0)

    def fastWipe(self, color):
        for i in range(self.leds.numPixels ()):
            self.leds.setPixelColor(i, color)
        self.leds.show ()

    def setColor (self, ledid, color):
        if ledid > self.leds.numPixels ():
            return
        self.leds.setPixelColor (ledid, color)

    def show (self):
        self.leds.show ()
