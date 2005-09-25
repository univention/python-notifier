#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# nf_wx.py
# 
# Author: Andreas Büsching <crunchy@bitkipper.net>
# 
# wxWindows notifier wrapper
# 
# $Id$
# 
# Copyright (C) 2004, 2005 Andreas Büsching <crunchy@bitkipper.net>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

"""wxWindows notifier wrapper"""

from select import select
import time
from wxPython.wx import *
import thread

IO_READ = 1
IO_WRITE = 2
IO_EXCEPT = 4

#------------------------------------------------------------------------------
# Event to communicate with gui-thread (main-thread)

wxEVT_UDPSOCKETEVENT = wxNewEventType()

def EVT_UDPSOCKETEVENT( handler, func ):
    """Bind UDP-Socket events to a callback function"""
    handler.Connect( -1, -1, wxEVT_UDPSOCKETEVENT, func )

## What can we do with the id?
#def EVT_UDPSOCKETEVENT( handler, id, func ):
#    handler.Connect( id, -1, wxEVT_UDPSOCKETEVENT, func )

class UDPSocketEvent( wxPyEvent ):
    """UDP-Socket events. Send from select-thread to gui-thread"""
    def __init__( self, socket ):
	wxPyEvent.__init__( self )
	self.SetEventType( wxEVT_UDPSOCKETEVENT )
	self.socket = socket
	self.msg, self.sender = socket.recvfrom( 256000 )
    def recvfrom( self, size ):
	"""this function is to fake a real socket"""
	if size >= len( self.msg ):
	    res = self.msg
	    self.msg = []
	else:
	    res = self.msg[:size]
	    self.msg = self.msg[size:]
	return ( res, self.sender )

#wxEVT_MBUSTIMEREVENT = wxNewEventType()
#
#def EVT_MBUSTIMEREVENT( handler, func ):
#    handler.Connect( -1, -1, wxEVT_MBUSTIMEREVENT, func )
#
#
#class MbusTimerEvent( wxPyEvent ):
#    def __init__( self, data = None ):
#	wxPyEvent.__init__( self )
#	self.SetEventType( wxEVT_MBUSTIMEREVENT )
#	self.data = data

#------------------------------------------------------------------------------

ID_Timer = wxNewId()

class Notifier( wxEvtHandler ):
    def __init__( self ):
        wxEvtHandler.__init__( self )
        self.sockets = {}
        self.timers = []
        # max seconds till new socket gets "selected"
        # decrease this value if you want to add/remove
        # sockets often
        self.timeout = 5 
        thread.start_new_thread( self.otherThreadLoop, () )
        self.app = wxPySimpleApp()
        EVT_UDPSOCKETEVENT( self, self.OnSocket )
        self.timer = wxTimer( self, ID_Timer )
        EVT_TIMER( self, ID_Timer, self.OnTimer )

    def addSocket( self, socket, method ):
        """The first argument specifies a socket, the second argument
        has to be a function that is called whenever there is data
        ready in the socket.  The callback function gets the socket
        back as only argument."""
        self.sockets[socket] = method

    def removeSocket( self, socket ):
        """Remove given socket from scheduler"""
        del self.sockets[socket]
        
    def addTimer( self, interval, method, data = None ):
        """The first argument specifies an interval in seconds, the
        second argument a function. This is function is called after
        interval seconds. If it returns true it's called again after
        interval seconds, otherwise it is removed from the
        scheduler. The third (optional) argument is a parameter given
        to the called function."""
        
        t = time.time()
        self.timers.append( (interval, t, method, data) )
        if len( self.timers ) == 1:
            self.timer.Start( (self.timers[0][0]+self.timers[0][1]-t) )

    def removeTimer( self, method ):
        """Removes _all_ functioncalls to the method given as argument
        from the scheduler."""
        remove = []
        for i in range( 0, len( self.timers ) ):
            if self.timers[ i ][ 2 ] == method:
                remove.append( i )
        remove.reverse()
        for i in remove: del self.timers[ i ]

    def otherThreadLoop( self ):        
        """socketloop sits in its own thread and sends events to the
        main thread"""
        while 1:
            if len( self.sockets.keys() ) != 0:
                r,w,e = select( self.sockets.keys(), [], [], self.timeout )
                for sock in r:
                    evt = UDPSocketEvent( sock )
                    wxPostEvent( self, evt )
            else: time.sleep( self.timeout )

    def OnSocket( self, evt ):
        """this is where the udp-events are send to"""
        self.sockets[evt.socket]( evt )

    def OnTimer( self, evt ):
        """gets called by wx-mainloop, mbus-timers are handled here"""
        remove = []
        mindelta = 86400 * 1000 # one day
        now = time.time() * 1000
        for i in range(0,len(self.timers)):
            delta = self.timers[i][1] + self.timers[i][0] - now
            if delta < 0:
                try:
                    if not self.timers[i][2]( self.timers[i][3] ):
                        remove.append( i )
                    else: self.timers[i] = ( self.timers[i][0], now, \
                            self.timers[i][2], self.timers[i][3] )
                except:
                    remove.append( i )
                delta = self.timers[i][0]
            if mindelta > delta: mindelta = delta
        remove.reverse()
        for r in remove: del self.timers[r]
        if mindelta == 86400: self.timer.Stop()
        else: self.timer.Start( mindelta )

    def loop( self ):
        """Execute main loop forver."""
        self.app.MainLoop()

    def step( self ):
        raise Error, "stepping not supported in wx-Mode"

# standard Notifier-Interface used by pyMbus 0.5.4 and above:

notifier_instance = Notifier()

addSocket	=  notifier_instance.addSocket
removeSocket	=  notifier_instance.removeSocket
addTimer	=  notifier_instance.addTimer
removeTimer	=  notifier_instance.removeTimer
step		=  notifier_instance.step
loop		=  notifier_instance.loop

addDispatcher = None
removeDispatcher = None
