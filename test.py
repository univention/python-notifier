#!/usr/bin/env python

import notifier

fasel = None

def bla():
  print 'hallo'
  
def timeout( data = None ):
    print 'timeout', data

fasel = bla

print fasel()

notifier.init()

print 'addTimer', notifier.addTimer

notifier.addTimer( 2, timeout )

notifier.loop()
