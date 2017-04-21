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
__version__ = '0.3.1' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import os


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
        
        # boolean to keep track of command updating
        self.no_commands = True
        
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
        
        # Reset flag after initial updating
        self.no_commands = True
       
        # list of errors thrown during the importing of the XML file
        self.error_log = []        
    # end def
    
    def update_size(self, target, new_size):
        """ 
        Update the length of the data in a name request
        
        @param[in]  target:    The property that is to be updated, one of:
                               'checksum_size', 'name_size', 'wflag_size', 
                               'ascii_size', 'time_size'  or 'length_size' 
                               (string).
        @param[in]  new_size:  The new size for that property (string).
        """     
        # check the validity of the new size
        if new_size.isdigit():
            # it is an integer so that is good
            if int(new_size) >= 0:
                # it is also positive so determine which property is to 
                # be updated then perform that update
                if target == 'checksum_size':
                    self.chksum_size = int(new_size)
                    
                elif target == 'name_size':
                    self.name_size = int(new_size)
                    
                elif target == 'wflag_size':
                    self.wflag_size = int(new_size)  
                    
                elif target == 'ascii_size':
                    self.ascii_size = int(new_size)  
                    
                elif target == 'time_size':
                    self.time_size = int(new_size)    
                    
                elif target == 'length_size':
                    self.length_size = int(new_size)   
                
                else:
                    # this is not a valid property to update
                    self.error_log.append('*** ' + str(target) + 'found '\
                                          ' in xml file is not a valid '\
                                          'default to update ***')
                # end if
            
            else:
                self.error_log.append('*** Invalid ' + str(target) +
                                      ' in xml file ***')   
            # end if
            
        else:
            self.error_log.append('*** Invalid ' + srt(target) + 
                                  ' in xml file ***')
        # end if  
    # end def        
        
              
    def add_command(self, command, length, format_string):
        """ 
        Add an item to the SCPI command dictionary
        
        @param[in]  command:       The new command string (string).
        @param[in]  length:        The length of the data field (string).
        @param[in]  format_string: The format of the data returned
        """ 
        
        # see if no new commands have been added
        if self.no_commands:
            
            # empty the dictionary
            self.SCPI_Data = {}        
            
            # set the updated flag
            self.no_commands = False
        # end if
        
        # check if the command is valid
        if length.isdigit() and is_valid_format(format_string):
            if int(length) > 0:
                # the command is valid so proceed
                
                # define list of keys to use
                keys = [command + ',name', command + ',data',
                        command + ',length', command + ',ascii']
                
                # define list of bbyte lengths to use
                key_bytes = [# name length
                             self.wflag_size + self.time_size + \
                             self.name_size + self.chksum_size,
                             # data length
                             self.wflag_size + self.time_size + \
                             self.chksum_size + int(length),
                             # length length
                             self.wflag_size + self.time_size + \
                             self.length_size + self.chksum_size,
                             # ascii length
                             self.wflag_size + self.time_size + \
                             self.chksum_size + self.ascii_size]
                
                # define list of formats
                formats = ['ascii', format_string, 'uint', 'ascii']
                
                # construct the four scpi commands for each command
                for i in range(0,4):
                    
                    # check if the command already exists in the library
                    if keys[i] not in self.SCPI_Data:
                        # it doesnt so add it
                        self.SCPI_Data[keys[i]] = [key_bytes[i], 
                                                   formats[i]]
                        
                    else:
                        self.error_log.append('*** ' + key[i] + 
                                              ' already in library ***')    
                    # end if                                              
                # end for
                             
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
        # add the error to the list
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
        
        # iterate through the devices
        for key in dev_keys:
            if (key not in devices) and (key != 'SUP'):
                # this is a unique device, add it to the list
                devices = devices + [key]
            # end if
        # end for
        
        devices = devices + ['SIM']
        
        # replace the GPS if present with its longer name
        devices = ['GPSRM' if device == 'GPS' else device 
                   for device in devices]
        return devices
    # end def     
# end class   


class write_directives:
    """ 
    Class to contain all of the information required by the 
    writing functions.
    """  
    def __init__(self, commands, address, delay, ascii, logging_p = 0):
        """
        Combine the passed vlaues into an object.
        
        @param[in]     commands:    The list of commands to send.
        @param[in]     address:     The address to send to.
        @param[in]     delay:       The intermessage delay to use.
        @param[in]     ascii:       The ascii delay to use.
        @param[in]     logging_p:   OPTIONAL, the logging period to use.
        """        
        self.command_list = commands
        self.addr = address
        self.delay_time = delay
        self.ascii_time = ascii
        self.logging_p = logging_p
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
    # define default status
    file_free = True
    
    # check if the file already exists
    if os.path.isfile(filename):
        # it does so try and rename it to see if it is in use
        try:
            os.rename(filename,filename)
            
        except OSError as e:
            # renaming was not possible as another program is using it.
            file_free = False
        # end try
    # end if
    
    return file_free
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
    # if it can be converted to a base 16 int then it is hex
    try:
        int(s, 16)
        return True
    
    except ValueError:
        # it could not be converted therefore is not hex
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
    if command.startswith('<READ') and command.endswith('>') and \
       is_vaild_raw(command):
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
    # default state
    valid = True
    
    # split the command into sections
    data_list = command[:-1].split(' ')
    
    # check the command's validity
    if (len(data_list) < 3) or ((data_list[0] != '<READ') and \
                                (data_list[0] != '<WRITE')):
        # if the command is too long and doesn't start corectly then it is 
        # invalid        
        valid = False
        
    elif (len(data_list[1]) != 5) or not data_list[1].startswith('0x'):
        # if the address field is not the right length and doesnt start 
        # wit the hexidecimal identifier then it is invalid
        valid = False
        
    elif (data_list[1][4] != ',') or not is_hex(data_list[1][2:-1]):
        # if the address doean't end with a comma or the number portion is 
        # not a hexideciaml number then it is invalid
        valid = False
        
    elif ('WRITE' in data_list[0]) and \
         any([not is_hex(item) for item in data_list[2:]]):
        # if it is a write command and any item in the data list is not
        # hexidecimal then it is invalid
        valid = False
        
    elif ('READ' in data_list[0]) and \
         (len(data_list) != 3 or not data_list[2].isdigit()):
        # if it is a read command and there in not a single decimal length
        # specified then the command is invalid
        valid = False     
    
    # end if
    
    # print errors associated with commands if required
    if ('READ' in command) and not valid:
        print '*** Invalid READ command, please refer to the'\
                      'Read me for proper syntax ***'          
        
    elif ('WRITE' in command) and not valid:
        print '*** Invalid WRITE command, please refer to the'\
                      'Read me for proper syntax ***'           
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
    # default
    is_valid = True
    
    # list of valid formats
    valid_formats = ['hex', 'char', 'uint', 'int', 'double', 
                     'ascii', 'long', 'long long', 'float']
    
    # list of formats provided (may be a single format)
    format_list = format_string.split(', ')
    
    # check each item in the provided list
    for item in format_list:
        
        # if it does not match a valid format then it is invalid
        if item not in valid_formats:
            is_valid = False
        # end if
    # end for
    
    return is_valid
# end def

