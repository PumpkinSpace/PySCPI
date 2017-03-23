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
def write_aardvark(exit_event, commands, dec_addr, Delay, Ascii_delay, float_dp):
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
    i = 0
    while i < len(commands):
    
        # See if the Aardvark is free
        if Aardvark_free:
            # Prepare the data for transmission
            write_data = list(commands[i])
            write_data = [ord(item) for item in write_data]
            write_data.append(0x0a)
            data = array('B', write_data)  
            # Write the data to the slave device
            aa_i2c_write(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
            if 'TEL?' in commands[i]:
                print 'Read:\t\t' + commands[i]
            else:
                print 'Write:\t\t' + commands[i]
            # end if
        # end if
        
        if 'TEL?' in commands[i]:
            # an I2C read has been requested
            # if the Aardvark is free read from it
            if Aardvark_free:
                if commands[i].endswith('ascii'):
                    # sleep a different amount if ascii was requested
                    aa_sleep_ms(Ascii_delay)
                else:
                    aa_sleep_ms(Delay)
                # end if
                
                # read from the slave device
                data = array('B', [1]*read_length(commands[i])) 
                read_data = aa_i2c_read(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                
                # print the recieved data
                print_read(commands[i], list(read_data[1]), float_dp)
            # end if
        # end if
        print ''
        aa_sleep_ms(Delay)
        
        # Iterate to next command
        i+=1
        
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
def log_aardvark(exit_event, commands, dec_addr, Delay, Ascii_delay, float_dp, logging_p, filename, output_text):

    csv_line = []
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
        
        # iterate through commands and add them to the aardvark file
        i = 0
        while i < len(commands):
        
            # See if the Aardvark is free
            if Aardvark_free:
                # Prepare the data for transmission
                write_data = list(commands[i])
                write_data = [ord(item) for item in write_data]
                write_data.append(0x0a)
                data = array('B', write_data)  
                # Write the data to the slave device
                aa_i2c_write(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                if 'TEL?' in commands[i]:
                    print 'Read:\t\t' + commands[i]
                else:
                    print 'Write:\t\t' + commands[i]
                # end if
            # end if
            
            if 'TEL?' in commands[i]:
                # if the Aardvark is free read from it
                if Aardvark_free:
                    if commands[i].endswith('ascii'):
                        aa_sleep_ms(Ascii_delay)
                    else:
                        aa_sleep_ms(Delay)
                    # end if
                    
                    # read from the slave device
                    data = array('B', [1]*read_length(commands[i])) 
                    read_data = aa_i2c_read(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                    
                    # print data
                    print_read(commands[i], list(read_data[1]), float_dp)
                    
                    # log data
                    log_read(commands[i], list(read_data[1]), csv_row)
                    # write to log file              
                # end if
            # end if
            print ''
            aa_sleep_ms(Delay)
            
            # Iterate to next command
            i+=1
        # end while
        
        while (time.time() - start_time) < logging_p:
            # delay to maintain the logging period
            time.sleep(0.1)
            if exit_event.isSet():
                break
        # end if
        # end while
        
        start_time = time.time()
        
        # write to log file
        output_writer.writerow(csv_row) 
                
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
Write an Aardvark compatible .xml file that can be used with the Total phase 
system or loaded back into pySCPI

@param[in]  commands:      List of commands to be sent (list of strings).
@param[in]  addr:          I2C address of the slave device (string).
@param[in]  Delay:         Millisecond delay to wait between transmissions (int).
@param[in]  Ascii_delay:   Millisecond delay to wait before reading an 'ascii' 
                           request (int).
@return     filename_full: Absolute directory of the file created
"""   
def create_XML(commands, addr, Delay, Ascii_delay):
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
    
    # iterate through commands
    i = 0
    while i < len(commands):    
        # delay after previous block
        ET.SubElement(aardvark, 'sleep', delay_attributes)
        
        # comment the string of the SCPI command
        aardvark.append(ET.Comment(commands[i]))
        
        # define attributes for write element
        write_attributes = {'addr':  addr,
                            'count': str(len(commands[i])+1),
                            'radix': str(radix)}
        
        # create write element
        scpi = ET.SubElement(aardvark, 'i2c_write', write_attributes)
        
        # add hexidecimal null terminated command as text to the write element
        scpi.text = ' '.join("{:02x}".format(ord(c)) for c in commands[i]) + ' 0a'        
        
        if 'TEL?' in commands[i]:
            # Read command was issued so a read needs to be performed
            
            if commands[i].endswith('ascii'):
                # leave a longer delay for ascii commands
                ET.SubElement(aardvark, 'sleep', ascii_delay_attributes)
            else:
                ET.SubElement(aardvark, 'sleep', delay_attributes)
            # end if
            
            # define attributes for read element extracting length from command
            read_attributes = {'addr':  addr,
                               'count': str(read_length(commands[i])),
                               'radix': str(radix)}        
                
            # create the read element
            read = ET.SubElement(aardvark, 'i2c_read', read_attributes)             
        # end if
        
        # Iterate to next command
        i+=1
    #end while        
    
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
