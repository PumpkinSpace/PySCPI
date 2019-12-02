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
@package pySCPI.pyw
Top level interface for the pySCPI program. to facilitate to control of 
SCPI capable module sproduced by Pumpkin Inc. This program utalizes the 
Aardvark device manufactured by Total Phase.
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.8' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import sys
sys.path.insert(1, 'src/')
import pySCPI_config  
import pySCPI_gui
import pySCPI_XML
import pySCPI_threading
sys.stderr = sys.stdout


#
# -------
# Main Code

# Initialise the command library
SCPI_library = pySCPI_config.command_library()

# Update the library from XML
pySCPI_XML.update_commands(SCPI_library)

# Initialise the defalut values for the GUI
GUI_defaults = pySCPI_gui.gui_defaults()

# update them from XML
pySCPI_XML.update_gui_defaults(GUI_defaults)

# define termination event manager
terminator = pySCPI_threading.terminator_event()

# construct the GUI
GUI = pySCPI_gui.main_gui(GUI_defaults, __version__, terminator, 
                          SCPI_library)

# start the GUI
GUI.start(GUI_defaults, SCPI_library)