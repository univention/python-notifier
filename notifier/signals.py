#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# signals.py
#
# Author: Andreas Büsching  <crunchy@bitkipper.net>
#
# signals
#
# $Id: file.py,v 1.1 2004/09/20 12:39:43 crunchy Exp $
#
# Copyright (C) 2005 Andreas Büsching <crunchy@bitkipper.net>
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

__signals = {}

class Signal( object ):
    def __init__( self, name ):
        self.name = name
        self.__callbacks = []

    def emit( self, *args ):
        for cb in self.__callbacks:
            if args: cb( *args )
            else: cb()

    def connect( self, callback ):
        self.__callbacks.append( callback )

    def disconnect( self, callback ):
        try: self.__callbacks.remove( callback )
        except: pass

    def __str__( self ):
        return self.name

class Provider( object ):
    def __init__( self ):
        self.__signals = {}

    def signal_new( self, signal ):
        new( signal, self.__signals )

    def signal_connect( self, signal, callback ):
        connect( signal, callback, self.__signals )

    def signal_disconnect( self, signal, callback ):
        disconnect( signal, callback, self.__signals )

    def signal_emit( self, signal, *args ):
        if isinstance( signal, Signal ) and \
               self.__signals.has_key( signal.name ):
            self.__signals[ signal.name ].emit( *args )
        elif isinstance( signal, str ) and self.__signals.has_key( signal ):
            self.__signals[ signal ].emit( *args )

def _select_signals( signals ):
    global __signals
    if signals == None: return __signals
    else: return signals

def new( signal, signals = None ):
    _signals = _select_signals( signals )
    if isinstance( signal, str ):
        signal = Signal( signal )

    if _signals.has_key( signal.name ):
        print "Signal already exists"
    else:
        _signals[ signal.name ] = signal

def connect( signal, callback, signals = None ):
    _signals = _select_signals( signals )
    if isinstance( signal, Signal ) and _signals.has_key( signal.name ):
        _signals[ signal.name ].connect( callback )
    elif isinstance( signal, str ) and _signals.has_key( signal ):
        _signals[ signal ].connect( callback )

def disconnect( signal, callback, signals = None ):
    _signals = _select_signals( signals )
    if isinstance( signal, Signal ) and _signals.has_key( signal.name ):
        _signals[ signal.name ].disconnect( callback )
    elif isinstance( signal, str ) and _signals.has_key( signal ):
        _signals[ signal ].disconnect( callback )

def emit( signal, *args ):
    if isinstance( signal, Signal ) and __signals.has_key( signal.name ):
        __signals[ signal.name ].emit( *args )
    elif isinstance( signal, str ) and __signals.has_key( signal ):
        __signals[ signal ].emit( *args )
