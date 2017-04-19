#!/usr/bin/env python
###########################################################################
#(C) Copyright Pumpkin, Inc. All Rights Reserved.
#
#This file may be distributed under the terms of the License
#Agreement provided with this software.
#
#THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,
#INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE.
###########################################################################
"""
@package pySCPI_threading.py
Module to handle the multi-threading aspects of pySCPI
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.0' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import pySCPI_aardvark
import threading
from functools import partial
import time


# ----------------
# Classes

class terminator_event:
    """ 
    Class to control the termination of threads
    """
    def __init__(self):
        self.kill_event = threading.Event()
        self.root_destroyed = False
    # end def


    def kill_log(self):
        """
        Kill all threads, intended for use with the logging thread.
        """      
        self.kill_event.set()
    # end def


    def kill_threads(self, gui):
        """
        Kill all threads and close the program.
        """      
        self.kill_event.set()
        self.root_destroyed = True
        gui.root.destroy()
    # end def
# end def


# ----------------
# Public Functions

def I2C_thread(command_list, addr_num, delay_time, 
               ascii_time, gui):
    """
    Wrapper for the I2C writing thread to control the startup and 
    shut down of the thread.
    
    @param[in]  command_list: List of commands to be sent 
                              (list of strings).
    @param[in]  addr_num:     I2C address of the slave device (int).
    @param[in]  delay_time:   Millisecond delay to wait between 
                              transmissions (int).
    @param[in]  ascii_time:   Millisecond delay to wait before reading an 
                              'ascii' request (int).
    @param[in]  gui:          Instance of the gui that this thread is 
                              started by (pySCPI_gui.main_gui).
    """      
    # write via the Aardvark
    pySCPI_aardvark.write_aardvark(command_list, addr_num, delay_time, 
                                   ascii_time, gui)
    # clear the thread termination flag
    gui.terminator.kill_event.clear()
    
    if not gui.terminator.root_destroyed:
        # unlock all of the GUI buttons
        gui.action_lock('Unlock')
    # end if
# end def


def I2C_log_thread(command_list, addr_num, delay_time, 
                   ascii_time, logging_p, filename, gui):
    """
    Wrapper for the logging thread to control the startup and shut down of 
    the thread.
    
    @param[in]  command_list: List of commands to be sent 
                              (list of strings).
    @param[in]  addr_num:     I2C address of the slave device (int).
    @param[in]  delay_time:   Millisecond delay to wait between 
                              transmissions (int).
    @param[in]  ascii_time:   Millisecond delay to wait before reading 
                              an 'ascii' request (int).
    @param[in]  logging_p:    Period of the logging task in seconds (int)
    @param[in]  filename:     absolute directory of the file to log to 
                              (string).
    @param[in]  gui:          Instance of the gui that this thread is 
                              started by (pySCPI_gui.main_gui).
    """      
    # Change the role of the logging button so that it stops logging
    gui.logging_button.config(state = 'normal', text = 'Stop Logging', 
                              command = gui.terminator.kill_log)
    # start logging
    pySCPI_aardvark.log_aardvark(command_list, addr_num, delay_time, 
                                 ascii_time, logging_p, filename, gui)
    # clear the flag that stopped logging
    gui.terminator.kill_event.clear()
    
    if not gui.terminator.root_destroyed:
        # unlock all GUI buttons
        gui.action_lock('Unlock')
        # Reset the logging button back to it's initial state
        gui.logging_button.config(text = 'Start Logging', 
                                  command = partial(pySCPI_aardvark.start_logging, gui))
    # end if
# end def

