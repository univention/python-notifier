#!/usr/bin/env python

from wxPython.wx import *
from mbus import mbusif
from mbus import mbustypes


class MyPanel( wxPanel ):
    def __init__( self, parent, ID ):
	self.parent = parent
	wxPanel.__init__( self, parent, ID )
	self.box = wxBoxSizer( wxVERTICAL )
	self.button_close = wxButton( self, 1, "Close" ) 
	EVT_BUTTON( self, 1, self.OnQuit )
	self.button_send = wxButton( self, 2, "Send" )
	EVT_BUTTON( self, 2, self.OnSend )
	self.box.Add( self.button_send )
	self.box.Add( self.button_close )
	self.SetAutoLayout( true )
	self.SetSizer( self.box )
	self.box.Fit( self )
    def OnQuit( self, event ):
	self.parent.Close()
    def OnSend( self, event ):
	mbus.send( "", "button_pressed", [] )

class MyFrame( wxFrame ):
    def __init__( self, parent ):
	wxFrame.__init__( self, parent, -1, "MyFrame" )
	self.box = wxBoxSizer( wxVERTICAL )
	self.panel = MyPanel( self, -1 )
	self.box.Add( self.panel )
	self.SetSizer( self.box )
	self.SetAutoLayout( true )
	self.box.Fit( self )

def newEntity( maddr ):
    print "New Entity:",
    for key in maddr.keys():
	print "%s:%s"%( key, maddr[key] ),
    print

def lostEntity( maddr ):
    print "Lost Entity:",
    for key in maddr.keys():
	print "%s:%s"%( key, maddr[key] ),
    print

def unknown( mmessage ):
    print "received unknown message:"
    print mmessage.asString()

def transporterror( e ):
    print "Mbus transport error occured:", e.descr
    print "MMessage content:"
    if e.mmsg:
	try: print e.mmsg.header.srcAdr, e.mmsg.header.destAdr
	except: pass

def simple_send( data = None ):
    # mbus.send( address, commandname, arguments
    mbus.send( "", "simple_send", [ -3.14 ] )
    return 1 # unregister timer callback

def recv_print( mmsg, data = None ):
    print "received print command, args =", mmsg.payload[0]
    return 1 # keep command registered

if __name__ == '__main__':
    mbus = mbusif.MbusIF( "app:wxTest lang:python" )
    mbus.newEntityFunction      = newEntity
    mbus.lostEntityFunction     = lostEntity
    mbus.unknownMessageFunction = unknown
    mbus.errorFunction          = transporterror
    mbus.addTimer( 3, simple_send )
    mbus.addCallback( "print", recv_print )
    frame = MyFrame(None)
    frame.Show(true)
    mbus.loop()
