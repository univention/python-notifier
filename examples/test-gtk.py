#!/usr/bin/env python

import gtk

import notifier

notifier.init( notifier.GTK )

def hello( *args ):
    print 'Hello World'

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
    return True

notifier.addTimer( 4000, notifier.Callback( timer_test ) )

notifier.loop()


