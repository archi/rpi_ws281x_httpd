# Minimalistic HTTP handler 
# 
# Interprets HTTP requests and dispatches them to the LEDController singleton
#
# Author: Sebastian Meyer <https://github.com/archi>

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from neopixel import *
from ledcontroller import LEDController

httpport = 8080
ctrl = LEDController ()

def getHex (s):
    i = int(s)
    if i >= 0 and i <= 255:
        return i
    return None

class WSHandler(BaseHTTPRequestHandler):

    def status(self, scode, msg=None):
        self.responded = True
        self.send_response (scode)
        self.send_header ('Content-type', 'text/html')
        self.end_headers ()
        if (msg != None):
            self.wfile.write ("Status " + str(scode) + ": " + msg + "\n<br>");
        else:
            self.wfile.write ("Status " + str(scode) + "\n<br>");
        return

    def do_GET(self):
        self.responded = False
        try:
            cmd = self.path.split ("/", 7)
            if (cmd[1] == 'test'):
                i = 0
                self.status (200)
                self.wfile.write ("Length: " + str(len(cmd) - 1));
                for s in cmd:
                    if i == 0 or i == 1:
                        i+=1
                        continue
                    self.wfile.write ("<br>" + str(i-1) + ": " + s)
                    i+=1

            elif (cmd[1] == 'clear'):
                ctrl.fastWipe (Color(0,0,0))
                self.status (200, "Clearing")
            
            elif (cmd[1] == 'full'):
                ctrl.fastWipe (Color(255,255,255))
                self.status (200, "Clearing")

            elif (cmd[1] == 'fullcolor'):
                e = False
                if len(cmd) != 5:
                    e = True
                else:
                    r = getHex (cmd[2])
                    g = getHex (cmd[3])
                    b = getHex (cmd[4])

                    if r == None or g == None or b == None:
                        e = True

                if e:
                    self.status (400, "Bad Request, use fullcolor/&ltr&gt;/&lt;g&gt;/&lt;b&gt;<br> with values for R G B in 0..255.")
                    return

                ctrl.fastWipe (Color (r,g,b))
                self.status (200, "OK")

            elif (cmd[1] == 'set'):
                e = False
                if len(cmd) != 6:
                    e = True
                else:
                    r = getHex (cmd[3])
                    g = getHex (cmd[4])
                    b = getHex (cmd[5])

                    if r == None or g == None or b == None:
                        e = True

                if e:
                    self.status (400, "Bad Request, use set/&lt;id&gt;/&ltr&gt;/&lt;g&gt;/&lt;b&gt;<br> with values for R G B in 0..255. Setting an out-of-bounds LED is a NOP")
                    return

                ctrl.setColor (int(cmd[2]), Color (r,g,b))
                ctrl.show ()
                self.status (200, "OK")

            if (not self.responded):
                self.status (404, "Not found: " + self.path);
            return
        except Exception as e:
            if not self.responded:
                self.status (500, "Exception: " + str(e))
            else:
                self.wfile.write ("Exception: " + str(e))
            return
     
def main():
    try:
        server = HTTPServer(('', httpport), WSHandler)
        print 'Staring rpi_ws281x_httpd on port ' + str(httpport)
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down rpi_ws281x_httpd'
        server.socket.close()

if __name__ == '__main__':
    main()

