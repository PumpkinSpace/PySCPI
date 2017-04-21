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
@package pySCPI_aardvark.py
Module to handle the aardvark aspects of pySCPI
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.1' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import sys
import aardvark_py
import pySCPI_formatting
import tkFileDialog as TKFD
import time
import pySCPI_config
import pySCPI_threading
import pySCPI_formatting
import os
import threading
from array import array
import csv


# ---------
# Constants

# I2C config
I2C = True
SPI = True
GPIO = False
Pullups = True
radix = 16
Bitrate = 100


#
# ----------------
# Public Functions

def Write_I2C(gui):
    """
    Function to command the I2C writing thread to start if all tests 
    are passed.
    
    @param[in]  gui:          Instance of the gui that this function is 
                              called by (pySCPI_gui.main_gui).
    """    
    # Lock all buttons
    gui.action_lock('Lock', None)
    # make the pressed button green
    gui.aardvark_button.config(background = 'green')
    
    # clear the output
    gui.output_clear()
    
    # get the desired delay from the gui.
    delay_time = gui.get_delay()
    
    
    # get the desired ascii delay from the gui.
    ascii_time = gui.get_ascii_delay()
    
    
    # get the desired I2C address from the gui.
    addr_num = gui.get_i2c_address()
    
    
    # get the list of commands from the gui
    command_list = gui.get_command_list()
    
    # construct the writing directives
    directives = pySCPI_config.write_directives(command_list, addr_num,
                                                delay_time, ascii_time)
    
    # define the thread to perform the writing
    write_thread = threading.Thread(target = pySCPI_threading.I2C_thread, 
                                    args=(directives, gui))
    # start the thread
    write_thread.start()
# end def


def start_logging(gui):
    """
    Function to command the loggingthread to start if all tests are passed.
    
    @param[in]  gui:          Instance of the gui that this function is 
                              called by (pySCPI_gui.main_gui).
    """    
    # lock all the GUI buttons
    gui.action_lock('Lock', None)
    # highlight the button that was pressed
    gui.logging_button.config(background = 'green')
    
    # clear output
    gui.output_clear()
    
    # get the desired delay from the gui.
    delay_time = gui.get_delay()
    
    
    # get the desired ascii delay from the gui.
    ascii_time = gui.get_ascii_delay()
    
    
    # get the desired I2C address from the gui.
    addr_num = gui.get_i2c_address()
    
    
    # get the list of commands from the gui
    command_list = gui.get_command_list()
    
    # determine the required/desired logging period for the program
    logging_time = gui.get_logging_period(command_list, delay_time, ascii_time)
    
    
    # define the options to use when promting for a file to save to
    file_opt = options = {}
    options['defaultextension'] = '.csv'
    options['filetypes'] = [('csv files', '.csv')]
    options['initialdir'] = os.getcwd() + '\\log_files'
    options['initialfile'] = 'example_log.csv'
    options['title'] = 'Save .csv log file as:'       
    
    # open a save file window
    filename_full = TKFD.asksaveasfilename(**file_opt) 
    
    # check the validity of the filename
    if (filename_full == ''):
        # No file was selected
        gui.output_clear()     
        print '*** No Logging filename selected ***'
        
        # unlock buttons
        gui.action_lock('Unlock')
        
    elif pySCPI_config.file_is_free(filename_full): 
        # the file is free so can be logged to
        
        # construct the writing directives
        directives = pySCPI_config.write_directives(command_list, addr_num,
                                                    delay_time, ascii_time,
                                                    logging_time)        
        
        # define the logging thread
        log_thread = threading.Thread(target = pySCPI_threading.I2C_log_thread, 
                                      args=(directives, filename_full, gui))
        # start the logging thread
        log_thread.start()
        
    else:
        # the file is in use by another program
        print'*** Requested log file is in use by another program ***'
        
        # unlock buttons
        gui.action_lock('Unlock')        
    # end if            
# end def


def update_aardvark(command, address, Aardvark_in_use):
    """
    Perform the configureation requested by a config command
    
    @param[in]  command:         The configuration command requested 
                                 (string).
    @param[in]  address:         The current I2C slave address in use 
                                 (int).
    @param[in]  AArdvark_in_use: The aardvark port in use 
                                 (aardvark_py.Aardvark).
    @return     (int)            The new I2C address to use 
                                 (potentially unchanged).
    """    
    new_address = address
    # determine the appropriate action to take
    if 'DELAY ' in command:
        delay_time = query_delay_command(command)
        aardvark_py.aa_sleep_ms(delay_time) 
    elif 'ADDRESS ' in command:
        # strip out the number
        address_list = command.split(' ')
        address_hex = address_list[1][0:-1]
        # verify that it is a number and that the beginning of the 
        # command was correct
        if address_hex.startswith('0x') and (len(address_hex) == 4) and \
           pySCPI_config.is_hex(address_hex[2:]) and \
           (address_list[0] == '<ADDRESS'):
            # is a good address
            new_address = int(address_hex,16)
            print 'Changed slave I2C address to ' + address_hex + '.'
        else:
            # the adderss is invlaid
            print '*** The requested ADDRESS command is not valid. '\
                  'Use <ADDRESS 0xYY>***'
        # end if        
    
    elif 'BITRATE ' in command:
        # strip out the number
        speed_list = command.split(' ')
        speed_num = speed_list[1][0:-1] 
        if speed_num.isdigit() and (speed_list[0] == '<BITRATE'):
            # is a good bitrate
            bitrate = aa_i2c_bitrate(Aardvark_in_use, int(speed_num))
            aardvark_py.aa_sleep_ms(200)             
            print 'Changed I2C bitrate to ' + str(bitrate) + 'kHz.'
        else:
            # the bitrate is invlaid
            print '*** The requested BITRATE command is not valid. '\
                  'Use <BITRATE x>***'
        # end if         
        
    elif 'PULLUPS ' in command:
        # check command
        if command == '<PULLUPS ON>':
            # turn pullups on
            aardvark_py.aa_i2c_pullup(Aardvark_in_use, 
                                      aardvark_py.AA_I2C_PULLUP_BOTH)
            aardvark_py.aa_sleep_ms(200)   
            print 'Turned I2C pullups on.'
        
        elif command == '<PULLUPS OFF>':
            # turn pullups off
            aardvark_py.aa_i2c_pullup(Aardvark_in_use, 
                                      aardvark_py.AA_I2C_PULLUP_NONE)
            aardvark_py.aa_sleep_ms(200)  
            print 'Turned I2C pullups off.'
        
        else:
            print '*** Invalid Pullup Command, use either '\
                  '<PULLUPS ON> or <PULLUPS OFF>***'
        #end if  
        
    else:
        print '*** The configuration command requested in not valid, '\
              'refer to Read Me***'
    # end if  
    
    return new_address
# end def


def write_aardvark(directives, gui):
    """
    Write to the slave device using the Aardvark and print its results 
    to the GUI.
    
    @param[in]  directives:  Instructions to direct the sending of 
                             data (pySCPI_config.write_directives)
    @param[in]  gui:         Instance of the gui that this function is 
                             called by (pySCPI_gui.main_gui).
    @return     int(0):      Failed to use Aardvark.
                None         Otherwise.
    """    
    # local copy of the write directives
    dec_addr = directives.addr
    commands = directives.command_list
    Delay = directives.delay_time
    Ascii_delay = directives.ascii_time
    
    # configure Aardvark if available
    Aardvark_in_use = configure_aardvark()
    
    # Check to see if an Aardvark was actually found
    if Aardvark_in_use != None:
        # iterate through commands and add them to the aardvark file
        # commands that start with # are deemed comments
        for command in [c for c in commands if not c.startswith('#')]:
            # determine if the command is a configuration command
            if pySCPI_config.is_config(command):
                # configure the system based on the config command
                dec_addr = update_aardvark(command, dec_addr, Aardvark_in_use)
                
            else:
                # Prepare the data for transmission
                if pySCPI_config.is_raw_write(command):
                    # it is a raw write command to send that
                    send_raw_command(command, AArdvark_in_use)
                    
                elif pySCPI_config.is_raw_read(command):
                    # it is a rew read command so read the data
                    read_raw_command(command, AArdvark_in_use)
                    
                else:
                    # it is a normal command
                    send_scpi_command(command, Aardvark_in_use, dec_addr)
                # end if
            # end if
            
            if 'TEL?' in command:
                # an I2C read has been requested
                
                # delay before reading the data
                if command.endswith('ascii'):
                    # sleep a different amount if ascii was requested
                    aardvark_py.aa_sleep_ms(Ascii_delay)
                    
                else:
                    aardvark_py.aa_sleep_ms(Delay)
                # end if
                
                # define array to read data into
                data = array('B', [1]*pySCPI_formatting.read_length(command, gui)) 
                
                # read from the slave device
                read_data = aardvark_py.aa_i2c_read(Aardvark_in_use, 
                                                    dec_addr, 
                                                    aardvark_py.AA_I2C_NO_FLAGS, 
                                                    data)
                
                # print the recieved data
                pySCPI_formatting.print_read(command, list(read_data[1]), 
                                             gui)
                # end if
            # end if
            
            # print an empty line
            print ''
            
            # intermessage delay
            aardvark_py.aa_sleep_ms(Delay)
            
            if gui.terminator.kill_event.isSet():
                # this thread has been asked to terminate
                break
            # end
        # end for
        
        # close the AArdvark device
        aardvark_py.aa_close(Aardvark_in_use)
        print 'Aardvark communications finished'
    
    else:
        return 0
    # end if
# end def

     
def log_aardvark(directives, filename, gui):
    """
    Write to the slave device using the Aardvark and print to 
    the gui and save the data to a csv log file.
    
    @param[in]  directives:  Instructions to direct the sending of 
                             data (pySCPI_config.write_directives)
    @param[in]  filename:    The absolute directory of the file to write 
                             log to (string).
    @param[in]  gui:         Instance of the gui that this function is 
                             called by (pySCPI_gui.main_gui).
    @return     int(0):      Failed to use Aardvark.
    """     
    # unpack the write directives
    addr = directives.addr
    commands = directives.command_list
    Delay = directives.delay_time
    Ascii_delay = directives.ascii_time
    logging_p = directives.logging_p
    
    # set up the csv writing output
    csv_output = open(filename, 'wb')
    output_writer = csv.writer(csv_output, delimiter = '\t')
    
    # create the header for the csv file
    csv_line = create_csv_header(commands, gui)
    
    # write the header
    output_writer.writerow(csv_line)     
    
    # configure Aardvark if available
    Aardvark_in_use = configure_aardvark()
    
    # Check to see if an Aardvark was actually found
    if Aardvark_in_use != None:    
        
        # start the loop timer
        start_time = time.time()
        
        # loop until the thread is asked to exit
        while not gui.terminator.kill_event.isSet():
            
            # define variables for the row
            csv_row = []
            dec_addr = addr
            first_timestamp = ''
            
            # iterate through commands and add them to the aardvark file
            # commands that start with # are deemed comments
            for command in [c for c in commands if not c.startswith('#')]:
                # determine if the command is a configuration command
                if pySCPI_config.is_config(command):
                    # configure the system based on the config command
                    dec_addr = update_aardvark(command, dec_addr, 
                                               Aardvark_in_use)
                    
                else:
                    # Prepare the data for transmission
                    if pySCPI_config.is_raw_write(command):
                        # it is a raw write command to send that
                        send_raw_command(command, AArdvark_in_use)
                        
                    elif pySCPI_config.is_raw_read(command):
                        # it is a rew read command so read the data and 
                        # add it to the csv row
                        csv_row.append(read_raw_command(command, 
                                                        AArdvark_in_use,
                                                        logging = True))
                        
                    else:
                        # it is a normal command
                        send_scpi_command(command, Aardvark_in_use, 
                                          dec_addr)
                    # end if
                # end if
                
                if 'TEL?' in command:
                    # the command is telemetry so log that
                    
                    # is it an ascii command
                    if command.endswith('ascii'):
                        # perform as ascii dealy
                        aardvark_py.aa_sleep_ms(Ascii_delay)
                        
                    else:
                        # perform a regular intermessage delay
                        aardvark_py.aa_sleep_ms(Delay)
                    # end if
                    
                    # define array to read data into
                    data = array('B', [1]*pySCPI_formatting.read_length(command, gui)) 
                    
                    # read from the slave device
                    read_data = aardvark_py.aa_i2c_read(Aardvark_in_use, 
                                                        dec_addr, 
                                                        aardvark_py.AA_I2C_NO_FLAGS, 
                                                        data)
                    
                    # print data
                    pySCPI_formatting.print_read(command, 
                                                 list(read_data[1]), 
                                                 gui)
                    
                    # log data
                    pySCPI_formatting.log_read(command, list(read_data[1]),
                                               csv_row, gui)
                # end if
                
                # print a blank line
                print ''
                
                # intermessage delay
                aardvark_py.aa_sleep_ms(Delay)
                
                # check to see if logging needs to stop
                if gui.terminator.kill_event.isSet():
                    # End if a stop has been issued
                    break            
                # end if
            # end while
            
            # get the earliest timestamp from the row
            first_timestamp = csv_row[0]
            
            # check to see if it is actually a timestamp
            if type(first_timestamp) == float:
                # it is a timestamp so convert it to a byte array of 
                # the  elapsed time in hundredths of a second
                timestamp_list = [ord(x) for x in '[1:' + 
                                  str(int(first_timestamp*100)) + ']']
                
                # convert the byte list to an ascii time
                timestamp_string = pySCPI_formatting.get_ascii_time(timestamp_list)
                
                # insert this timestamp at the beginning of the row
                csv_row.insert(0,timestamp_string)
                
            else:
                # the first entry is not a timestamp so leave it blank
                csv_row.insert(0,'-')
            # end if
            
            # write the row to the log file
            output_writer.writerow(csv_row)         
            
            # pace the loop to the correct logging period
            while (time.time() - start_time) < logging_p:
                # sleep to prevent resource hogging
                time.sleep(0.1)
                
                # check to see if logging should end
                if gui.terminator.kill_event.isSet():
                    # it should so exit
                    break
            # end if
            # end while
            
            start_time = time.time()
            
            # check to see if we can clear the gui for the next period
            if not gui.terminator.root_destroyed:        
                # clear the output display on the GUI
                gui.output_clear()
            # end if
        # end while
    
        # close the csv file
        csv_output.close()   
        
        # close the aardvark
        aardvark_py.aa_close(Aardvark_in_use)
        print 'Aardvark logging finished'
    
    else: 
        # no aardvark connection was established
        return 0
    # end if
# end def


#
# ----------------
# Private Functions


def query_delay_command(command):
    """
    Function to investigate a delay command, and if it is deemed valid
    then return the delay
    
    @param[in] command:          The command to be tested and executed
                                 (string).
    @return    (int)             The delay to be executed in miliseconds
                                 0 if the command is invalid
    """  
    
    
    # strip out the number
    delay_list = command.split(' ')
    delay_number = delay_list[1][0:-1]
    
    # verify that it is a number and that the beginning of 
    # the command was correct
    if delay_number.isdigit() and (delay_list[0] == '<DELAY'):
        # it is correct so retunr the delay period
        print 'Implementing additional ' + delay_number + 'ms delay.'
        delay = int(delay_number)
    else:
        # the delay is not valid
        print '*** The requested DELAY command is not valid. '\
              'Use <DELAY x>***'
        delay = 0
    # end if
    
    return delay
# end def

def configure_aardvark():
    """ 
    Function to configure the aardvark for pySCPI operation if there is one
    available.
    
    @return  (aardvark_py.aardvark)   The handle of the aardvark to be used
                                      'None' if there is not one available
    """
    # define the handle to return
    Aardvark_in_use = None
    
    # find all connected aardvarks
    AA_Devices = aardvark_py.aa_find_devices(1)
    
    # define a port mask
    Aardvark_port = 8<<7
    
    # assume that an aardvark can be found until proved otherwise
    Aardvark_free = True
    
    # Check if there is an Aardvark present
    if (AA_Devices[0] < 1):
        # there is no aardvark to be found
        print '*** No Aardvark is present ***'
        Aardvark_free = False
        
    else:
        # there is an aardvark connected to select the first one if there
        # are many
        Aardvark_port = AA_Devices[1][0]
    # end if
    
    
    # If there is an Aardvark there is it free?
    if Aardvark_port >= 8<<7 and Aardvark_free:
        # the aardvark is not free
        print '*** Aardvark is being used, '\
              'disconnect other application or Aardvark device ***'
        # close the aardvark
        aardvark_py.aa_close(Aardvark_port)
        Aardvark_free = False
        
    elif Aardvark_free:
        # Aardvark is available so configure it
        
        # open the connection with the aardvark
        Aardvark_in_use = aardvark_py.aa_open(Aardvark_port)
        
        # set it up in teh mode we need for pumpkin modules
        aardvark_py.aa_configure(Aardvark_in_use, 
                                 aardvark_py.AA_CONFIG_SPI_I2C)
        
        # default to both pullups on
        aardvark_py.aa_i2c_pullup(Aardvark_in_use, 
                                  aardvark_py.AA_I2C_PULLUP_BOTH)
        
        # set the bit rate to be the default
        aardvark_py.aa_i2c_bitrate(Aardvark_in_use, Bitrate)
        
        # free the bus
        aardvark_py.aa_i2c_free_bus(Aardvark_in_use)
        
        # delay to allow the config to be registered
        aardvark_py.aa_sleep_ms(200)    
        
        print "Starting Aardvark communications\n"
    # end if    
    
    return Aardvark_in_use
# end def


def send_raw_command(command, Aardvark_in_use):
    """
    Function to send a <RAW> command to a slave device.
    
    @param[in]    command:         The command to send (string).
    @param[in]    Aardvark_in_use: The Aaardvark to use to send the command
                                   (aardvark_py.aardvark)
    """
    
    # determine if it is a valid raw command
    if pySCPI_config.is_valid_raw(command):
        # it is so extract the data to write
        write_data = command[:-1].split(' ')
        
        # extract the address to write to
        raw_addr = int(write_data[1][:-1],16)
        
        # convert all of the data specified in the string to integers
        int_write_data = [int(item,16) for \
                          item in write_data[2:]]
        
        # add the terminator
        int_write_data.append(0x0a)
        
        # convert the data to an array to be compatible with the aardvark
        data = array('B', int_write_data)  
        
        # Write the data to the slave device
        aardvark_py.aa_i2c_write(Aardvark_in_use, raw_addr,
                                 aardvark_py.AA_I2C_NO_FLAGS, 
                                 data)
        # write output
        print 'Raw Write:\t\t[' + \
              ' '.join([str(item) for item in write_data[2:]]) + \
              '] to address ' + write_data[1][:-1]
        # end if                        
    else:
        # it is not a valid raw command
        print '*** Invalid WRITE command, please refer '\
              'to the Read me for proper syntax ***'
    # end if   
# end def

def read_raw_command(command, AArdvark_in_use, logging = False):
    """
    Function to read a <RAW> command from a slave device.
    
    @param[in]    command:         The command with the read information
                                   (string).
    @param[in]    Aardvark_in_use: The Aaardvark to use to read the data
                                   (aardvark_py.aardvark).
    @param[in]    logging:         Is the data read going to be logged. 
                                   If so, return the data (bool).
    @return       (string)         The data to be logged if logging 
                                   parameter is True.
    """    
    
    # check if the command is valid
    if pySCPI_config.is_valid_raw(command):
        # it is valid so break the command into parts
        data_list = command.split(' ')
        
        # extract the length to read
        data_len = int(data_list[2][:-1])
        
        # extract the address to read from
        raw_addr = int(data_list[1][:-1],16)
        
        # define the destination array
        data = array('B', [1]*data_len)
        
        # read the data
        read_data = aardvark_py.aa_i2c_read(Aardvark_in_use, raw_addr, 
                                            aardvark_py.AA_I2C_NO_FLAGS,
                                            data)
        
        # convert date to a string
        data_string = ' '.join(['%02X' % x for x in list(read_data[1])])
        
        # print the result
        print 'Raw Read:\t\t[' + data_string + '] from address ' + \
              data_list[1][:-1]
        
        # if the data is to be logged retun the data in a string format
        if logging:
            return data_string
        # end if
        
    else:
        # it is not a valid command
        print '*** Invalid READ command, please refer '\
              'to the Read me for proper syntax ***'
    # end if     
# end def

def send_scpi_command(command, Aardvark_in_use, dec_addr):
    """
    Function to send a SCPI command to the slave device
    
    @param[in]    command:         the command to send (string)
    @param[in]    Aardvark_in_use: The Aaardvark to use to read the data
                                   (aardvark_py.aardvark)
    @param[in]    dec_addr:        the decimal address to write to (int)
    """  
    
    # convert the data into a list of bytes and append the terminator
    write_data = list(command)
    write_data = [ord(item) for item in write_data]
    write_data.append(0x0a)
    
    # convert to an array to be compiant with the aardvark
    data = array('B', write_data)  
    
    
    # Write the data to the slave device
    aardvark_py.aa_i2c_write(Aardvark_in_use, dec_addr, 
                             aardvark_py.AA_I2C_NO_FLAGS, data)
    
    # print what was done
    if 'TEL?' in command:
        # there is data to follow
        print 'Read:\t\t' + command
    else:
        # there is not
        print 'Write:\t\t' + command
    # end if   
# end def


def create_csv_header(commands, gui):
    """
    Create a header line for the logging csv file by assiging a title to 
    every command.
    
    @param[in]  commands:          the command to look at (list of strings)
    @return     (list of strings)  The strings to form the csv header with.
    """   
    
    # start the header
    csv_line = ['Timestamp']
    
    # iterate through command list
    for command in commands:
        
        # only log telemetry requests and raw data reads
        if 'TEL?' in command:
            # is a telemetry request
            
            # does the command have time information
            if pySCPI_config.has_preamble(command):
                # can extract time data
                csv_line.append(command + ': Time (s)')
            # end if
            
            # find the print format for that command
            print_format = gui.scpi_commands.SCPI_Data[command][1]
            
            # check the print format
            if ',' not in print_format:
                # is only a single data item so append title
                csv_line.append(command + ': Data')
                
            else:
                # is a list so create a column for every item in the list
                for i in range(len(print_format.split(','))):
                    csv_line.append(command + ': Data[' + str(i) + ']')
                # end for
            # end if
            
        elif is_raw_read(command):
            # the command is a raw_read command
            if is_valid_raw(command):
                # and it is a valid raw command
                csv_line.append(command)
            # end if
        # end if
    # end for  
    
    return csv_line
# end def