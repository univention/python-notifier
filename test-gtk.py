#!/usr/bin/env python

# this is a translation of "Hello World III" from the GTK manual,
# using gtk.py
# ...combined with the litte pyMbus example
# example taken from pygtk-distro

from gtk import *
from mbus import mbusif
from mbus import mbustypes

def hello(*args):
    print " Sending: Hello World"
    mbus.send( "", "hellow", [ "world" ] )

def destroy(*args):
    window.hide()
    mainquit()

window = GtkWindow(WINDOW_TOPLEVEL)
window.connect("destroy", destroy)
window.set_border_width(10)

button = GtkButton("Hello World")
button.connect("clicked", hello)
window.add(button)
button.show()

window.show()

# notifier-timer testfunction
def timer_test( data ):
    print "timer_test"
    m = mbustypes.MMessage( "" ) # empty address means send to ALL entities
    m.payload.append( mbustypes.MCommand( "mbus.python" ) )
    m.payload[-1].args = [ 'python', 'rules', [ 1, 2, [ 1, 2, 3, 4] ], \
		    mbustypes.MSymbol( "somewhat" ) ]
    mbus.send( m )
    return 1 # return true for endless looping,
	     # nothing or false to be removed from scheduler

def recv_print( mmsg, data = None ):
    print "received print command, args =", mmsg.payload[0]
    return 1 # keep command registered

mbus = mbusif.MbusIF( "app:test lang:python" )
mbus.addCallback( "print", recv_print )
mbus.addTimer( 4, timer_test )

mainloop()


