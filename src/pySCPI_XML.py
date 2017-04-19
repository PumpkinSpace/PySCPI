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
@package pySCPI_XML.py
Module to handle the XML aspects of pySCPI
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.0' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import tkFileDialog as TKFD 
import pySCPI_config
import pySCPI_aardvark
import platform
import threading
import xml.etree.ElementTree as ET
import pySCPI_formatting
import os


# ----------------
# Public Functions

def Write_XML(gui):
    """
    Function to start the process of saving the commands to xml.
    
    @param[in]  gui:          Instance of the gui that this function is 
                              called by (pySCPI_gui.main_gui).
    """    
    # lock buttons
    gui.action_lock('Lock', gui.save_button)
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
        gui.delay.delete(0,'end')
        gui.delay.insert(0, str(gui.defaults.default_delay))
    # end if
    
    # determine ascii delay
    ascii_text = gui.ascii.get()
    ascii_time = gui.defaults.default_delay*4;
    if ascii_text.isdigit():
        # delay is good
        ascii_time = int(ascii_text)
    else:
        print '*** Requested ascii delay is not valid, ' \
              'reverting to default ***'
        gui.ascii.delete(0,'end')
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
        print '*** Invlaid address entered, '\
              'reverting to device default ***'
        gui.addr_string = address_of(gui.slave_var.get())
        gui.addr_var.set(addr_string)
        gui.addr_num = int(addr_string,16)
    # end if
    
    # get command list
    input_string = gui.Command_text.get('1.0', 'end').encode('ascii', 'ignore')
    input_list = input_string.split('\n')
    command_list = []
    for item in input_list:
        # add allcommands to the list
        item = item.strip()
        if item != '':
            command_list = command_list + [item]
        # end if
    # end for
            
    # create the xml file
    filename = create_XML(command_list, addr_string, delay_time, 
                          ascii_time, gui)
    
    # update the filename display window to show the filename saved
    gui.file_window.config(state='normal')
    gui.file_window.delete('1.0', 'end')
    gui.file_window.insert('insert', filename.split('/')[-1])
    gui.file_window.config(state = 'disabled')
    gui.file_window.tag_configure('center', justify = 'center')
    gui.file_window.tag_add('center', '1.0', 'end')     
    
    # unlock the buttons
    gui.action_lock('Unlock')
# end def



def Load_XML(gui):
    """
    Function to load a command set, delays and address from a saved 
    xml file
    
    @param[in]  gui:          Instance of the gui that this function is 
                              called by (pySCPI_gui.main_gui).
    """     
    # lock the buttons
    gui.action_lock('Lock', gui.xml_button)   
    
    # prepare to open a windo to load a file through
    file_opt = options = {}
    options['defaultextension'] = '.xml'
    options['filetypes'] = [('xml files', '.xml')]
    options['initialdir'] = os.getcwd() + '/xml_files'
    dir_list = os.listdir(os.getcwd() + '/xml_files')
    # determine default file name to display
    if 'aardvark_script.xml' in dir_list or dir_list == []:
        options['initialfile'] = 'aardvark_script.xml'
    else:
        options['initialfile'] = dir_list[1]
    # end if
    options['title'] = 'Select .xml file to open'   
    
    # open window
    filename = TKFD.askopenfilename(**file_opt)

    commands = []
    config_found = False
    ascii_last = 0
    ascii_delay = '0'
    message_delay = '0'
    device_detected = ''
    previous_line = ''
    printed = False
    first_address = True
    last_address = '0'
    first_bitrate = True
    first_config = True
    
    if (filename != ''): 
        # extract all commands from the XML
        xml = open(filename, 'r')
        xml_strip = [line.strip() for line in xml]
        for line in xml_strip:
            # determine what each file in the xml is
            if line.startswith('<!--'):
                if config_found:
                    # line is a command
                    command = line[4:-3]
                    commands = commands + [command]
                    if not command.startswith('SUP'):
                        # detect the device name
                        device_detected = command.split(':')[0]
                    # end if
                else:
                    # line is the configuration command
                    config_found = True
                # end if
                
                # is it an ascii command
                if ('ascii' in line):
                    ascii_last = 1
                else:
                    ascii_last = 0
                # end if
                
            elif line.startswith('<sleep'):
                # delay found
                slices = [s for s in line.split('"') if s.isdigit()]
                if (ascii_last == 0):
                    # not an ascii delay
                    if 'sleep' not in previous_line:
                        # a standard delay
                        gui.delay.delete(0,'end')
                        message_delay = slices[0]
                        gui.delay.insert(0, message_delay)    
                        
                    else:
                        time = line.split('"')[1]
                        commands = commands + ['<DELAY ' + time + '>']                        
                    # end if
                else:
                    # is an ascii delay
                    ascii_delay = slices[0]
                # end
            elif line.startswith('<i2c_write'):
                # finding address
                index = line.index('"')
                address = '0x' + line[index+3:index+5]
                
                if first_address == True:
                    gui.addr_var.set(address)
                    
                    # create local address dictionary to compare to
                    local_address_of = gui.defaults.address_of.copy()
                    local_address_of['GPS'] = '0x51'
                    
                    if device_detected in local_address_of.keys():
                        if address == local_address_of[device_detected]:
                            # address matches a device
                            if device_detected == 'GPS':
                                gui.slave_var.set('GPSRM')
                            else:
                                gui.slave_var.set(device_detected)
                            # end if
                        else:
                            # address does not so color it yellow as a warning
                            gui.addr_text.config(background = 'yellow') 
                            if not printed:
                                print '*** Warning, loaded device address '\
                                      'does not match a device default ***'
                                printed = True
                            # end if
                        # end if  
                    else:
                        if address in gui.defaults.address_of.values():
                            # address matches a device
                            gui.slave_var.set(gui.defaults.address_of.keys()[gui.defaults.address_of.values().index(address)])
                        else:
                            # address does not so color it yellow as a warning
                            gui.addr_text.config(background = 'yellow') 
                            if not printed:
                                print '*** Warning, loaded device address '\
                                      'does not match a device default ***'
                                printed = True
                            # end if
                        # end if
                    # end if
                    first_address = False
                    last_address = address
                    
                else:
                    if (address != last_address) and \
                       ('<READ' not in previous_line) and \
                       ('<WRITE' not in previous_line):
                        # an address change has happened
                        if commands[-1].startswith('<'):
                            commands = commands + ['<ADDRESS '+address+'>']
                            
                        else:
                            # needs to be added before the last command
                            commands.insert(-1,'<ADDRESS ' + address + '>')
                        # end if
                        last_address = address
                    # end if
                # end if
            
            elif 'bitrate' in line:
                # the line is a bitrate setting line
                if first_bitrate == True:
                    # it is the default line so should be ignored
                    first_bitrate = False
                
                else:
                    # it is a change in bitrate so it should be processed
                    rate = line.split('"')[1]
                    commands = commands + ['<BITRATE ' + rate + '>']
                # end if
                
            elif 'configure' in line:
                # the line is a config line
                if first_config == True:
                    # it is the default line so should be ignored
                    first_config = False
                
                else:
                    # it is a change in pullups so it should be processed
                    states = ['<PULLUPS OFF>', '<PULLUPS ON>']
                    state = int(line.split('pullups="')[1][0])
                    commands = commands + [states[state]]
                # end if                
            # end if
            previous_line = line
        # end if
        
        
        if (ascii_delay == '0') or (ascii_delay == message_delay):
            # if ascii delay is too short, go to the default delay
            ascii_delay = 4*int(message_delay)
        # end if
        gui.ascii.delete(0,'end')
        gui.ascii.insert(0, ascii_delay)    
        
        # update the filename display window to show the filename loaded   
        gui.file_window.config(state = 'normal')
        gui.file_window.delete('1.0', 'end')
        gui.file_window.insert('insert', filename.split('/')[-1])
        gui.file_window.config(state = 'disabled')
        gui.file_window.tag_configure('center', justify = 'center')
        gui.file_window.tag_add('center', '1.0', 'end')    
        
        
        # empty command box and add new commands
        gui.Command_text.delete('1.0', 'end')
        gui.Command_text.insert('insert', '\n'.join(commands))
        xml.close()
    else:
        gui.output_text.config(state='normal')
        gui.output_text.delete('1.0', 'end')
        gui.output_text.config(state='disabled')        
        print '*** No file given to Load ***'
    # end if
    
    # unlock buttons
    gui.action_lock('Unlock')
# end def



def update_XML(command, address, XML):
    """
    Save the configuration requested by a config command to XML
    
    @param[in]  command:         The configuration comamnd requested 
                                 (string).
    @param[in]  address:         The current I2C slave address in use 
                                 (int).
    @param[in]  XML:             The XML Element to add to (ET.Element).
    @return     (int)            The new I2C address to use 
                                 (potentially unchanged).
    """    
    new_address = address
    # determine the appropriate action to take
    if 'DELAY ' in command:
        # strip out the number
        delay_list = command.split(' ')
        delay_number = delay_list[1][0:-1]
        # verify that it is a number and that the 
        # beginning of the command was correct
        if delay_number.isdigit() and (delay_list[0] == '<DELAY'):
            # perform a millisecond delay
            delay_attributes = {'ms': str(delay_number)} 
            ET.SubElement(XML, 'sleep', delay_attributes)
        else:
            # the delay is not valid
            print '*** The requested DELAY command is not valid. '\
                  'Use <DELAY x>***'
        # end if
             
    elif 'ADDRESS ' in command:
        # strip out the number
        address_list = command.split(' ')
        address_hex = address_list[1][0:-1]
        # verify that it is a number and that the 
        # beginning of the command was correct
        if address_hex.startswith('0x') and (len(address_hex) == 4) and \
           pySCPI_config.is_hex(address_hex[2:]) and \
           (address_list[0] == '<ADDRESS'):
            # is a good address
            new_address = address_hex
        else:
            # the adderss is invlaid
            print '*** The requested ADDRESS command is not valid.'\
                  'Use <ADDRESS 0xYY>***'
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
            print '*** The requested BITRATE command is not valid. '\
                  'Use <BITRATE x>***'
        # end if         
        
    elif 'PULLUPS ' in command:
        # check command
        if command == '<PULLUPS ON>':
            # turn pullups on
            config_attributes = {'i2c':     str(int(pySCPI_aardvark.I2C)),
                                 'spi':     str(int(pySCPI_aardvark.SPI)),
                                 'gpio':    str(int(pySCPI_aardvark.GPIO)),
                                 'pullups': '1'}
    
            config = ET.SubElement(XML, 'configure', config_attributes)
            
            delay_attributes = {'ms': '200'} 
            ET.SubElement(XML, 'sleep', delay_attributes)  
        
        elif command == '<PULLUPS OFF>':
            # turn pullups off
            config_attributes = {'i2c':     str(int(pySCPI_aardvark.I2C)),
                                 'spi':     str(int(pySCPI_aardvark.SPI)),
                                 'gpio':    str(int(pySCPI_aardvark.GPIO)),
                                 'pullups': '0'}
    
            config = ET.SubElement(XML, 'configure', config_attributes)
            
            delay_attributes = {'ms': '200'} 
            ET.SubElement(XML, 'sleep', delay_attributes)              
        
        else:
            print '*** Invalid Pullup Command, use either '\
                  '<PULLUPS ON> or <PULLUPS OFF>'
        #end if  
        
    else:
        print '*** The configuration command requested in not valid, '\
              'refer to Read Me***'
    # end if  
    
    return new_address
# end def

  
def create_XML(commands, address, Delay, Ascii_delay, gui):
    """
    Write an Aardvark compatible .xml file that can be used with the 
    Total phase system or loaded back into pySCPI
    
    @param[in]  commands:      List of commands to be sent 
                               (list of strings).
    @param[in]  addr:          I2C address of the slave device (string).
    @param[in]  Delay:         Millisecond delay to wait between 
                               transmissions (int).
    @param[in]  Ascii_delay:   Millisecond delay to wait before reading an 
                               'ascii' request (int).
    @param[in]  gui:           Instance of the gui that this function is 
                               called by (pySCPI_gui.main_gui).
    @return     filename_full: Absolute directory of the file created
    """     
    addr = address
    # Start XML
    aardvark = ET.Element('aardvark')
    
    aardvark.append(ET.Comment('Configuration (Need pullups, not sure why...)'))    
    
    # Configuration Element
    config_attributes = {'i2c':     str(int(pySCPI_aardvark.I2C)),
                         'spi':     str(int(pySCPI_aardvark.SPI)),
                         'gpio':    str(int(pySCPI_aardvark.GPIO)),
                         'pullups': str(int(pySCPI_aardvark.Pullups))}
    
    config = ET.SubElement(aardvark, 'configure', config_attributes)
    
    # Bitrate
    rate_attributes = {'khz': str(pySCPI_aardvark.Bitrate)}
    
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
        
        if pySCPI_config.is_config(command):
            # add the configuration to the XML
            addr = update_XML(command, addr, aardvark)
            
        elif pySCPI_config.is_raw_write(command) or \
             pySCPI_config.is_raw_read(command):
            if pySCPI_config.is_valid_raw(command):
                aardvark.append(ET.Comment(command))
                raw_list = command[:-1].split(' ')
                raw_addr = '0x' + raw_list[1][2:-1]
                if pySCPI_config.is_raw_write(command):
                    write_attributes = {'addr':  raw_addr,
                                        'count': str(len(raw_list)-1),
                                        'radix': str(pySCPI_aardvark.radix)}
                    raw = ET.SubElement(aardvark, 'i2c_write',
                                        write_attributes)
                    
                    # add hexidecimal null terminated command as 
                    # text to the write element
                    raw.text = ' '.join("{:02x}".format(int(c, 16)) for \
                                        c in raw_list[2:]) + ' 0a'
                    
                else:
                    read_attributes = {'addr':  raw_addr,
                                       'count': raw_list[2],
                                       'radix': str(pySCPI_aardvark.radix)}     
                    
                    read = ET.SubElement(aardvark, 'i2c_read', 
                                         read_attributes) 
                # end if
                ET.SubElement(aardvark, 'sleep', delay_attributes)  
                
            else:
                if 'READ' in command:
                    print '*** Invalid READ command, please refer to the'\
                          'Read me for proper syntax ***'
                    
                else:
                    print '*** Invalid WRITE command, please refer to the'\
                          'Read me for proper syntax ***'
                # end if
            # end if        
                    
        else:
            
            # comment the string of the SCPI command
            aardvark.append(ET.Comment(command))
            
            # define attributes for write element
            write_attributes = {'addr':  addr,
                                'count': str(len(command)+1),
                                'radix': str(pySCPI_aardvark.radix)}
            
            # create write element
            scpi = ET.SubElement(aardvark, 'i2c_write', write_attributes)
            
            # add hexidecimal null terminated command as 
            # text to the write element
            scpi.text = ' '.join("{:02x}".format(ord(c)) for \
                                 c in command) + ' 0a'        
            
            if 'TEL?' in command:
                # Read command was issued so a read needs to be performed
                
                if command.endswith('ascii'):
                    # leave a longer delay for ascii commands
                    ET.SubElement(aardvark, 'sleep', 
                                  ascii_delay_attributes)
                else:
                    ET.SubElement(aardvark, 'sleep', delay_attributes)
                # end if
                
                # define attributes for read element extracting 
                # length from command
                read_attributes = {'addr':  addr,
                                   'count': str(pySCPI_formatting.read_length(command, gui)),
                                   'radix': str(pySCPI_aardvark.radix)}        
                    
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
    
    # insert double new line before comments to create
    # blocks for each command
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
    
    filename_full = TKFD.asksaveasfilename(**file_opt)
    
    if (filename_full != ''):    
        # open file for writing
        
        filename_short = filename_full.split('/')[-1]
        filename_dir = filename_full[:filename_full.rfind('/')]
        if (filename_short not in os.listdir(filename_dir)) or \
           pySCPI_config.file_is_free(filename_full):         
            myfile = open(filename_full, 'w+')
            
            # write file
            myfile.write(file_string5)
            myfile.write('\n')
            
            # close file
            myfile.close()    
            
            print 'XML file \''+ filename_full.split('/')[-1]+'\' written'
        else:
            print '*** Requested XML file is open in another program ***'
    else:    
        print '*** No XML file written ***'
    # end if
    return filename_full
# end def


def update_gui_defaults(GUI_defaults):
    """ 
    Function to read in the default values for GUI parameters from XML
    
    @param[in/out] GUI_defaults:  Default values for a set of parameters 
                                  used to construct the gui. These values
                                  get modified by this fuction.
                                  (pySCPI_gui.gui_defaults)
    """
    config_import_error = False
    src_dir = os.getcwd() + '\\src'
    
    try:
        tree = ET.parse(src_dir + '\\pySCPI_config.xml')
        root = tree.getroot()
    except (IOError, ET.ParseError) as err:
        print (err)
        config_import_error = True
        GUI_defaults.log_error('*** pySCPI_config.xml is'
                               'missing or corrupt ***')
    # end try
    
    # import the default values from the xml file
    if not config_import_error:
        ### find the default filename ###
        filename_element = root.findall('default_filename')
        if len(filename_element) == 1:
            # there is default_filename present
            filename_text = filename_element[0].text
            GUI_defaults.update_filename(filename_text)
        else:
            GUI_defaults.log_error('*** There is the wrong number of '
                                   'default_filename declarations in '
                                   'pySCPI_config.xml ***')
        # end if
        
        ### find the default delay ###
        delay_element = root.findall('default_delay')
        if len(delay_element) == 1:
            # there is default_filename present
            delay_text = delay_element[0].text
            GUI_defaults.update_delay(delay_text)
            # end if
        else:
            GUI_defaults.log_error('*** There is the wrong number of '
                                   'default_delay declarations in '
                                   'pySCPI_config.xml ***')
        # end if
                
        ### find the default length ###
        length_element = root.findall('default_length')
        if len(length_element) == 1:
            # there is default_filename present
            length_text = length_element[0].text
            GUI_defaults.update_length(length_text)
        else:
            GUI_defaults.log_error('*** There is the wrong number of '
                                   'default_length declarations in '
                                   'pySCPI_config.xml ***')
        # end if    
        
        ### find the default dp ###
        dp_element = root.findall('default_dp')
        if len(dp_element) == 1:
            # there is default_filename present
            dp_text = dp_element[0].text
            GUI_defaults.update_dp(dp_text)
        else:
            GUI_defaults.log_error('*** There is the wrong number of '
                                   'default_dp declarations in '
                                   'pySCPI_config.xml ***')
        # end if     
        
        ### find the default addresses ###
        address_elements = root.findall('addresses')
        first_element = True
        if len(address_elements) == 1:
            for element in address_elements[0]:
                if first_element:
                    GUI_defaults.add_first_address(element.tag, 
                                                   element.get('address'))
                    first_element = False
                else:
                    GUI_defaults.add_address(element.tag, 
                                             element.get('address'))
                # endif
            # end for
            if first_element:
                # there were no addresses
                GUI_defaults.log_error('*** No addresses were provided in '
                                       'pySCPI_config.xml ***')  
            # end if
        else:
            GUI_defaults.log_error('*** No addresses were provided in '
                                   'pySCPI_config.xml ***')  
        # end if
        
        
        ### find the default commands
        command_elements = root.findall('default_commands')
        first_element = True
        if len(command_elements) == 1:
            for command in command_elements[0]:
                if first_element:
                    GUI_defaults.add_first_command(command.text)
                    first_element = False
                else:
                    GUI_defaults.add_command(command.text)
                # end if
            # end for
            if first_element:
                # no commands were found
                GUI_defaults.log_error('*** No commands were provided in '
                                                   'pySCPI_config.xml ***')                
            
        else:
            GUI_defaults.log_error('*** No commands were provided in '
                                   'pySCPI_config.xml ***')  
        # end if        
    # end if
# end def

def update_commands(SCPI_library):
    """
    Function to import updated SCPI library information from XML.
    
    @param[in/out] SCPI_library:  The library of supported scpi commands.
                                  The entries in this library are modified
                                  by this function. 
                                  (pySCPI_config.command_library)
    """
    config_import_error = False
    src_dir = os.getcwd() + '\\src'
    
    try:
        tree = ET.parse(src_dir + '\\SCPI_Commands.xml')
        root = tree.getroot()
    except (IOError, ET.ParseError) as err:
        print (err)
        config_import_error = True
        SCPI_library.log_error('*** SCPI_Commands.xml is'
                               'missing or corrupt ***')
    # end try    
    
    # import the default values from the xml file
    if not config_import_error:  
        
        # find the scpi command size information
        size_elements = root.findall('sizes')
        if len(size_elements) == 1:
            for size in size_elements[0]: 
                if size.tag == 'name_size':
                    SCPI_library.update_name_size(size.text)
                    
                elif size.tag == 'checksum_size':
                    SCPI_library.update_checksum_size(size.text)
                    
                elif size.tag == 'wflag_size':
                    SCPI_library.update_writeflag_size(size.text)
                    
                elif size.tag == 'time_size':
                    SCPI_library.update_timestamp_size(size.text)
                    
                elif size.tag == 'length_size':
                    SCPI_library.update_length_size(size.text)
                    
                elif size.tag == 'ascii_size':
                    SCPI_library.update_ascii_size(size.text)
                    
                else:
                    SCPI_library.log_error('*** ' + size.tag + ' is not a '
                                           'recognised size config **')
                # end if
            # end for
        else:
            SCPI_library.log_error('*** No size configurations were found'
                                   ' in SCPI_Commands.xml **') 
        # end if
        
        first_command = True
        command_list = root.findall('command')
        if len(command_list) > 0:
            for command in command_list:
                if ('name' in command.attrib) and \
                   ('data_length' in command.attrib) and \
                   ('data_format' in command.attrib):                
                    if first_command:
                        SCPI_library.add_first_command(command.get('name'),
                                                      command.get('data_length'),
                                                      command.get('data_format'))
                        first_command = False
                    else:
                        SCPI_library.add_command(command.get('name'),
                                                command.get('data_length'),
                                                command.get('data_format'))
                    # end if
                else:
                    SCPI_library.log_error('*** A command has an '
                                           'invalid format in '
                                           'SCPI_Commands.xml ***')    
                # end if
            # end for
            
            if first_command:
                SCPI_library.log_error('*** No commands were found in '
                                       ' SCPI_Commands.xml **') 
            # end if
        else:
            SCPI_library.log_error('*** No commands were found in '
                                   ' SCPI_Commands.xml **') 
        # end if
    # end if
# end def
        
