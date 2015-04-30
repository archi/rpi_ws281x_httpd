# Minimalistic HTTP handler 
# 
# Interprets HTTP requests and dispatches them to the LEDController singleton
#
# Author: Sebastian Meyer <https://github.com/archi>

import string,cgi,time,sys,traceback,urllib
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from ledcontroller import LEDController
from neopixel import *;
ctrl = LEDController ()

httpport = 80
test_mode = True

def getHex (s):
    i = 0
    try:
        i = int(s)
    except Exception:
        return None

    if i >= 0 and i <= 255:
        return i
    return None

def parseColor(raw):
    c = raw.split (",", 3)
    if len(c) != 3:
        return None
    r = getHex (c[0])
    g = getHex (c[1])
    b = getHex (c[2])
    if r == None or b == None or g == None:
        return None
    return Color (r,g,b)

class WSHandler(BaseHTTPRequestHandler):

    def doc(self, cmd, descr):
        self.wfile.write ('<b><a href='+cmd+'>'+cmd+'</a></b>: '+descr+'<br>')

    def status(self, scode, msg=None):
        self.responded = True
        self.send_response (scode)
        self.send_header ('Content-type', 'text/html')
        self.end_headers ()
        if (msg != None):
            if (msg):
                self.wfile.write ("Status " + str(scode) + ": " + msg + "\n<br>");
        else:
            self.wfile.write ("Status " + str(scode) + "\n<br>");
        return
        

    def do_GET(self):
        self.responded = False
        try:
            cmd = self.path.split ("/", 7)
            opts = len (cmd) - 2
            if opts == -1 or cmd[1] == "":
                self.status (200, False)
                self.wfile.write ("rpi_ws281x_httpd - <a href='http://www.github.com/archi/rpi_ws281x_httpd/'>Source on github</a><hr>Commands in this version:<br>")
                self.doc ("fill", "Set all LEDs to a given color")
                self.doc ("set", "Set a single LED to a given color")
                self.doc ("clear", "Clear all LEDs")
                self.doc ("char", "Draw a single char using toilet")
                self.doc ("chars", "Draw some chars using toilet")
                if test_mode:
                    self.doc ("test", "Test parameter count and splitting [debug option!]")
                self.wfile.write (" <hr>Usually, colors are specified as <i>r,g,b</i>, where each value of needs to be in the range of 0..255. I.e. white is 255,255,255 and black/off 0,0,0.")
                return

            elif test_mode and cmd[1] == 'test':
                i = 0
                self.status (200)
                self.wfile.write ("Length: " + str(opts - 1));
                for s in cmd:
                    if i == 0 or i == 1:
                        i+=1
                        continue
                    self.wfile.write ("<br>" + str(i-1) + ": " + s)
                    i+=1

            elif (cmd[1] == 'clear'):
                ctrl.fastWipe (Color(0,0,0))
                ctrl.show ()
                self.status (200, "Clearing")

            elif cmd[1] == 'fill':
                c = None
                if opts == 1:
                    c = parseColor (cmd[2])

                if c != None:
                    ctrl.fastWipe (c)
                    ctrl.show ()
                    self.status (200, "OK")
                    return
                self.status (400, "Bad Request, use /fill/&lt;color&gt;")

            elif (cmd[1] == 'set'):
                c = None
                if opts == 2:
                    c = parseColor (cmd[3])

                if c != None:
                    ctrl.setColor (int(cmd[2]), c)
                    ctrl.show ()
                    self.status (200)
                    return

                self.status (400, "Bad Request, use set/&lt;id&gt;/&lt;color&gt;")

            elif cmd[1] == 'chars':
                if opts != 1 or len (cmd[2]) > 128:
                    self.status (400, "Too many chars")
                    return

                s = urllib.unquote(cmd[2]).decode('utf8')
                
                for i in range (len(s)):
                    ctrl.fastWipe (Color(0,0,0))
                    ctrl.char (s[i])
                    ctrl.show ()
                    time.sleep(0.5)

                self.status (200)


            elif (cmd[1] == 'char'):
                if opts == 1 and len(cmd[2]) == 1:
                    ctrl.fastWipe (Color(0,0,0))
                    ctrl.char (cmd[2])
                    ctrl.show ()
                    self.status (200, "Syntax OK, but command not supported, yet.")
                    return
                
                self.status (400, "Bad Request, use char/&lt;char&gt;")

            if (not self.responded):
                self.status (404, "Not found!");
            return
        except Exception as e:
            if not self.responded:
                self.status (500)

            exType, ex, tb = sys.exc_info ()
            self.wfile.write ("<hr><h1>Exception</h1>"+str(e)+"<pre>")
            traceback.print_exception (exType, ex, tb, 64, self.wfile)
            self.wfile.write ("</pre>")
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

