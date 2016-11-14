# Aardvark batch script writer
# Pumpkin Inc.
# David Wright 2016

import xml.etree.ElementTree as ET

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

# Intermessage delay in miliseconds
Delay = 200

# Slave Address as text
address = '0x53'

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

commands = ['WRITE',    'SUP:LED ON',
            'READ 21',  'SUP:TEL? 2,length'] 

################################################################################

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
        
        # add hexidecimal null termianted command as text to the write element
        scpi.text = ' '.join("{:02x}".format(ord(c)) for c in commands[i+1]) + ' 0a'
        
        if (commands[i].startswith('READ')):
            # Read command was issued so a read needs to be perfromed
            
            # define attributes for read element extracting length from command
            read_attributes = {'addr':  address,
                               'count': commands[i].split(' ')[1],
                               'radix': str(radix)}        
            
            # create the read element
            read = ET.SubElement(aardvark, 'i2c_read', read_attributes) 
    else:
        # command was not valid
        print('Error in read/write declaration')
        
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