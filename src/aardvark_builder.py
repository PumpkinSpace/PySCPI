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

def file_is_free(filename):
    try:
        os.rename(filename,filename)
        return True
    except OSError as e:
        return False
    # end
# end


def write_aardvark(exit_event, commands, dec_addr, Delay, Ascii_delay, float_dp, THREAD_EXIT):
    # configure Aardvark if available
    AA_Devices = aa_find_devices(1)
    Aardvark_free = True
    Aardvark_port = 8<<7
    if (AA_Devices[0] < 1):
        print '*** No Aardvark is present ***'
        Aardvark_free = False
    else:
        Aardvark_port = AA_Devices[1][0]
    # end
    
    if Aardvark_port >= 8<<7 and Aardvark_free:
        print '*** Aardvark is being used, disconnect other application or Aardvark device ***'
        aa_close(Aardvark_port)
        Aardvark_free = False
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
            # end
        # end
        
        if 'TEL?' in commands[i]:
            # if the Aardvark is free read from it
            if Aardvark_free:
                if commands[i].endswith('ascii'):
                    aa_sleep_ms(Ascii_delay)
                else:
                    aa_sleep_ms(Delay)
                # end
                data = array('B', [1]*read_length(commands[i])) 
                # read from the slave device
                read_data = aa_i2c_read(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                print_read(commands[i], list(read_data[1]), float_dp)
            # end  
        # end
        print ''
        aa_sleep_ms(Delay)
        
        # Iterate to next command
        i+=1
        if not exit_event.isSet():
            break
        # end
    # end loop
    
def log_aardvark(exit_event, commands, dec_addr, Delay, Ascii_delay, float_dp, logging_p, filename, output_text):
    # configure Aardvark if available
    
    csv_line = []
    output_writer = None
    csv_output = None
    # create CSV Header
    for command in commands:
        if 'TEL?' in command:
            if has_preamble(command):
                csv_line.append(command + ': Time (s)')
            #end
            print_format = SCPI_Data[command][1]
            if ',' not in print_format:
                csv_line.append(command + ': Data')
            else:
                for i in range(len(print_format.split(','))):
                    csv_line.append(command + ': Data[' + str(i) + ']')
                # end
            # end
        # end
    # end
    # write Header
    if file_is_free(filename):     
        csv_output = open(filename, 'wb')
        output_writer = csv.writer(csv_output, delimiter = ',')
        output_writer.writerow(csv_line) 
    else:
        print'*** Requested log file is in use by another program ***'
        return 0
    # end
    
    AA_Devices = aa_find_devices(1)
    Aardvark_free = True
    Aardvark_port = 8<<7
    if (AA_Devices[0] < 1):
        print '*** No Aardvark is present ***'
        Aardvark_free = False
        THREAD_EXIT = True
    else:
        Aardvark_port = AA_Devices[1][0]
    # end
    
    if Aardvark_port >= 8<<7 and Aardvark_free:
        print '*** Aardvark is being used, disconnect other application or Aardvark device ***'
        aa_close(Aardvark_port)
        Aardvark_free = False
        THREAD_EXIT = True
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

    csv_row = []
    start_time = time.time()
    while not exit_event.isSet():
        
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
                # end
            # end
            
            if 'TEL?' in commands[i]:
                # if the Aardvark is free read from it
                if Aardvark_free:
                    if commands[i].endswith('ascii'):
                        aa_sleep_ms(Ascii_delay)
                    else:
                        aa_sleep_ms(Delay)
                    # end
                    data = array('B', [1]*read_length(commands[i])) 
                    # read from the slave device
                    read_data = aa_i2c_read(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                    print_read(commands[i], list(read_data[1]), float_dp)
                    log_read(commands[i], list(read_data[1]), csv_row)
                    # write to log file              
                # end  
            # end
            print ''
            aa_sleep_ms(Delay)
            
            # Iterate to next command
            i+=1
        # end loop
        while (time.time() - start_time) < logging_p:
            continue
        # end
        start_time = time.time()
        output_writer.writerow(csv_row) 
        csv_row = []        
        output_text.config(state = NORMAL)
        output_text.delete('1.0', END)
        output_text.config(state=DISABLED)  
        
    # end loop
    csv_output.close()   

    if Aardvark_free:
        aa_close(Aardvark_port)
        print 'Aardvark communications finished'
    # end
# end

def create_XML(commands, addr, Delay, Ascii_delay, output_text):
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
                ET.SubElement(aardvark, 'sleep', ascii_delay_attributes)
            else:
                ET.SubElement(aardvark, 'sleep', delay_attributes)
            # end
            
            
            # define attributes for read element extracting length from command
            read_attributes = {'addr':  addr,
                               'count': str(read_length(commands[i])),
                               'radix': str(radix)}        
                
            # create the read element
            read = ET.SubElement(aardvark, 'i2c_read', read_attributes)             
        # end
        
        # Iterate to next command
        i+=1
    #end loop        
    
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
    
    file_opt = options = {}
    options['defaultextension'] = '.xml'
    options['filetypes'] = [('xml files', '.xml')]
    options['initialdir'] = os.getcwd() + '\\xml_files'
    options['initialfile'] = 'aardvark_script.xml'
    options['title'] = 'Save .xml file as:'     
    
    filename_full = asksaveasfilename(**file_opt)
    
    if (filename_full != ''):    
        # open file for writing
        
        if file_is_free(filename_full):
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
        output_text.config(state=NORMAL)
        output_text.delete('1.0', END)
        output_text.config(state=DISABLED)        
        print '*** No XML file written ***'
    # end
    
    return filename_full
# end

def write_I2C(commands, dec_addr, Delay, write_aardvark, create_XML, filename):
    if use_aardvark:
        write_aardvark(commands, dec_addr, Delay)
    # end
    if use_XML:
        create_XML(commands, address, Delay, filename)
    # end
# end


#write_I2C()
## Incase of error, write this in shell
# aa_close(Aardvark_port)

