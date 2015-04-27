# rpi\_ws281x\_httpd
This python httpd aims to export the rpi\_ws281x library over http. The long-term goal to to offer a minimalistic, C-style language, which is to be compiled to bytecode and than interpreted in a VM.

# Use case
LED notifications in my shared office using a simple HTTP API.

# State
This commit pushes only a small proof of concept. You can clear all LEDs, set all LEDs to a specific color, and set single LEDs to a given color. No fancy animations or the like - this needs some sort of threading.

# Usage
Set correct values in controller.py - AND PLEASE NOTE: my setup inverts, most others don't!!
Run 'sudo python server.py' [lib seems to require root] on your rpi.
Open a browser to http://raspberrypi:8080/set/1/255/0/0 to set LED number 1 to red (RGB 255,0,0).

# TODO
Everything. Right now this is just a quick hack since I usually don't do python. But I believe a full blown C++ multi thread webserver plus compiler plus VM is a bit of an overkill for what I want to do here (I would love to try the gatling library some day, though... ;-)
Before you ask "wow, a compiler and a VM? you're kidding, why don't you just...?": I feel like I want to build this that way for fun. With a minimalistic, reduced ANSI-C style language. That shouldn't be too difficult. Also, I know what I am doing and want some practice with python.

# Contribution
Well, feel free. But for sake of your sanity: Wait until I have some more logic implemented than just sticking two examples together.

# Requirements
You need an installed rpi\_ws281x, see https://github.com/jgarff/rpi_ws281x
