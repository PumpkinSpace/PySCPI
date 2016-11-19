# Aardvark batch script writer
# Pumpkin Inc.
# David Wright 2016

import xml.etree.ElementTree as ET
import sys
from aardvark_py import *
from SCPI_formatting import *

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

#Filename to save as
filename = 'aardvark_script.xml'

# Intermessage delay in milliseconds
Delay = 300

# I2C address dictionary
address_of = {'PIM':        '0x53',
              'BM2':        '0x5C',
              'GPSRM':      '0x51',
              'SIM':        '0x54',
              'BIM':        '0x52',
              'BSM':        '0x58',
              # Non-SCPI Devices
              'CS EPS':     '0x2B',
              'ADCS CTRL':  '0x1F',
              'CS BAT':     '0x2A',
              'EXT_LIGHT':  '0x60',
              }
              
# Slave Address as text
address = address_of['PIM']
dec_addr = int(address,0)

########################## SCPI Commands #######################################
# commands is a list of SCPI Commands to be sent, TELEM requests will have all
# appropriate reading steps done following sending the command
#
# Example:
# commands = ['SUP:LED ON',
#             'SUP:TEL? 2,length'] 

commands = ['SUP:TEL? 0,name',
            'SUP:TEL? 0,length',
            'SUP:TEL? 0,data',
            'SUP:TEL? 0,ascii',
            ]
            
################################################################################

def write_aardvark(commands, dec_addr, Delay):
    # configure Aardvark if available
    AA_Devices = aa_find_devices(1)
    Aardvark_free = True
    Aardvark_port = 8<<7
    if (AA_Devices[0] < 1):
        print ' *** No Aardvark is present ***'
        Aardvark_free = False
    else:
        Aardvark_port = AA_Devices[1][0]
    # end
    
    if Aardvark_port >= 8<<7 and Aardvark_free:
        print ' *** Aardvark is being used, disconnect other application or Aardvark device ***'
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
            aa_sleep_ms(Delay)
            if 'TEL?' in commands[i]:
                print 'Read:\t\t' + commands[i]
            else:
                print 'Write:\t\t' + commands[i]
            # end
        # end
        
        if 'TEL?' in commands[i]:
            # if the Aardvark is free read from it
            if Aardvark_free:
                data = array('B', [1]*read_length(commands[i])) 
                # read from the slave device
                read_data = aa_i2c_read(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                print_read(commands[i], list(read_data[1]))
                aa_sleep_ms(Delay)
            # end  
        # end
        print ''
        
        # Iterate to next command
        i+=1
    # end loop

    if Aardvark_free:
        aa_close(Aardvark_port)
        print 'Aardvark communications finished'
    # end
# end

def create_XML(commands, addr, Delay, filename):
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
    
    i = 0
    while i < len(commands):    
        # delay after previous block
        ET.SubElement(aardvark, 'sleep', delay_attributes)
        
        # comment the string of the SCPI command
        aardvark.append(ET.Comment(commands[i]))
        
        # define attributes for write element
        write_attributes = {'addr':  address,
                            'count': str(len(commands[i])+1),
                            'radix': str(radix)}
        
        # create write element
        scpi = ET.SubElement(aardvark, 'i2c_write', write_attributes)
        
        # add hexidecimal null terminated command as text to the write element
        scpi.text = ' '.join("{:02x}".format(ord(c)) for c in commands[i]) + ' 0a'        
        
        if 'TEL?' in commands[i]:
            # Read command was issued so a read needs to be performed
            ET.SubElement(aardvark, 'sleep', delay_attributes)
            
            # define attributes for read element extracting length from command
            read_attributes = {'addr':  address,
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
    
    
    # open file for writing
    myfile = open(os.getcwd() + '\\xml_files\\' + filename, 'w+')
    
    # write file
    myfile.write(file_string5)
    myfile.write('\n')
    
    # close file
    myfile.close()    
    
    print 'XML file \'' + filename + '\' written'
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

