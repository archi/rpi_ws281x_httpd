# LED Controller class
#
# This is just a place holder for now. Future revisons should run as a singleton thread with locking
# The WSHandler will than dispatch the effect to this controller
# 
# Author: Sebastian Meyer <https://github.com/archi>

import threading
import time
import subprocess
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

        self.colorCodes = [
                Color(255,255,255),
                Color(0,0,0),
                Color(0,0,127),
                Color(0,147,0),
                Color(255,0,0),
                Color(127,0,0),
                Color(156,0,156),
                Color(252,127,0),
                Color(255,255,0),
                Color(0,252,0),
                Color(0,147,147),
                Color(0,255,255),
                Color(0,0,252),
                Color(255,0,255),
                Color(127,127,127),
                Color(210,210,210)]


    def fastWipe(self, color):
        for i in range(self.leds.numPixels ()):
            self.leds.setPixelColor(i, color)

    def setColor (self, ledid, color):
        if ledid > self.leds.numPixels ():
            return
        self.leds.setPixelColor (ledid, color)

    def show (self):
        self.leds.show ()

    def xyToId (self, x, y):
        return y * 8 + x

    def colorCode (self, code):
        return self.colorCodes[code]

    def char (self, c):
        if len(c) != 1:
            return False

        p = subprocess.Popen(['toilet', '-F', 'gay', '-f', 'block', '-E', 'irc', c], stdout=subprocess.PIPE)
        t, err = p.communicate ()

        x = 0
        y = 0
        c = Color (0,0,0)

        p = 0
        pp = len (t)
        while p < pp:
            if t[p] == " ":
                if t[p+1] == " ":
                    p+=1
                x+=1
            elif t[p] == "_":
                i = self.xyToId (x,y - 1)
                self.leds.setPixelColor (i, c)
                p+=1
                x+=1
            elif t[p] == "":
                cc = int(t[p+1])
                if t[p+2] != "_":
                    cc*=10
                    cc+=int(t[p+2])
                    p+=2
                else:
                    p+=1
                c = self.colorCode (cc)
            elif t[p] == "\n":
                x = 0
                y+=1
            p+=1

        return True
