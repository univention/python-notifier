#!/usr/bin/env python

# this is a translation of "Hello World III" from the GTK manual,
# using gtk.py
# ...combined with the litte pyMbus example
# example taken from pygtk-distro

import gtk
from mbus import mbusif
from mbus import mbustypes

import notifier

notifier.init( notifier.GTK )

def hello(*args):
    print " Sending: Hello World"
    mbus.send( "", "hellow", [ "world" ] )

def destroy(*args):
    window.hide()
    gtk.mainquit()

window = gtk.Window( gtk.WINDOW_TOPLEVEL )
window.connect( 'destroy', destroy )
window.set_border_width( 10 )

button = gtk.Button( 'Hello World' )
button.connect( 'clicked', hello )
window.add( button )
button.show()

window.show()

# notifier-timer testfunction
def timer_test():
    print "timer_test"
    m = mbustypes.MMessage( "" ) # empty address means send to ALL entities
    m.payload.append( mbustypes.MCommand( "mbus.python" ) )
    m.payload[-1].args = [ 'python', 'rules', [ 1, 2, [ 1, 2, 3, 4] ], \
		    mbustypes.MSymbol( "somewhat" ) ]
    mbus.send( m )
    return True

def recv_print( mmsg, data = None ):
    print "received print command, args =", mmsg.payload[ 0 ]
    return True # keep command registered

mbus = mbusif.MbusIF( "app:test lang:python" )
mbus.addCallback( "print", notifier.Callback( recv_print ) )
mbus.addTimer( 4000, notifier.Callback( timer_test ) )

notifier.loop()


