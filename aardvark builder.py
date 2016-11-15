# Aardvark batch script writer
# Pumpkin Inc.
# David Wright 2016

import xml.etree.ElementTree as ET

from aardvark_py import *
from SCPI_Commands import *

# Configure I2C (DO NOT MODIFY)
I2C = True
SPI = True
GPIO = False
Pullups = True
radix = 16

######################## User Defined Configuration ############################
# Bitrate in kHz
Bitrate = 100

#Filename to save as
filename = 'aardvark_script.xml'

# Intermessage delay in milliseconds
Delay = 100

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
# commands is a list of read/write commands and the SCPI command to read/write
# a command takes the form of a pair of list entries the read/write command
# taking the even entry in the list and the associated SCPI commad taking the 
# even entry.
# For a write command use the string 'WRITE' as the even item in the list and
# then use the string of the command as the odd item eg. 'SUP:LED ON'
# For a read command the even entry is a string 'READ ' followed by the number 
# of bytes to read, ie. to read 10 bytes it would be 'READ 10'. The odd entry is
# as before just the SCPI command string eg. 'SUP:TEL? 2,length'
#
#
# Example:
# commands = ['WRITE',    'SUP:LED ON',
#             'READ 21',  'SUP:TEL? 2,length'] 

commands = ['WRITE',     'PIM:PORT:POW ON,4',
            'READ 39',   'PIM:TEL? 1,data',
            'READ 39',   'PIM:TEL? 3,data',
            'READ 39',   'PIM:TEL? 4,data',
            ]
            
################################################################################

# Start XML
aardvark = ET.Element('aardvark')

aardvark.append(ET.Comment('Configuration (Need pullups, not sure why...)'))


# configure Aardvark if available
Aardvark_port = aa_find_devices(1)[1][0]
Aardvark_free = True
if Aardvark_port >= 8<<7:
    print ' *** Aardvark is being used ***'
    Aardvark_free = False
else:
    # Aardvark is available so configure it
    Aardvark_in_use = aa_open(Aardvark_port)
    aa_configure(Aardvark_in_use, AA_CONFIG_SPI_I2C)
    aa_i2c_pullup(Aardvark_in_use, AA_I2C_PULLUP_BOTH)
    aa_i2c_bitrate(Aardvark_in_use, Bitrate)
    aa_i2c_free_bus(Aardvark_in_use)
    aa_sleep_ms(Delay)    
    print "Starting Aardvark communications\n"
# end


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


# iterate through commands and add them to the aardvark file
i = 0
while i < len(commands):
    
    # delay after previous block
    ET.SubElement(aardvark, 'sleep', delay_attributes)
    
    # comment the string of the SCPI command
    aardvark.append(ET.Comment(commands[i+1]))
    
    # determine the type of command requested
    if ((commands[i] == 'WRITE') or (commands[i].startswith('READ'))):
        # Command is a valid write or read command
        
        # define attributes for write element
        write_attributes = {'addr':  address,
                            'count': str(len(commands[i+1])+1),
                            'radix': str(radix)}
        
        # create write element
        scpi = ET.SubElement(aardvark, 'i2c_write', write_attributes)
        
        # add hexidecimal null terminated command as text to the write element
        scpi.text = ' '.join("{:02x}".format(ord(c)) for c in commands[i+1]) + ' 0a'
        
        # See if the Aardvark is free
        if Aardvark_free:
            # Prepare the data for transmission
            write_data = list(commands[i+1])
            write_data = [ord(item) for item in write_data]
            write_data.append(0x0a)
            data = array('B', write_data)  
            # Write the data to the slave device
            aa_i2c_write(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
            aa_sleep_ms(Delay)
            if not (commands[i].startswith('READ')):
                print 'Write: ' + commands[i+1]
            else:
                print 'Read: ' + commands[i+1]
            # end
        # end
        
        if (commands[i].startswith('READ')):
            # Read command was issued so a read needs to be performed
            ET.SubElement(aardvark, 'sleep', delay_attributes)
            
            # define attributes for read element extracting length from command
            read_attributes = {'addr':  address,
                               'count': commands[i].split(' ')[1],
                               'radix': str(radix)}        
            
            # check the length of the command desired
            if int(read_attributes['count']) != read_length(commands[i+1]):
                aardvark.append(ET.Comment('*** requested length does not match that specified in dictionary ***'))
                print '*** requested length does not match that specified in dictionary ***'
            # end
            
            # create the read element
            read = ET.SubElement(aardvark, 'i2c_read', read_attributes) 
            
            # if the Aardvark is free read from it
            if Aardvark_free:
                data = array('B', [1]*read_length(commands[i+1])) 
                # read from the slave device
                read_data = aa_i2c_read(Aardvark_in_use, dec_addr, AA_I2C_NO_FLAGS, data)
                print_read(commands[i+1], list(read_data[1]))
                aa_sleep_ms(Delay)
            # end  
        # end
        print ''
    else:
        # command was not valid
        print('Error in read/write declaration')
    # end
    
    # Iterate to next command
    i+=2
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
myfile = open(filename, 'w+')

# write file
myfile.write(file_string5)
myfile.write('\n')

# close file
myfile.close()

if Aardvark_free:
    aa_close(Aardvark_port)
    print 'Aardvark communications finished and'
# end
print 'XML file \'' + filename + '\' written'

## Incase of error, write this in shell
# aa_close(Aardvark_port)