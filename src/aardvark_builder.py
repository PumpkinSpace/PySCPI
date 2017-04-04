# Aardvark batch script writer
# Pumpkin Inc.
# David Wright 2016

import xml.etree.ElementTree as ET
import sys
from aardvark_py import *
from SCPI_formatting import *
from tkFileDialog import *
import time
from pySCPI_config import *
from Tkinter import *
import os

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

"""
Determine if a file that is to be modified is being used by another program.

@param[in]  filename: The absolute directory of the file (string).
@return     (bool)    True:     The file is not being used by another program.
                      False:    The file is in use.
"""
def file_is_free(filename):
    try:
        # attempt to change the files name to see if it is available.
        os.rename(filename,filename)
        return True
    except OSError as e:
        # renaming was not possible as another program is using it.
        return False
    # end try
# end def


"""
Perform the configureation requested by a config command

@param[in]  command:         The configuration comamnd requested (string).
@param[in]  address:         The current I2C slave address in use (int).
@param[in]  AArdvark_in_use: The aardvark port in use (Aardvark handle).
@return     (int)            The new I2C address to use (potentially unchanged).
"""
def update_aardvark(command, address, Aardvark_in_use):
    new_address = address
    # determine the appropriate action to take
    if 'DELAY ' in command:
        # strip out the number
        delay_list = command.split(' ')
        delay_number = delay_list[1][0:-1]
        # verify that it is a number and that the beginning of the command was correct
        if delay_number.isdigit() and (delay_list[0] == '<DELAY'):
            # perform a millisecond delay
            print 'Implementing additional ' + delay_number + 'ms delay.'
            aa_sleep_ms(int(delay_number))  
        else:
            # the delay is not valid
            print '*** The requested DELAY command is not valid. Use <DELAY x>***'
        # end if
             
    elif 'ADDRESS ' in command:
        # strip out the number
        address_list = command.split(' ')
        address_hex = address_list[1][0:-1]
        # verify that it is a number and that the beginning of the command was correct
        if address_hex.startswith('0x') and (len(address_hex) == 4) and is_hex(address_hex[2:]) and (address_list[0] == '<ADDRESS'):
            # is a good address
            new_address = int(address_hex,16)
            print 'Changed slave I2C address to ' + address_hex + '.'
        else:
            # the adderss is invlaid
            print '*** The requested ADDRESS command is not valid. Use <ADDRESS 0xYY>***'
        # end if        
    
    elif 'BITRATE ' in command:
        # strip out the number
        speed_list = command.split(' ')
        speed_num = speed_list[1][0:-1] 
        if speed_num.isdigit() and (speed_list[0] == '<BITRATE'):
            # is a good bitrate
            bitrate = aa_i2c_bitrate(Aardvark_in_use, int(speed_num))
            aa_sleep_ms(200)             
            print 'Changed I2C bitrate to ' + str(bitrate) + 'kHz.'
        else:
            # the bitrate is invlaid
            print '*** The requested BITRATE command is not valid. Use <BITRATE x>***'
        # end if         
        
    elif 'PULLUPS ' in command:
        # check command
        if command == '<PULLUPS ON>':
            # turn pullups on
            aa_i2c_pullup(Aardvark_in_use, AA_I2C_PULLUP_BOTH)
            aa_sleep_ms(200)   
            print 'Turned I2C pullups on.'
        
        elif command == '<PULLUPS OFF>':
            # turn pullups off
            aa_i2c_pullup(Aardvark_in_use, AA_I2C_PULLUP_NONE)
            aa_sleep_ms(200)  
            print 'Turned I2C pullups off.'
        
        else:
            print '*** Invalid Pullup Command, use either <PULLUPS ON> or <PULLUPS OFF>***'
        #end if  
        
    else:
        print '*** The configuration command requested in not valid, refer to Read Me***'
    # end if  
    
    return new_address
# end def
        

"""
Write to the slave device using the Aardvark and print its results to the GUI

@param[in]  exit_event:  Event to terminate the function (threading.Event).
@param[in]  commands:    List of commands to be sent (list of strings).
@param[in]  dec_addr:    I2C address of the slave device (int).
@param[in]  Delay:       Millisecond delay to wait between transmissions (int).
@param[in]  Ascii_delay: Millisecond delay to wait before reading an 'ascii' 
                         request (int).
@param[in]  float_dp:    The number of decimal places to print a float to (int).
@return     int(0):      Failed to use Aardvark.
            None         Otherwise.
"""
def write_aardvark(exit_event, commands, addr, Delay, Ascii_delay, float_dp):
    # local copy of the address
    dec_addr = addr
    
    # configure Aardvark if available
    AA_Devices = aa_find_devices(1)
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
        print '*** Aardvark is being used, disconnect other application or Aardvark device ***'
        aa_close(Aardvark_port)
        Aardvark_free = False
        return 0
    elif Aardvark_free:
        # Aardvark is available so configure it
        Aardvark_in_use = aa_open(Aardvark_port)
        aa_configure(Aardvark_in_use, AA_CONFIG_SPI_I2C)
        aa_i2c_pullup(Aardvark_in_use, AA_I2C_PULLUP_BOTH)
        aa_i2c_bitrate(Aardvark_in_use, Bitrate)
        aa_i2c_free_bus(Aardvark_in_use)
        aa_sleep_ms(Delay)    
        print "Starting Aardvark communications\n"
    # end if
    
    # iterate through commands and add them to the aardvark file
    for command in commands:
        # See if the Aardvark is free
        if Aardvark_free:
            # determine if the command is a configuration command
            if is_config(command):
                # configure the system based on the config command
                dec_addr = update_aardvark(command, dec_addr, Aardvark_in_use)
            else:
                # Prepare the data for transmission
                if is_raw_write(command):
                    if is_valid_raw(command):
                        write_data = command[:-1].split(' ')
                        raw_addr = int(write_data[1][:-1],16)
                        int_write_data = [int(item,16) for item in write_data[2:]]
                        int_write_data.append(0x0a)
                        data = array('B', int_write_data)  
                        # Write the data to the slave device
                        aa_i2c_write(Aardvark_in_use, raw_addr, AA_I2C_NO_FLAGS, data)
                        print 'Raw Write:\t\t[' + ', '.join([str(item) for item in write_data[2:]]) + '] to address ' + write_data[1][:-1]
                        # end if                        
                    else:
                        print '*** Invalid WRITE command, please refer to the Read me for proper syntax ***'
                    # end if
                elif not is_raw_read(command):
                    write_data = list(command)
                    write_data = [ord(item) for item in write_data]
                    write_data.append(0x0a)
                    data = array('B', write_data)  
                    # Write the data to the slave device
                    aa_i2c_write(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                    if 'TEL?' in command:
                        print 'Read:\t\t' + command
                    else:
                        print 'Write:\t\t' + command
                    # end if

                else:
                    # is a raw read command
                    if is_valid_raw(command):
                        data_list = command.split(' ')
                        data_len = int(data_list[2][:-1])
                        raw_addr = int(data_list[1][:-1],16)
                        
                        data = array('B', [1]*data_len)
                        read_data = aa_i2c_read(Aardvark_in_use, raw_addr, AA_I2C_NO_FLAGS, data)
                        
                        print 'Raw Read:\t\t[' + ', '.join(['0x%02x' % x for x in list(read_data[1])]) + '] from address ' + data_list[1][:-1]
                    else:
                        print '*** Invalid READ command, please refer to the Read me for proper syntax ***'
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
                    aa_sleep_ms(Ascii_delay)
                else:
                    aa_sleep_ms(Delay)
                # end if
                
                # read from the slave device
                data = array('B', [1]*read_length(command)) 
                read_data = aa_i2c_read(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                
                # print the recieved data
                print_read(command, list(read_data[1]), float_dp)
            # end if
        # end if
        print ''
        aa_sleep_ms(Delay)
        
        if exit_event.isSet():
            # this thread has been asked to terminate
            break
        # end
    # end while
    
    if Aardvark_free:
        # close the AArdvark device
        aa_close(Aardvark_port)
        print 'Aardvark communications finished'
    # end if
# end def

  
   
"""
Write to the slave device using the Aardvark and print to the gui and save the
data to a csv log file.

@param[in]  exit_event:  Event to terminate the function (threading.Event).
@param[in]  commands:    List of commands to be sent (list of strings).
@param[in]  dec_addr:    I2C address of the slave device (int).
@param[in]  Delay:       Millisecond delay to wait between transmissions (int).
@param[in]  Ascii_delay: Millisecond delay to wait before reading an 'ascii' 
                         request (int).
@param[in]  float_dp:    The number of decimal places to print a float to (int).
@param[in]  logging_p:   The period in seconds to use for the logging loop (int).
@param[in]  filename:    The absolute directory of the file to write log to (string).
@param[out] output_text: The text window on the GUI to clear between logging loops.
@return     int(0):      Failed to use Aardvark.
"""      
def log_aardvark(exit_event, commands, addr, Delay, Ascii_delay, float_dp, logging_p, filename, output_text):

    csv_line = ['Timestamp']
    output_writer = None
    csv_output = None
    # create CSV Header
    for command in commands:
        if 'TEL?' in command:
            # is a telemetry request
            if has_preamble(command):
                # can extract time data
                csv_line.append(command + ': Time (s)')
            # end if
            print_format = SCPI_Data[command][1]
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
    if (filename_short not in os.listdir(filename_dir)) or file_is_free(filename): 
        # write header to the log file
        csv_output = open(filename, 'wb')
        output_writer = csv.writer(csv_output, delimiter = '\t')
        output_writer.writerow(csv_line) 
    else:
        print'*** Requested log file is in use by another program ***'
        return 0
    # end if
    
    # Configure the Aardvark if present
    AA_Devices = aa_find_devices(1)
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
        print '*** Aardvark is being used, disconnect other application or Aardvark device ***'
        aa_close(Aardvark_port)
        Aardvark_free = False
        return 0
    elif Aardvark_free:
        # Aardvark is available so configure it
        Aardvark_in_use = aa_open(Aardvark_port)
        aa_configure(Aardvark_in_use, AA_CONFIG_SPI_I2C)
        aa_i2c_pullup(Aardvark_in_use, AA_I2C_PULLUP_BOTH)
        aa_i2c_bitrate(Aardvark_in_use, Bitrate)
        aa_i2c_free_bus(Aardvark_in_use)
        aa_sleep_ms(Delay)    
        print "Starting Aardvark communications\n"
    # end    

    start_time = time.time()
    
    # loop until the thread is asked to exit
    while not exit_event.isSet():
        csv_row = []
        dec_addr = addr
        first_timestamp = ''
        
        # iterate through commands and add them to the aardvark file
        for command in commands:
            # See if the Aardvark is free
            if Aardvark_free:
                # determine if the command is a configuration command
                if is_config(command):
                    # configure the system based on the config command
                    dec_addr = update_aardvark(command, dec_addr, Aardvark_in_use)
                else:
                    if is_raw_write(command):
                        if is_valid_raw(command):
                            write_data = command[:-1].split(' ')
                            raw_addr = int(write_data[1][2:-1],16)
                            int_write_data = [int(item,16) for item in write_data[2:]]
                            int_write_data.append(0x0a)
                            data = array('B', int_write_data)  
                            # Write the data to the slave device
                            aa_i2c_write(Aardvark_in_use, raw_addr, AA_I2C_NO_FLAGS, data)
                            print 'Raw Write:\t\t[' + ', '.join([str(item) for item in write_data[2:]]) + '] to address ' + write_data[1][:-1]
                            # end if                        
                        else:
                            print '*** Invalid WRITE command, please refer to the Read me for proper syntax ***'
                        # end if  
                        
                    elif not is_raw_read(command):
                        # Prepare the data for transmission
                        write_data = list(command)
                        write_data = [ord(item) for item in write_data]
                        write_data.append(0x0a)
                        data = array('B', write_data)  
                        # Write the data to the slave device
                        aa_i2c_write(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                        if 'TEL?' in commands:
                            print 'Read:\t\t' + command
                        else:
                            print 'Write:\t\t' + command
                        # end if
                        
                    else:
                        # is a raw read command
                        if is_valid_raw(command):
                            data_list = command.split(' ')
                            data_len = int(data_list[2][:-1])
                            raw_addr = int(data_list[1][2:-1],16)
                            
                            data = array('B', [1]*data_len)
                            read_data = aa_i2c_read(Aardvark_in_use, raw_addr, AA_I2C_NO_FLAGS, data)
                            
                            print 'Raw Read:\t\t[' + ', '.join(['0x%02x' % x for x in list(read_data[1])]) + '] from address ' + data_list[1][:-1]
                            
                            log_read(command, list(read_data[1]), csv_row)
                        else:
                            print '*** Invalid READ command, please refer to the Read me for proper syntax ***'
                        # end if    
                    # end if
                # end if
            # end if
            
            if 'TEL?' in command:
                # if the Aardvark is free read from it
                if Aardvark_free:
                    if command.endswith('ascii'):
                        aa_sleep_ms(Ascii_delay)
                    else:
                        aa_sleep_ms(Delay)
                    # end if
                    
                    # read from the slave device
                    data = array('B', [1]*read_length(command)) 
                    read_data = aa_i2c_read(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                    
                    # print data
                    print_read(command, list(read_data[1]), float_dp)
                    
                    # log data
                    log_read(command, list(read_data[1]), csv_row)
                    # write to log file              
                # end if
            # end if
            print ''
            aa_sleep_ms(Delay)
            
            if exit_event.isSet():
                # End if a stop has been issued
                break            
            # end if
            
        # end while
        
        first_timestamp = csv_row[0]
        if type(first_timestamp) == float:
            timestamp_list = [ord(x) for x in '[1:' + str(int(first_timestamp*100)) + ']']
            timestamp_string = get_ascii_time(timestamp_list)
            csv_row.insert(0,timestamp_string)
        else:
            csv_row.insert(0,'-')
            
        
        # write to log file
        output_writer.writerow(csv_row)         
        
        while (time.time() - start_time) < logging_p:
            # delay to maintain the logging period
            time.sleep(0.1)
            if exit_event.isSet():
                break
        # end if
        # end while
        
        start_time = time.time()
        
                
        # clear the output display on the GUI
        output_text.config(state = NORMAL)
        output_text.delete('1.0', END)
        output_text.config(state=DISABLED)  
        
    # end while
    
    # close the csv file
    csv_output.close()   

    if Aardvark_free:
        # close the aardvark
        aa_close(Aardvark_port)
        print 'Aardvark communications finished'
    # end if
# end def


"""
Save the configuration requested by a config command to XML

@param[in]  command:         The configuration comamnd requested (string).
@param[in]  address:         The current I2C slave address in use (int).
@param[in]  XML:             The XML Element to add to (ET.Element).
@return     (int)            The new I2C address to use (potentially unchanged).
"""
def update_XML(command, address, XML):
    new_address = address
    # determine the appropriate action to take
    if 'DELAY ' in command:
        # strip out the number
        delay_list = command.split(' ')
        delay_number = delay_list[1][0:-1]
        # verify that it is a number and that the beginning of the command was correct
        if delay_number.isdigit() and (delay_list[0] == '<DELAY'):
            # perform a millisecond delay
            delay_attributes = {'ms': str(delay_number)} 
            ET.SubElement(XML, 'sleep', delay_attributes)
        else:
            # the delay is not valid
            print '*** The requested DELAY command is not valid. Use <DELAY x>***'
        # end if
             
    elif 'ADDRESS ' in command:
        # strip out the number
        address_list = command.split(' ')
        address_hex = address_list[1][0:-1]
        # verify that it is a number and that the beginning of the command was correct
        if address_hex.startswith('0x') and (len(address_hex) == 4) and is_hex(address_hex[2:]) and (address_list[0] == '<ADDRESS'):
            # is a good address
            new_address = address_hex
        else:
            # the adderss is invlaid
            print '*** The requested ADDRESS command is not valid. Use <ADDRESS 0xYY>***'
        # end if        
    
    elif 'BITRATE ' in command:
        # strip out the number
        speed_list = command.split(' ')
        speed_num = speed_list[1][0:-1] 
        if speed_num.isdigit() and (speed_list[0] == '<BITRATE'):
            # is a good bitrate
            rate_attributes = {'khz': speed_num}
            rate = ET.SubElement(XML, 'i2c_bitrate', rate_attributes)
            delay_attributes = {'ms': '200'} 
            ET.SubElement(XML, 'sleep', delay_attributes)             
        else:
            # the bitrate is invlaid
            print '*** The requested BITRATE command is not valid. Use <BITRATE x>***'
        # end if         
        
    elif 'PULLUPS ' in command:
        # check command
        if command == '<PULLUPS ON>':
            # turn pullups on
            config_attributes = {'i2c':     str(int(I2C)),
                                 'spi':     str(int(SPI)),
                                 'gpio':    str(int(GPIO)),
                                 'pullups': '1'}
    
            config = ET.SubElement(XML, 'configure', config_attributes)
            
            delay_attributes = {'ms': '200'} 
            ET.SubElement(XML, 'sleep', delay_attributes)  
        
        elif command == '<PULLUPS OFF>':
            # turn pullups off
            config_attributes = {'i2c':     str(int(I2C)),
                                 'spi':     str(int(SPI)),
                                 'gpio':    str(int(GPIO)),
                                 'pullups': '0'}
    
            config = ET.SubElement(XML, 'configure', config_attributes)
            
            delay_attributes = {'ms': '200'} 
            ET.SubElement(XML, 'sleep', delay_attributes)              
        
        else:
            print '*** Invalid Pullup Command, use either <PULLUPS ON> or <PULLUPS OFF>'
        #end if  
        
    else:
        print '*** The configuration command requested in not valid, refer to Read Me***'
    # end if  
    
    return new_address
# end def


"""
Write an Aardvark compatible .xml file that can be used with the Total phase 
system or loaded back into pySCPI

@param[in]  commands:      List of commands to be sent (list of strings).
@param[in]  addr:          I2C address of the slave device (string).
@param[in]  Delay:         Millisecond delay to wait between transmissions (int).
@param[in]  Ascii_delay:   Millisecond delay to wait before reading an 'ascii' 
                           request (int).
@return     filename_full: Absolute directory of the file created
"""   
def create_XML(commands, address, Delay, Ascii_delay):
    addr = address
    # Start XML
    aardvark = ET.Element('aardvark')
    
    aardvark.append(ET.Comment('Configuration (Need pullups, not sure why...)'))    
    
    # Configuration Element
    config_attributes = {'i2c':     str(int(I2C)),
                         'spi':     str(int(SPI)),
                         'gpio':    str(int(GPIO)),
                         'pullups': str(int(Pullups))}
    
    config = ET.SubElement(aardvark, 'configure', config_attributes)
    
    # Bitrate
    rate_attributes = {'khz': str(Bitrate)}
    
    rate = ET.SubElement(aardvark, 'i2c_bitrate', rate_attributes)
    
    # Start I2C
    start = ET.SubElement(aardvark, 'i2c_free_bus')
    
    # delay attributes
    delay_attributes = {'ms': str(Delay)}    
    ascii_delay_attributes = {'ms': str(Ascii_delay)}  
    
    # delay
    ET.SubElement(aardvark, 'sleep', delay_attributes)    
    
    # iterate through commands
    for command in commands: 
        
        if is_config(command):
            # add the configuration to the XML
            addr = update_XML(command, addr, aardvark)
            
        elif is_raw_write(command) or is_raw_read(command):
            if is_valid_raw(command):
                aardvark.append(ET.Comment(command))
                raw_list = command[:-1].split(' ')
                raw_addr = '0x' + raw_list[1][2:-1]
                if is_raw_write(command):
                    write_attributes = {'addr':  raw_addr,
                                        'count': str(len(raw_list)-1),
                                        'radix': str(radix)}
                    raw = ET.SubElement(aardvark, 'i2c_write', write_attributes)
                    
                    # add hexidecimal null terminated command as text to the write element
                    raw.text = ' '.join("{:02x}".format(int(c, 16)) for c in raw_list[2:]) + ' 0a'
                    
                else:
                    read_attributes = {'addr':  raw_addr,
                                       'count': raw_list[2],
                                       'radix': str(radix)}     
                    
                    read = ET.SubElement(aardvark, 'i2c_read', read_attributes) 
                # end if
                ET.SubElement(aardvark, 'sleep', delay_attributes)  
                
            else:
                if 'READ' in command:
                    print '*** Invalid READ command, please refer to the Read me for proper syntax ***'
                    
                else:
                    print '*** Invalid WRITE command, please refer to the Read me for proper syntax ***'
                # end if
            # end if        
                    
        else:
            
            # comment the string of the SCPI command
            aardvark.append(ET.Comment(command))
            
            # define attributes for write element
            write_attributes = {'addr':  addr,
                                'count': str(len(command)+1),
                                'radix': str(radix)}
            
            # create write element
            scpi = ET.SubElement(aardvark, 'i2c_write', write_attributes)
            
            # add hexidecimal null terminated command as text to the write element
            scpi.text = ' '.join("{:02x}".format(ord(c)) for c in command) + ' 0a'        
            
            if 'TEL?' in command:
                # Read command was issued so a read needs to be performed
                
                if command.endswith('ascii'):
                    # leave a longer delay for ascii commands
                    ET.SubElement(aardvark, 'sleep', ascii_delay_attributes)
                else:
                    ET.SubElement(aardvark, 'sleep', delay_attributes)
                # end if
                
                # define attributes for read element extracting length from command
                read_attributes = {'addr':  addr,
                                   'count': str(read_length(command)),
                                   'radix': str(radix)}        
                    
                # create the read element
                read = ET.SubElement(aardvark, 'i2c_read', read_attributes)             
            # end if
            
            # delay
            ET.SubElement(aardvark, 'sleep', delay_attributes)             
        # end if

    #end for        
    
    # convert XML file to modifiable string to beautify it
    text_string = ET.tostring(aardvark, encoding='utf8', method='xml')
    
    # insert line breaks before end of file tag
    file_string2 = text_string.replace('</aardvark>', '\n\n</aardvark>')
    
    # insert double new line before comments to creat blocks for each command
    file_string3 = file_string2.replace('<!', '\n\n<!')
    
    # insert new line between each set of XML tags
    file_string4 = file_string3.replace('><', '>\n\t<')
    
    # remove header
    file_string5 = file_string4.replace('<?xml version=\'1.0\' encoding=\'utf8\'?>\n', '')
    
    # open window for saving the file
    file_opt = options = {}
    options['defaultextension'] = '.xml'
    options['filetypes'] = [('xml files', '.xml')]
    options['initialdir'] = os.getcwd() + '\\xml_files'
    options['initialfile'] = 'aardvark_script.xml'
    options['title'] = 'Save .xml file as:'     
    
    filename_full = asksaveasfilename(**file_opt)
    
    if (filename_full != ''):    
        # open file for writing
        
        filename_short = filename_full.split('/')[-1]
        filename_dir = filename_full[:filename_full.rfind('/')]
        if (filename_short not in os.listdir(filename_dir)) or file_is_free(filename_full):         
            myfile = open(filename_full, 'w+')
            
            # write file
            myfile.write(file_string5)
            myfile.write('\n')
            
            # close file
            myfile.close()    
            
            print 'XML file \'' + filename_full.split('/')[-1] + '\' written'
        else:
            print '*** Requested XML file is open in another program ***'
    else:    
        print '*** No XML file written ***'
    # end if
    return filename_full
# end def
