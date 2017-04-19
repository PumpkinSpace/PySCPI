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
__version__ = '0.3.0' #Versioning: http://www.python.org/dev/peps/pep-0386/


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

# Configure I2C (DO NOT MODIFY)
I2C = True
SPI = True
GPIO = False
Pullups = True
radix = 16

use_aardvark = True
use_XML = True

######################## User Defined Configuration ############################
# Bitrate in kHz
Bitrate = 100
################################################################################


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
    gui.aardvark_button.config(background = 'green')
    
    # clear output
    gui.output_text.config(state='normal')
    gui.output_text.delete('1.0', 'end')
    gui.output_text.config(state='disabled') 
    
    # determine delay
    delay_text = gui.delay.get()
    delay_time = gui.defaults.default_delay;
    if delay_text.isdigit():
        # is a good delay
        delay_time = int(delay_text)
    else:
        print '*** Requested delay is not valid, reverting to default ***'
        gui.delay.delete(0,'end')
        gui.delay.insert(0, str(delay_time))
    # end if
    
    # determine ascii delay
    ascii_text = gui.ascii.get()
    ascii_time = gui.defaults.default_delay*4;
    if ascii_text.isdigit():
        # is a good delay
        ascii_time = int(ascii_text)
    else:
        print '*** Requested ascii delay is not valid, '\
              'reverting to default ***'
        gui.ascii.delete(0,'end')
        gui.ascii.insert(0, str(ascii_time))
    # end if 
    
    # determine I2C address to write to
    addr_string = gui.addr_text.get()
    addr_num = 0
    if addr_string.startswith('0x') and (len(addr_string) == 4) and \
       pySCPI_config.is_hex(addr_string[2:]):
        # is a good address
        addr_num = int(addr_string,16)
    else:
        print '*** Invalid address entered, reverting to device default ***'
        gui.addr_string = address_of[gui.slave_var.get()]
        gui.addr_var.set(addr_string)
        addr_num = int(addr_string,16)
    # end if
    
    # get command list from GUI
    input_string = gui.Command_text.get('1.0', 'end').encode('ascii', 'ignore')
    input_list = input_string.split('\n')
    command_list = []
    for item in input_list:
        # add all acceptible command to the list
        item = item.strip()
        if item != '':
            command_list = command_list + [item]
        # end if
    # end for
    
    # start the thread to perform the writing
    write_thread = threading.Thread(target = pySCPI_threading.I2C_thread, 
                                    args=(command_list, addr_num, 
                                          delay_time, ascii_time, gui))
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
    gui.logging_button.config(background = 'green')
    
    # clear output
    gui.output_text.config(state='normal')
    gui.output_text.delete('1.0', 'end')
    gui.output_text.config(state='disabled') 
    
    # determine delay
    delay_text = gui.delay.get()
    delay_time = gui.defaults.default_delay;
    if delay_text.isdigit():
        # delay is good
        delay_time = int(delay_text)
    else:
        print '*** Requested delay is not valid, reverting to default ***'
        gui.delay.delete(0,END)
        gui.delay.insert(0, str(delay_time))
    # end if
    
    # determine ascii delay
    ascii_text = gui.ascii.get()
    ascii_time = gui.defaults.default_delay*4;
    if ascii_text.isdigit():
        # delay is good
        ascii_time = int(ascii_text)
    else:
        print '*** Requested ascii delay is not valid, '\
              'reverting to default ***'
        gui.ascii.delete(0,END)
        gui.ascii.insert(0, str(ascii_time))
    # end if 
    
    # determine I2C address to write to
    addr_string = gui.addr_text.get()
    addr_num = 0
    if addr_string.startswith('0x') and (len(addr_string) == 4) and \
       pySCPI_config.is_hex(addr_string[2:]):
        # address is good
        addr_num = int(addr_string,16)
    else:
        print '*** Invlaid address entered, reverting to device default ***'
        gui.addr_string = address_of[gui.slave_var.get()]
        gui.addr_var.set(addr_string)
        addr_num = int(addr_string,16)
    # end if
    
    # get command list
    input_string = gui.Command_text.get('1.0', 'end').encode('ascii', 
                                                             'ignore')
    input_list = input_string.split('\n')
    command_list = []
    for item in input_list:
        # add all commands to a list
        item = item.strip()
        if item != '':
            command_list = command_list + [item]
        # end if
    # end for
    
    # find the required loop period
    loop_time = 0
    for command in command_list:
        # add up the time of all the commands in the list
        if 'ascii' in command:
            # is ascii
            loop_time += (ascii_time + delay_time)
        elif 'TEL?' in command:
            # is telemetry
            loop_time += (2*delay_time)
        else:
            # is just a command
            loop_time += delay_time
        # end if
    # end for
    
    # evaluate the perscribed loop period
    logging_text = gui.logging.get()
    logging_time = (loop_time/1000)+1;
    if logging_text.isdigit():
        # delay is a number
        logging_time = int(logging_text)
    else:
        print '*** Requested logging period is not valid, '\
              'reverting to default ***'
        gui.logging.delete(0,'end')
        gui.logging.insert(0, str(logging_time))
    # end if
    
    if logging_time*1000.0 <= loop_time*1.2:
        print '*** Warning, logging period may be shorter than '\
              'the duration of the commands requested ***'
    # end if
    
    # open a save file window
    file_opt = options = {}
    options['defaultextension'] = '.csv'
    options['filetypes'] = [('csv files', '.csv')]
    options['initialdir'] = os.getcwd() + '\\log_files'
    options['initialfile'] = 'example_log.csv'
    options['title'] = 'Save .csv log file as:'       
    
    filename_full = TKFD.asksaveasfilename(**file_opt)
    
    if (filename_full == ''):
        # No file was selected
        gui.output_text.config(state='normal')
        gui.output_text.delete('1.0', 'end')
        gui.output_text.config(state='disabled')        
        print '*** No Logging filename selected ***'
        # unlock buttons
        gui.action_lock('Unlock')
    else: 
        # start the logging thread
        log_thread = threading.Thread(target = pySCPI_threading.I2C_log_thread, 
                                      args=(command_list, addr_num, 
                                            delay_time, ascii_time, 
                                            logging_time, filename_full, 
                                            gui))
        log_thread.start()
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
        # strip out the number
        delay_list = command.split(' ')
        delay_number = delay_list[1][0:-1]
        # verify that it is a number and that the beginning of 
        # the command was correct
        if delay_number.isdigit() and (delay_list[0] == '<DELAY'):
            # perform a millisecond delay
            print 'Implementing additional ' + delay_number + 'ms delay.'
            aardvark_py.aa_sleep_ms(int(delay_number))  
        else:
            # the delay is not valid
            print '*** The requested DELAY command is not valid. '\
                  'Use <DELAY x>***'
        # end if
             
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



def write_aardvark(commands, addr, Delay, Ascii_delay, gui):
    """
    Write to the slave device using the Aardvark and print its results 
    to the GUI.
    
    @param[in]  commands:    List of commands to be sent (list of strings).
    @param[in]  dec_addr:    I2C address of the slave device (int).
    @param[in]  Delay:       Millisecond delay to wait between 
                             transmissions (int).
    @param[in]  Ascii_delay: Millisecond delay to wait before reading an 
                             'ascii' request (int).
    @param[in]  gui:         Instance of the gui that this function is 
                             called by (pySCPI_gui.main_gui).
    @return     int(0):      Failed to use Aardvark.
                None         Otherwise.
    """    
    # local copy of the address
    dec_addr = addr
    
    # configure Aardvark if available
    AA_Devices = aardvark_py.aa_find_devices(1)
    Aardvark_free = True
    Aardvark_port = 8<<7
    
    # Check if there is an Aardvark present
    if (AA_Devices[0] < 1):
        print '*** No Aardvark is present ***'
        Aardvark_free = False
        return 0
    else:
        Aardvark_port = AA_Devices[1][0]
    # end if
    
    # If there is an Aardvark there is it free?
    if Aardvark_port >= 8<<7 and Aardvark_free:
        print '*** Aardvark is being used, '\
              'disconnect other application or Aardvark device ***'
        aardvark_py.aa_close(Aardvark_port)
        Aardvark_free = False
        return 0
    elif Aardvark_free:
        # Aardvark is available so configure it
        Aardvark_in_use = aardvark_py.aa_open(Aardvark_port)
        aardvark_py.aa_configure(Aardvark_in_use, 
                                 aardvark_py.AA_CONFIG_SPI_I2C)
        aardvark_py.aa_i2c_pullup(Aardvark_in_use, 
                                  aardvark_py.AA_I2C_PULLUP_BOTH)
        aardvark_py.aa_i2c_bitrate(Aardvark_in_use, Bitrate)
        aardvark_py.aa_i2c_free_bus(Aardvark_in_use)
        aardvark_py.aa_sleep_ms(Delay)    
        print "Starting Aardvark communications\n"
    # end if
    
    # iterate through commands and add them to the aardvark file
    for command in commands:
        # See if the Aardvark is free
        if Aardvark_free:
            # determine if the command is a configuration command
            if pySCPI_config.is_config(command):
                # configure the system based on the config command
                dec_addr = update_aardvark(command, dec_addr, 
                                           Aardvark_in_use)
            else:
                # Prepare the data for transmission
                if pySCPI_config.is_raw_write(command):
                    if pySCPI_config.is_valid_raw(command):
                        write_data = command[:-1].split(' ')
                        raw_addr = int(write_data[1][:-1],16)
                        int_write_data = [int(item,16) for \
                                          item in write_data[2:]]
                        int_write_data.append(0x0a)
                        data = array('B', int_write_data)  
                        # Write the data to the slave device
                        aardvark_py.aa_i2c_write(Aardvark_in_use, raw_addr,
                                                 aardvark_py.AA_I2C_NO_FLAGS, 
                                                 data)
                        print 'Raw Write:\t\t[' + \
                              ' '.join([str(item) for \
                                         item in write_data[2:]]) + \
                              '] to address ' + write_data[1][:-1]
                        # end if                        
                    else:
                        print '*** Invalid WRITE command, please refer '\
                              'to the Read me for proper syntax ***'
                    # end if
                elif not pySCPI_config.is_raw_read(command):
                    write_data = list(command)
                    write_data = [ord(item) for item in write_data]
                    write_data.append(0x0a)
                    data = array('B', write_data)  
                    # Write the data to the slave device
                    aardvark_py.aa_i2c_write(Aardvark_in_use, dec_addr, 
                                             aardvark_py.AA_I2C_NO_FLAGS, 
                                             data)
                    if 'TEL?' in command:
                        print 'Read:\t\t' + command
                    else:
                        print 'Write:\t\t' + command
                    # end if

                else:
                    # is a raw read command
                    if pySCPI_config.is_valid_raw(command):
                        data_list = command.split(' ')
                        data_len = int(data_list[2][:-1])
                        raw_addr = int(data_list[1][:-1],16)
                        
                        data = array('B', [1]*data_len)
                        read_data = aardvark_py.aa_i2c_read(Aardvark_in_use,
                                                            raw_addr, 
                                                            aardvark_py.AA_I2C_NO_FLAGS,
                                                            data)
                        
                        print 'Raw Read:\t\t[' + \
                              ' '.join(['%02X' % x for \
                                        x in list(read_data[1])]) + \
                              '] from address ' + data_list[1][:-1]
                    else:
                        print '*** Invalid READ command, please refer '\
                              'to the Read me for proper syntax ***'
                    # end if    
                # end if
            # end if
        # end if
        
        if 'TEL?' in command:
            # an I2C read has been requested
            # if the Aardvark is free read from it
            if Aardvark_free:
                if command.endswith('ascii'):
                    # sleep a different amount if ascii was requested
                    aardvark_py.aa_sleep_ms(Ascii_delay)
                else:
                    aardvark_py.aa_sleep_ms(Delay)
                # end if
                
                # read from the slave device
                data = array('B', [1]*pySCPI_formatting.read_length(command, gui)) 
                read_data = aardvark_py.aa_i2c_read(Aardvark_in_use, 
                                                    dec_addr, 
                                                    aardvark_py.AA_I2C_NO_FLAGS, 
                                                    data)
                
                # print the recieved data
                pySCPI_formatting.print_read(command, list(read_data[1]), 
                                             gui)
            # end if
        # end if
        print ''
        aardvark_py.aa_sleep_ms(Delay)
        
        if gui.terminator.kill_event.isSet():
            # this thread has been asked to terminate
            break
        # end
    # end while
    
    if Aardvark_free:
        # close the AArdvark device
        aardvark_py.aa_close(Aardvark_port)
        print 'Aardvark communications finished'
    # end if
# end def

     
def log_aardvark(commands, addr, Delay, Ascii_delay, 
                 logging_p, filename, gui):
    """
    Write to the slave device using the Aardvark and print to 
    the gui and save the data to a csv log file.
    
    @param[in]  commands:    List of commands to be sent (list of strings).
    @param[in]  dec_addr:    I2C address of the slave device (int).
    @param[in]  Delay:       Millisecond delay to wait between 
                             transmissions (int).
    @param[in]  Ascii_delay: Millisecond delay to wait before reading 
                             an 'ascii' request (int).
    @param[in]  logging_p:   The period in seconds to use for the logging 
                             loop (int).
    @param[in]  filename:    The absolute directory of the file to write 
                             log to (string).
    @param[in]  gui:         Instance of the gui that this function is 
                             called by (pySCPI_gui.main_gui).
    @return     int(0):      Failed to use Aardvark.
    """     
    csv_line = ['Timestamp']
    output_writer = None
    csv_output = None
    # create CSV Header
    for command in commands:
        if 'TEL?' in command:
            # is a telemetry request
            if pySCPI_config.has_preamble(command):
                # can extract time data
                csv_line.append(command + ': Time (s)')
            # end if
            print_format = gui.scpi_commands.SCPI_Data[command][1]
            if ',' not in print_format:
                # is only a single data item so append title
                csv_line.append(command + ': Data')
            else:
                # is a list so create a column for every item in the list
                for i in range(len(print_format.split(','))):
                    csv_line.append(command + ': Data[' + str(i) + ']')
                # end for
            # end if
        # end if
    # end for
    
    # write Header
    filename_short = filename.split('/')[-1]
    filename_dir = filename[:filename.rfind('/')]
    if (filename_short not in os.listdir(filename_dir)) or \
       pySCPI_config.file_is_free(filename): 
        # write header to the log file
        csv_output = open(filename, 'wb')
        output_writer = csv.writer(csv_output, delimiter = '\t')
        output_writer.writerow(csv_line) 
    else:
        print'*** Requested log file is in use by another program ***'
        return 0
    # end if
    
    # Configure the Aardvark if present
    AA_Devices = aardvark_py.aa_find_devices(1)
    Aardvark_free = True
    Aardvark_port = 8<<7
    if (AA_Devices[0] < 1):
        print '*** No Aardvark is present ***'
        Aardvark_free = False
        return 0
    else:
        Aardvark_port = AA_Devices[1][0]
    # end
    
    # If there is an Aardvark there is it free?
    if Aardvark_port >= 8<<7 and Aardvark_free:
        print '*** Aardvark is being used, disconnect other '\
              'application or Aardvark device ***'
        aardvark_py.aa_close(Aardvark_port)
        Aardvark_free = False
        return 0
    elif Aardvark_free:
        # Aardvark is available so configure it
        Aardvark_in_use = aardvark_py.aa_open(Aardvark_port)
        aardvark_py.aa_configure(Aardvark_in_use, 
                                 aardvark_py.AA_CONFIG_SPI_I2C)
        aardvark_py.aa_i2c_pullup(Aardvark_in_use, 
                                  aardvark_py.AA_I2C_PULLUP_BOTH)
        aardvark_py.aa_i2c_bitrate(Aardvark_in_use, Bitrate)
        aardvark_py.aa_i2c_free_bus(Aardvark_in_use)
        aardvark_py.aa_sleep_ms(Delay)    
        print "Starting Aardvark communications\n"
    # end    

    start_time = time.time()
    
    # loop until the thread is asked to exit
    while not gui.terminator.kill_event.isSet():
        csv_row = []
        dec_addr = addr
        first_timestamp = ''
        
        # iterate through commands and add them to the aardvark file
        for command in commands:
            # See if the Aardvark is free
            if Aardvark_free:
                # determine if the command is a configuration command
                if pySCPI_config.is_config(command):
                    # configure the system based on the config command
                    dec_addr = update_aardvark(command, dec_addr, 
                                               Aardvark_in_use)
                else:
                    if pySCPI_config.is_raw_write(command):
                        if pySCPI_config.is_valid_raw(command):
                            write_data = command[:-1].split(' ')
                            raw_addr = int(write_data[1][2:-1],16)
                            int_write_data = [int(item,16) for \
                                              item in write_data[2:]]
                            int_write_data.append(0x0a)
                            data = array('B', int_write_data)  
                            # Write the data to the slave device
                            aardvark_py.aa_i2c_write(Aardvark_in_use, 
                                                     raw_addr, 
                                                     aardvark_py.AA_I2C_NO_FLAGS, 
                                                     data)
                            print 'Raw Write:\t\t[' + \
                                  ', '.join([str(item) for \
                                             item in write_data[2:]]) + \
                                  '] to address ' + write_data[1][:-1]
                            # end if                        
                        else:
                            print '*** Invalid WRITE command, please refer'\
                                  ' to the Read me for proper syntax ***'
                        # end if  
                        
                    elif not pySCPI_config.is_raw_read(command):
                        # Prepare the data for transmission
                        write_data = list(command)
                        write_data = [ord(item) for item in write_data]
                        write_data.append(0x0a)
                        data = array('B', write_data)  
                        # Write the data to the slave device
                        aardvark_py.aa_i2c_write(Aardvark_in_use, 
                                                 dec_addr, 
                                                 aardvark_py.AA_I2C_NO_FLAGS,
                                                 data)
                        if 'TEL?' in commands:
                            print 'Read:\t\t' + command
                        else:
                            print 'Write:\t\t' + command
                        # end if
                        
                    else:
                        # is a raw read command
                        if pySCPI_config.is_valid_raw(command):
                            data_list = command.split(' ')
                            data_len = int(data_list[2][:-1])
                            raw_addr = int(data_list[1][2:-1],16)
                            
                            data = array('B', [1]*data_len)
                            read_data = aardvark_py.aa_i2c_read(Aardvark_in_use, 
                                                                raw_addr, 
                                                                aardvark_py.AA_I2C_NO_FLAGS, 
                                                                data)
                            
                            print 'Raw Read:\t\t[' + \
                                  ', '.join(['0x%02x' % x for \
                                             x in list(read_data[1])]) + \
                                  '] from address ' + data_list[1][:-1]
                            
                            pySCPI_formatting.log_read(command, 
                                                       list(read_data[1]), 
                                                       csv_row)
                        else:
                            print '*** Invalid READ command, please refer'\
                                  'to the Read me for proper syntax ***'
                        # end if    
                    # end if
                # end if
            # end if
            
            if 'TEL?' in command:
                # if the Aardvark is free read from it
                if Aardvark_free:
                    if command.endswith('ascii'):
                        aardvark_py.aa_sleep_ms(Ascii_delay)
                    else:
                        aardvark_py.aa_sleep_ms(Delay)
                    # end if
                    
                    # read from the slave device
                    data = array('B', [1]*pySCPI_formatting.read_length(command, gui)) 
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
                    # write to log file              
                # end if
            # end if
            print ''
            aardvark_py.aa_sleep_ms(Delay)
            
            if gui.terminator.kill_event.isSet():
                # End if a stop has been issued
                break            
            # end if
            
        # end while
        
        first_timestamp = csv_row[0]
        if type(first_timestamp) == float:
            timestamp_list = [ord(x) for x in '[1:' + 
                              str(int(first_timestamp*100)) + ']']
            timestamp_string = pySCPI_formatting.get_ascii_time(timestamp_list)
            csv_row.insert(0,timestamp_string)
        else:
            csv_row.insert(0,'-')
            
        
        # write to log file
        output_writer.writerow(csv_row)         
        
        while (time.time() - start_time) < logging_p:
            # delay to maintain the logging period
            time.sleep(0.1)
            if gui.terminator.kill_event.isSet():
                break
        # end if
        # end while
        
        start_time = time.time()
        
        
        if not gui.terminator.root_destroyed:        
            # clear the output display on the GUI
            gui.output_text.config(state = 'normal')
            gui.output_text.delete('1.0', 'end')
            gui.output_text.config(state='disabled')
        # end if
        
    # end while
    
    # close the csv file
    csv_output.close()   

    if Aardvark_free:
        # close the aardvark
        aardvark_py.aa_close(Aardvark_port)
        print 'Aardvark communications finished'
    # end if
# end def

