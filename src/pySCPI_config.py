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
@package pySCPI_config.py
Module to handle the configureation of pySCPI including setting default 
values and declaring the dictionaries of address and commands.
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.0' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import os

# ---------
# Constants


# ---------
# Classes
class command_library:
    """
    Class containing the information that defines all the supported 
    SCPI commands
    """
    
    def __init__(self):
        """
        Initialise the library with default values
        """
        
        # The length of a name request in bytes
        self.name_size = 32
        
        # The length of the checksum in bytes
        self.chksum_size = 0
        
        # The length of the write flag element in bytes
        self.wflag_size = 1
        
        # The length of the timestamp in bytes
        self.time_size = 4
        
        # The length of a length request in bytes
        self.length_size = 2
        
        # The leght of an ascii request in bytes
        self.ascii_size = 128
        
        # Default command list
        self.SCPI_Data = {}
        self.add_command('SUP:TEL? 0', '48', 'ascii')
        self.add_command('SUP:TEL? 1', '8',  'long long')
        self.add_command('SUP:TEL? 2', '8',  'long long')
        self.add_command('SUP:TEL? 3', '2',  'uint')
        self.add_command('SUP:TEL? 4', '22', 'long, long, int, int, int')
        self.add_command('SUP:TEL? 5', '8',  'long long')
        self.add_command('SUP:TEL? 6', '8',  'long long')
        self.add_command('SUP:TEL? 7', '8',  'long long')
        self.add_command('SUP:TEL? 8', '8',  'double')
            
       
        # list of errors thrown during the importing of the XML file
        self.error_log = []        
    # end def
    
    
    def update_name_size(self, new_size):
        """ 
        Update the length of the data in a name request
        
        @param[in]  new_size:  The new name length (string).
        """ 
        if new_size.isdigit():
            if int(new_size) > 0:
                self.name_size = int(new_size)
            else:
                self.error_log.append('*** Invalid name_size '
                                      'in xml file ***')   
            # end if
        else:
            self.error_log.append('*** Invalid name_size '
                                  'in xml file ***')
        # end if  
    # end def 
    
    
    def update_checksum_size(self, new_size):
        """ 
        Update the length of the checksum in SCPI telemetry
        
        @param[in]  new_size:  The new checksum length (string).
        """ 
        if new_size.isdigit():
            if int(new_size) >= 0:
                self.chksum_size = int(new_size)
            else:
                self.error_log.append('*** Invalid checksum size '
                                      'in xml file ***')                    
        else:
            self.error_log.append('*** Invalid checksum size '
                                  'in xml file ***')
        # end if  
    # end def   
    
    
    def update_writeflag_size(self, new_size):
        """ 
        Update the length of the writeflag in SCPI telemetry
        
        @param[in]  new_size:  The new writeflag length (string).
        """ 
        if new_size.isdigit():
            if int(new_size) >= 0:
                self.wflag_size = int(new_size)
            else:
                self.error_log.append('*** Invalid write flag size '
                                      'in xml file ***')                    
        else:
            self.error_log.append('*** Invalid write flag size '
                                  'in xml file ***')
        # end if  
    # end def 
    
    
    def update_timestamp_size(self, new_size):
        """ 
        Update the length of the timestamp in SCPI telemetry
        
        @param[in]  new_size:  The new timestamp length (string).
        """ 
        if new_size.isdigit():
            if int(new_size) >= 0:
                self.time_size = int(new_size)
            else:
                self.error_log.append('*** Invalid timestamp size '
                                      'in xml file ***')                    
        else:
            self.error_log.append('*** Invalid timestamp size '
                                  'in xml file ***')
        # end if  
    # end def  
    
    
    def update_length_size(self, new_size):
        """ 
        Update the length of a length request in SCPI telemetry
        
        @param[in]  new_size:  The new length request length (string).
        """ 
        if new_size.isdigit():
            if int(new_size) >= 0:
                self.length_size = int(new_size)
            else:
                self.error_log.append('*** Invalid length size '
                                      'in xml file ***')                    
        else:
            self.error_log.append('*** Invalid length size '
                                  'in xml file ***')
        # end if  
    # end def   
    
    
    def update_ascii_size(self, new_size):
        """ 
        Update the length of an ascii request in SCPI telemetry
        
        @param[in]  new_size:  The new ascii request length (string).
        """ 
        if new_size.isdigit():
            if int(new_size) >= 0:
                self.ascii_size = int(new_size)
            else:
                self.error_log.append('*** Invalid ascii size '
                                      'in xml file ***')                    
        else:
            self.error_log.append('*** Invalid ascii size '
                                  'in xml file ***')
        # end if  
    # end def  
    
    
    def add_first_command(self, command, length, format_string):
        """ 
        Rebuild the dictionary of SCPI commands with the first item
        
        @param[in]  command:       The new command string (string).
        @param[in]  length:        The length of the data field (string).
        @param[in]  format_string: The format of the data returned
        """         
        self.SCPI_Data = {}
        self.add_command(command, length, format_string)
    # end def
                
                
    def add_command(self, command, length, format_string):
        """ 
        Add an item to the SCPI command dictionary
        
        @param[in]  command:       The new command string (string).
        @param[in]  length:        The length of the data field (string).
        @param[in]  format_string: The format of the data returned
        """ 
        
        if length.isdigit() and is_valid_format(format_string):
            if int(length) > 0:
                # Add the ,name command to the dictionary
                name_key = command + ',name'
                name_bytes = self.wflag_size + self.time_size + \
                    self.name_size + self.chksum_size                
                if name_key not in self.SCPI_Data:
                    self.SCPI_Data[name_key] = [name_bytes, 'ascii']
                else:
                    self.error_log.append('*** ' + name_key + 
                                          ' already in library ***')    
                # end if
                
                # Add the ,data command to the library
                data_key = command + ',data'
                data_bytes = self.wflag_size + self.time_size + \
                    self.chksum_size + int(length)
                if data_key not in self.SCPI_Data:
                    self.SCPI_Data[data_key] = [data_bytes, format_string]
                else:
                    self.error_log.append('*** ' + data_key + 
                                          ' already in library ***')    
                # end if   
                
                # Add the ,length command to the library
                length_key = command + ',length'
                length_bytes = self.wflag_size + self.time_size + \
                    self.length_size + self.chksum_size
                if length_key not in self.SCPI_Data:
                    self.SCPI_Data[length_key] = [length_bytes, 'uint']
                else:
                    self.error_log.append('*** ' + length_key + 
                                          ' already in library ***')    
                # end if   
                
                # Add the ,ascii command to the library
                ascii_key = command + ',ascii'
                ascii_bytes = self.wflag_size + self.time_size + \
                    self.chksum_size + self.ascii_size
                if ascii_key not in self.SCPI_Data:
                    self.SCPI_Data[ascii_key] = [ascii_bytes, 'ascii']
                else:
                    self.error_log.append('*** ' + ascii_key + 
                                          ' already in library ***')    
                # end if   
            else:
                self.error_log.append('*** ' + command + 
                                      ' length is too short ***')  
            # end if
        else:
            self.error_log.append('*** ' + command + 
                                  ' length or format is invalid ***')            
        # end if
    # end def
        
    
    def log_error(self, error):
        """ 
        Append an error to the class's error log
        
        @param[in]  error:  The error to log (string).
        """         
        self.error_log.append(error)
    # end def
    
    def get_devices(self):
        """
        Get a list of all the devices that pySCPI supports
        
        @return     devices:  A list of all the supported devices 
                              (list of strings).
        """    
        devices = []
        # get all the keys from the dictionary
        keys = self.SCPI_Data.keys()
        # extract the device specifier
        dev_keys = [key.split(':')[0] for key in keys]
        for key in dev_keys:
            if (key not in devices) and (key != 'SUP'):
                # this is a unique device, add it to the list
                devices = devices + [key]
            # end if
        # end for
        
        devices = devices + ['SIM']
        
        # replace the GPS if present with its longer name
        devices = ['GPSRM' if device == 'GPS' 
                   else device for device in devices]
        return devices
    # end def     
# end class    
 
                
#
# ----------------
# Public Functions 

def file_is_free(filename):
    """
    Determine if a file that is to be modified is being 
    used by another program.
    
    @param[in]  filename: The absolute directory of the file (string).
    @return     (bool)    True:     The file is not being used by 
                                    another program.
                          False:    The file is in use.
    """    
    try:
        # attempt to change the files name to see if it is available.
        os.rename(filename,filename)
        return True
    except OSError as e:
        # renaming was not possible as another program is using it.
        return False
    # end try
# end def


def has_preamble(command):
    """
    Determines if the command in question has a preamble.
    
    @param[in]  command:  The command of interest (string).
    @return     (bool)    True:  There is a preamble associated 
                                 with this command.
                          False: There is not.
    """    
    if command.endswith('ascii'): # or command.endswith('length')  
        # or command.endswith('name'):
        return False
    else:
        return True
    # end if
# end def


def get_devices():
    """
    Get a list of all the devices that pySCPI supports
    
    @return     devices:  A list of all the supported devices 
                          (list of strings).
    """    
    devices = []
    # get all the keys from the dictionary
    keys = SCPI_Data.keys()
    # extract the device specifier
    dev_keys = [key.split(':')[0] for key in keys]
    for key in dev_keys:
        if (key not in devices) and (key != 'SUP'):
            # this is a unique device, add it to the list
            devices = devices + [key]
        # end if
    # end for
    
    devices = devices + ['SIM']
    
    # replace the GPS if present with its longer name
    devices = ['GPSRM' if device == 'GPS' else 
               device for device in devices]
    return devices
# end def


def is_config(command):
    """
    Determine if the command in question is a configuration command
    
    @param[in]  command: The command string to be tested (string).
    @return     (bool)   True:    The command is a configuration command.
                         False:   The command is not a configuration 
                                  command.
    """    
    if command.startswith('<') and command.endswith('>') and \
       ('WRITE' not in command) and ('READ' not in command):
        return True
    else:
        return False
    # end if
# end def


def is_hex(s):
    """
    Determine if a string is a hexnumber
    
    @param[in]  s:       The string to be tested (string).
    @return     (bool)   True:    The string is a hex number.
                         False:   The command is not a hex number.
    """    
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
    # end try
# end def


def is_raw_write(command):
    """
    Determine if the command in question is a raw write command
    
    @param[in]  command: The command string to be tested (string).
    @return     (bool)   True:    The command is a raw write command.
                         False:   The command is not a raw write command.
    """    
    if command.startswith('<WRITE') and command.endswith('>'):
        return True
    else:
        return False
    # end if
# end def    


def is_raw_read(command):
    """
    Determine if the command in question is a raw read command
    
    @param[in]  command: The command string to be tested (string).
    @return     (bool)   True:    The command is a raw read command.
                         False:   The command is not a raw read command.
    """    
    if command.startswith('<READ')and command.endswith('>'):
        return True
    else:
        return False
    # end if
# end def 


def is_valid_raw(command):
    """
    Determine if the command in question is a raw read command
    s
    @param[in]  command: The command string to be tested (string).
    @return     (bool)   True:    The command is a raw read command.
                         False:   The command is not a raw read command.
    """    
    valid = True
    data_list = command[:-1].split(' ')
    
    if (len(data_list) < 3) or ((data_list[0] != '<READ') and \
                                (data_list[0] != '<WRITE')):
        valid = False
        
    elif (len(data_list[1]) != 5) or not data_list[1].startswith('0x'):
        valid = False
        
    elif (data_list[1][4] != ',') or not is_hex(data_list[1][2:-1]):
        valid = False
        
    elif ('WRITE' in data_list[0]) and \
         any([not is_hex(item) for item in data_list[2:]]):
        valid = False
        
    elif ('READ' in data_list[0]) and \
         (len(data_list) != 3 or not data_list[2].isdigit()):
        valid = False        
    # end if
    return valid   
# end def 


#
# ----------------
# Private Functions 
         
    
def is_valid_format(format_string):
    """ 
    Determine if an imported format string is valid
    
    @param[in]  format_string: The format of the data returned
    @return     (bool)         True:  The format string is valid
                               False: The format string is not valid
    """     
    is_valid = True
    valid_formats = ['hex', 'char', 'uint', 'int', 'double', 
                     'ascii', 'long', 'long long']
    format_list = format_string.split(', ')
    for item in format_list:
        if item not in valid_formats:
            is_valid = False
        # end if
    # end for
    return is_valid
# end def

