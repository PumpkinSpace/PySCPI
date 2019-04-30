#!/usr/bin/env python
################################################################################
#(C) Copyright Pumpkin, Inc. All Rights Reserved.
#
#This file may be distributed under the terms of the License
#Agreement provided with this software.
#
#THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,
#INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE.
################################################################################
"""
@package pySCPI_threading.py
Module to handle the multi-threading aspects of pySCPI
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.6' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import pySCPI_aardvark
import threading


# ----------------
# Classes

class terminator_event:
    """ 
    Class to control the termination of threads
    
    @attribute kill_event     (Event) The event that controls termination
    @attribute root_destroyed (bool)  True if the gui has been exited
    """
    def __init__(self):
        """
        Initialise the terminator event.
        """        
        # threading event to manage thread closure
        self.kill_event = threading.Event()
        
        # boolean to indicate if the gui itself has been closed
        self.root_destroyed = False
    # end def


    def kill_log(self):
        """
        Kill all threads, intended for use with the logging thread.
        """      
        # set the thread termination event
        self.kill_event.set()
    # end def


    def kill_threads(self, gui):
        """
        Kill all threads and close the program.
        """      
        # set the thread termination event
        self.kill_event.set()
        
        # indicate that the gui is being closed
        self.root_destroyed = True
        
        # close the gui
        gui.root.destroy()
    # end def
# end class


# ----------------
# Public Functions

def I2C_thread(write_directives, gui):
    """
    Wrapper for the I2C writing thread to control the startup and 
    shut down of the thread.
    
    @param[in]  write_directives: Instructions to direct the sending of 
                                  data (pySCPI_config.write_directives)
    @param[in]  gui:              Instance of the gui that this thread is 
                                  started by (pySCPI_gui.main_gui).
    """      
    # Change the role of the button so that it stops commands
    gui.aardvark_button_state('stop')    
    
    # write via the Aardvark
    pySCPI_aardvark.write_aardvark(write_directives, gui)
    # clear the thread termination flag
    gui.terminator.kill_event.clear()
    
    # re-allow access to hte command text box
    gui.Command_text.config(state = 'normal')
    
    if not gui.terminator.root_destroyed:
        # unlock all of the GUI buttons
        gui.action_lock('Unlock')
        
        # Reset the button back to it's initial state
        gui.aardvark_button_state('start')        
    # end if
# end def


def I2C_log_thread(write_directives, filename, gui):
    """
    Wrapper for the logging thread to control the startup and shut down of 
    the thread.
    
    @param[in]  write_directives: Instructions to direct the sending of 
                                  data (pySCPI_config.write_directives)
    @param[in]  filename:         absolute directory of the file to log to 
                                  (string).
    @param[in]  gui:              Instance of the gui that this thread is 
                                  started by (pySCPI_gui.main_gui).
    """      
    # Change the role of the logging button so that it stops logging
    gui.logging_button_state('stop')
    
    # start logging
    pySCPI_aardvark.log_aardvark(write_directives, filename, gui)
    
    # clear the flag that stopped logging
    gui.terminator.kill_event.clear()
    
    # re-allow access to hte command text box
    gui.Command_text.config(state = 'normal')    
    
    # determine if there is still a gui to update
    if not gui.terminator.root_destroyed:
        # there is so unlock all GUI buttons
        gui.action_lock('Unlock')
        
        # Reset the logging button back to it's initial state
        gui.logging_button_state('start')
    # end if
# end def

