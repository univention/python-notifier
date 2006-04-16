#!/usr/bin/env python

import sys

import gtk

import notifier

notifier.init( notifier.GTK )

def hello( *args ):
    print 'Hello World'

def destroy(*args):
    window.hide()
    sys.exit( 0 )

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
    return True

notifier.timer_add( 4000, notifier.Callback( timer_test ) )

notifier.loop()


