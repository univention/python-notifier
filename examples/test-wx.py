#!/usr/bin/env python

from wxPython.wx import *

class MyPanel( wxPanel ):
    def __init__( self, parent, ID ):
	self.parent = parent
	wxPanel.__init__( self, parent, ID )
	self.box = wxBoxSizer( wxVERTICAL )
	self.button_close = wxButton( self, 1, "Close" ) 
	EVT_BUTTON( self, 1, self.OnQuit )
	self.box.Add( self.button_send )
	self.box.Add( self.button_close )
	self.SetAutoLayout( true )
	self.SetSizer( self.box )
	self.box.Fit( self )

    def OnQuit( self, event ):
	self.parent.Close()

class MyFrame( wxFrame ):
    def __init__( self, parent ):
	wxFrame.__init__( self, parent, -1, "MyFrame" )
	self.box = wxBoxSizer( wxVERTICAL )
	self.panel = MyPanel( self, -1 )
	self.box.Add( self.panel )
	self.SetSizer( self.box )
	self.SetAutoLayout( true )
	self.box.Fit( self )

if __name__ == '__main__':
    frame = MyFrame( None )
    frame.Show( true )
    
    notifier.loop()
