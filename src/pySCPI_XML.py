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
__version__ = '0.3.8' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import tkFileDialog as TKFD 
import pySCPI_config
import xml.etree.ElementTree as ET
import pySCPI_formatting
import os
import pySCPI_aardvark


#
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
    gui.text_queue.put(None)
    
    # get the desired delay from the gui.
    delay_time = gui.get_delay()
    
    
    # get the desired ascii delay from the gui.
    ascii_time = gui.get_ascii_delay()
    
    
    # get the desired I2C address from the gui.
    addr = "0x%X" % gui.get_i2c_address()
    
    
    # get the list of commands from the gui
    command_list = gui.get_command_list()
    
    # wrap up the writing directives
    directives = pySCPI_config.write_directives(command_list, addr,
                                                delay_time, ascii_time)
            
    # create the xml file
    filename = create_XML(directives, gui)
    
    # update the filename display window to show the filename saved
    gui.update_filename(filename = filename)  
    
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
    
    # prepare to open a window to load a file through
    file_opt = options = {}
    options['defaultextension'] = '.xml'
    options['filetypes'] = [('xml files', '.xml')]
    options['initialdir'] = os.getcwd() + '/xml_files'
    options['title'] = 'Select .xml file to open' 
    
    # determine default directory to open
    dir_list = os.listdir(os.getcwd() + '/xml_files')
    
    # determine default file name to display
    if 'aardvark_script.xml' in dir_list or dir_list == []:
        # the default name is in the directory so use that
        options['initialfile'] = 'aardvark_script.xml'
        
    else:
        # use the name of the first file in the directory
        options['initialfile'] = dir_list[1]
    # end if
    
    # open window to fet filename to open
    filename = TKFD.askopenfilename(**file_opt)

    # define the values to read in
    commands = []
    ascii_delay = '0'
    delay = '0'
    first_address = '0'
    
    # define temporary variables
    last_address = '0'
    device_detected = ''
    previous_line = ''    
    
    # define boolean flags
    config_found = False
    first_bitrate = True
    ascii_last = False
    
    # determine if a file was actually selected
    if (filename != ''): 
        
        # a file was so extract open the file
        xml = open(filename, 'r')
        
        # split ithe XML into a list of lines
        xml_strip = [line.strip() for line in xml]
        
        # iterate through the lines
        for line in xml_strip:
            
            # determine what each file in the xml is
            if line.startswith('<!--'):
                # this is a comment that could conatin command information
                if config_found:
                    # all of the configuration comments have been found, 
                    # leaving only the command comments, 
                    # thus this is a command
                    
                    # strip out the command
                    command = line[4:-3]
                    
                    # append to the command list
                    commands = commands + [command]
                    
                    # see if device information can be extracted from it
                    if not (command.startswith('SUP') or \
                            command.startswith('<')):
                        # detect the device name
                        device_detected = command.split(':')[0]
                    # end if
                    
                else:
                    # line is the configuration command
                    config_found = True
                # end if
                
                # is it an ascii command
                ascii_last = ('ascii' in line)
                
            elif line.startswith('<sleep'):
                # delay found so strip out the delay
                temp_delay = [s for s in line.split('"') if s.isdigit()][0]
                
                if not ascii_last:
                    # not an ascii delay
                    
                    if ('sleep' not in previous_line) and (delay == '0'):
                        # the first standard delay so update the delay
                        delay = temp_delay  
                        
                    elif ('sleep' in previous_line):
                        # it is an additional delay
                        
                        # strip out the delay time
                        time = line.split('"')[1]
                        
                        # add the command
                        commands = commands + ['<DELAY ' + time + '>']                        
                    # end if
                    
                elif (ascii_delay == '0'):
                    # is the first ascii delay so strip out that delay
                    ascii_delay = line.split('"')[1]
                # end
                
            elif line.startswith('<i2c_write'):
                # command is a write command so find the address
                index = line.index('"')
                address = '0x' + line[index+3:index+5]
                
                if first_address == '0':
                    # this is the first address
                    first_address = address
                                        
                elif (address != last_address) and \
                     ('<READ' not in previous_line) and \
                     ('<WRITE' not in previous_line):
                    # an address change has happened
                
                    if commands[-1].startswith('<'):
                        # add the address change
                        commands = commands + ['<ADDRESS '+address+'>']
                        
                    else:
                        # needs to be added before the last command
                        commands.insert(-1,'<ADDRESS ' + address + '>')
                    # end if
                # end if   
                
                # store the last address
                last_address = address                    
            
            elif 'bitrate' in line:
                # the line is a bitrate setting line
                if first_bitrate:
                    # it is the default line so should be ignored
                    first_bitrate = False
                
                else:
                    # it is a change in bitrate so it should be processed
                    rate = line.split('"')[1]
                    commands = commands + ['<BITRATE ' + rate + '>']
                # end if
                
            elif ('configure' in line) and not first_bitrate:
                # it is not the first config command so it must be a change
                # in pullups
                
                # set of valid states
                states = ['<PULLUPS OFF>', '<PULLUPS ON>']
                
                # build the commands
                state = int(line.split('pullups="')[1][0])
                commands = commands + [states[state]]
            # end if
            
            # store the line
            previous_line = line
        # end if
        
        # update the filename display window to show the filename loaded   
        gui.update_filename(filename = filename)
        
        # wrap all the other elements to update in the gui
        new_fields = pySCPI_config.write_directives(commands, first_address,
                                                    delay, ascii_delay)
        
        # update the gui
        gui.update_fields(new_fields, device_detected)
        
        # close the xml file
        xml.close()
        
    else:
        # no file was loaded
        gui.text_queue.put(None)       
        gui.text_queue.put('*** No file given to Load ***')
    # end if
    
    # unlock buttons
    gui.action_lock('Unlock')
# end def

  
def update_gui_defaults(GUI_defaults):
    """ 
    Function to read in the default values for GUI parameters from XML
    
    @param[in/out] GUI_defaults:  Default values for a set of parameters 
                                  used to construct the gui. These values
                                  get modified by this fuction.
                                  (pySCPI_gui.gui_defaults)
    """
    # failure flag
    config_import_error = False
    
    # xml source directory
    src_dir = os.getcwd() + '\\src'
    
    # attempt to parse the xml file and get it's root
    try:
        tree = ET.parse(src_dir + '\\pySCPI_config.xml')
        root = tree.getroot()
        
    except (IOError, ET.ParseError):
        # parsing failed for some reason
        config_import_error = True
        GUI_defaults.log_error('*** pySCPI_config.xml is'
                               'missing or corrupt ***')
    # end try
    
    # import the default values from the xml file
    if not config_import_error:
        
        # list of tags to look for
        config_tags = ['default_filename', 'default_delay', 
                       'default_length', 'default_dp']
        
        # iterate through tags
        for tag in config_tags:
            # find each tag
            config_element = root.findall(tag)
            
            # if there is only one of a tag
            if len(config_element) == 1:
                # convert it to text
                config_text = config_element[0].text
                
                # update the appropriate field
                if tag == 'default_filename':
                    GUI_defaults.update_filename(config_text)
                
                elif tag == 'default_delay':
                    GUI_defaults.update_delay(config_text)
                    
                elif tag == 'default_length':
                    GUI_defaults.update_length(config_text)
                    
                elif tag == 'default_dp':
                    GUI_defaults.update_dp(config_text)
                # end if
                
            else:
                GUI_defaults.log_error('*** There is the wrong number '
                                       'of ' + tag + ' declarations in '
                                       'pySCPI_config.xml ***')   
            # end if
        # end for
              
        # find the default addresses
        address_elements = root.findall('addresses')
        
        # if there are addresses
        if (len(address_elements) == 1) and (len(address_elements[0]) > 0):
            for element in address_elements[0]:
                # add each address to the list
                GUI_defaults.add_address(element.tag, element.get('address'))
            # end for
            
        else:
            GUI_defaults.log_error('*** No addresses were provided in '
                                   'pySCPI_config.xml ***')  
        # end if
        
        # find the default commands
        command_elements = root.findall('default_commands')
        
        # if there are commands
        if (len(command_elements) == 1) and (len(command_elements[0]) > 0):
            for command in command_elements[0]:
                # add each command to the list
                GUI_defaults.add_command(command.text)
            # end for

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
    
    # failure flag
    config_import_error = False
    
    # xml source directory
    src_dir = os.getcwd() + '\\src'
    
    # try to parse the xml file and get it's root
    try:
        tree = ET.parse(src_dir + '\\SCPI_Commands.xml')
        root = tree.getroot()
        
    except (IOError, ET.ParseError):
        # parsing failed for some reason
        config_import_error = True
        SCPI_library.log_error('*** SCPI_Commands.xml is'
                               'missing or corrupt ***')
    # end try    
    
    # import the default values from the xml file
    if not config_import_error:  
        
        # find the scpi command size information
        size_elements = root.findall('sizes')
        
        # if the size information exists
        if (len(size_elements) == 1) and (len(size_elements[0]) > 0):
            for size in size_elements[0]: 
                SCPI_library.update_size(size.tag, size.text)
            # end for
        else:
            SCPI_library.log_error('*** No size configurations were found'
                                   ' in SCPI_Commands.xml **') 
        # end if
        
        # find all the commands
        command_list = root.findall('command')
        
        # if there are commands
        if len(command_list) > 0:
            # iterate through the commands
            for command in command_list:
                
                if ('name' in command.attrib) and \
                   ('data_length' in command.attrib) and \
                   ('data_format' in command.attrib):    
                    # all the required attributes exist so add the command
                    SCPI_library.add_command(command.get('name'),
                                            command.get('data_length'),
                                            command.get('data_format'))
                        
                else:
                    # the command is incorrectly defined in the xml
                    SCPI_library.log_error('*** A command has an '
                                           'invalid format in '
                                           'SCPI_Commands.xml ***')    
                # end if
            # end for
            
        else:
            # there are no commands
            SCPI_library.log_error('*** No commands were found in '
                                   ' SCPI_Commands.xml **') 
        # end if
    # end if
# end def
       
        
#
# ----------------
# Private Functions

def create_XML(directives, gui):
    """
    Write an Aardvark compatible .xml file that can be used with the 
    Total phase system or loaded back into pySCPI
    
    @param[in]  directives:  Instructions to direct the sending of 
                             data (pySCPI_config.write_directives)
    @param[in]  gui:           Instance of the gui that this function is 
                               called by (pySCPI_gui.main_gui).
    @return     filename_full: Absolute directory of the file created
    """     
    # unpack the directives
    commands = directives.command_list
    Delay = directives.delay_time
    Ascii_delay = directives.ascii_time    
    addr = directives.addr
    
    # Start XML
    aardvark = ET.Element('aardvark')
    
    # starup comment for historical reasons
    aardvark.append(ET.Comment('Configuration (Need pullups, ' + 
                               'not sure why...)'))    
    
    # Configuration Element
    config_attributes = {'i2c':     str(int(pySCPI_aardvark.I2C)),
                         'spi':     str(int(pySCPI_aardvark.SPI)),
                         'gpio':    str(int(pySCPI_aardvark.GPIO)),
                         'pullups': str(int(pySCPI_aardvark.Pullups))}
    
    ET.SubElement(aardvark, 'configure', config_attributes)
    
    # Bitrate
    rate_attributes = {'khz': str(pySCPI_aardvark.Bitrate)}
    
    ET.SubElement(aardvark, 'i2c_bitrate', rate_attributes)
    
    # Start I2C
    ET.SubElement(aardvark, 'i2c_free_bus')
    
    # delay attributes
    delay_attributes = {'ms': str(Delay)}    
    ascii_delay_attributes = {'ms': str(Ascii_delay)}  
    
    # delay
    ET.SubElement(aardvark, 'sleep', delay_attributes)    
    
    # iterate through commands
    for command in commands: 
        
        if pySCPI_config.is_config(command):
            # add the configuration to the XML
            addr = update_XML(command, addr, aardvark, gui.text_queue)
            
        elif pySCPI_config.is_valid_raw(command, gui.text_queue):
            # it is a valid raw command so comment the command
            aardvark.append(ET.Comment(command))
            
            # split the command up
            raw_list = command[:-1].split(' ')
            raw_addr = '0x' + raw_list[1][2:-1]
            
            # determine the type of raw command it is
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
                
                ET.SubElement(aardvark, 'i2c_read', 
                              read_attributes) 
            # end if
            
            # intermessage delay
            ET.SubElement(aardvark, 'sleep', delay_attributes)  
                              
        else:
            # this is a regular command so comment the SCPI command
            aardvark.append(ET.Comment(command))
            
            # define attributes for write element
            write_attributes = {'addr':  addr,
                                'count': str(len(command)+1),
                                'radix': str(pySCPI_aardvark.radix)}
            
            # create write element if it is not a comment
            if not command.startswith('#'):
                scpi = ET.SubElement(aardvark,'i2c_write',write_attributes)
                
                # add hexidecimal null terminated command as 
                # text to the write element
                scpi.text = ' '.join("{:02x}".format(ord(c)) for \
                                     c in command) + ' 0a'                  
            # end if
            
                  
            
            if ('TEL?' in command) and not command.startswith('#'):
                # Read command was issued so a read needs to be performed
                
                if command.endswith('ascii'):
                    # leave a longer delay for ascii commands
                    ET.SubElement(aardvark, 'sleep', 
                                  ascii_delay_attributes)
                    
                else:
                    # regular delay
                    ET.SubElement(aardvark, 'sleep', delay_attributes)
                # end if
                
                # extract length from command
                command_len = pySCPI_formatting.read_length(command, gui)          
                
                # define attributes for read element
                read_attributes = {'addr':  addr,
                                   'count': str(command_len),
                                   'radix': str(pySCPI_aardvark.radix)}        
                    
                # create the read element
                ET.SubElement(aardvark, 'i2c_read', read_attributes)             
            # end if
            
            # delay
            ET.SubElement(aardvark, 'sleep', delay_attributes)             
        # end if

    #end for        
    
    # beautify the xml
    file_string = beautify_xml(aardvark)
    
    # open window for saving the file
    file_opt = options = {}
    options['defaultextension'] = '.xml'
    options['filetypes'] = [('xml files', '.xml')]
    options['initialdir'] = os.getcwd() + '\\xml_files'
    options['initialfile'] = 'aardvark_script.xml'
    options['title'] = 'Save .xml file as:'     
    
    # get the file name from the user
    filename = TKFD.asksaveasfilename(**file_opt)
    
    # see if the user selected a file or not
    if (filename != ''):    
        # a file was selected so open file for writing
        
        if pySCPI_config.file_is_free(filename):         
            myfile = open(filename, 'w+')
            
            # write file
            myfile.write(file_string)
            myfile.write('\n')
            
            # close file
            myfile.close()    
            
            gui.text_queue.put('XML file \''+ filename.split('/')[-1]+'\' written')
            
        else:
            gui.text_queue.put('*** Requested XML file is open in another program ***')
            
    else:    
        # no file was selected
        gui.text_queue.put('*** No XML file written ***')
    # end if
    
    return filename
# end def


def beautify_xml(XML):
    """
    Function to improve the readability of the xml file produced.
    
    @param[in/out]    XML:     The XML element to beautify (ET.element).
    
    @return           (string) The beautiful xml string
    """
    # convert XML file to modifiable string to beautify it
    text_string = ET.tostring(XML, encoding='UTF-8', method='xml')
    
    # insert line breaks before end of file tag
    file_string = text_string.replace('</aardvark>', '\n\n</aardvark>')
    
    # insert double new line before comments to create
    # blocks for each command
    file_string = file_string.replace('<!', '\n\n<!')
    
    # insert new line between each set of XML tags
    file_string = file_string.replace('><', '>\n\t<')
    
    # remove header
    # file_string = file_string.replace('<?xml version=\'1.0\' encoding=\'utf8\'?>\n', '')   
    
    return file_string
# end def
    
    
def update_XML(command, address, XML, text_queue):
    """
    Save the configuration requested by a config command to XML
    
    @param[in]  command:         The configuration comamnd requested 
                                 (string).
    @param[in]  address:         The current I2C slave address in use 
                                 (int).
    @param[in]  XML:             The XML Element to add to (ET.Element).
    @param[out] text_queue:      The queue to write outpuit to (Queue).
    @return     (int)            The new I2C address to use 
                                 (potentially unchanged).
    """   
    # return value
    new_address = address
    
    # split command into list
    command_list = command.split(' ')
    command_arg = command_list[1][0:-1]
    
    # determine the appropriate action to take
    if (command_list[0] == '<DELAY') and command_arg.isdigit():
        # perform a millisecond delay
        ET.SubElement(XML, 'sleep', {'ms': str(command_arg)})
        
    elif (command_list[0] == '<ADDRESS') and (len(command_arg) == 4):
        if command_arg.startswith('0x') and \
         pySCPI_config.is_hex(command_arg[2:]):
            # this is a satisfatory new address
            new_address = command_arg     
        # end if
    
    elif (command_list[0] == '<BITRATE') and command_arg.isdigit():
        # is a good bitrate so change the bitrate
        rate_attributes = {'khz': str(command_arg)}
        ET.SubElement(XML, 'i2c_bitrate', rate_attributes)
        
        # sleep to allow the config to take effect
        ET.SubElement(XML, 'sleep', {'ms': '200'})                  
        
    elif (command_list[0] == '<BITRATE'):
        # check command
        if command == '<PULLUPS ON>':
            # turn pullups on
            config_attributes = {'i2c':     str(int(pySCPI_aardvark.I2C)),
                                 'spi':     str(int(pySCPI_aardvark.SPI)),
                                 'gpio':    str(int(pySCPI_aardvark.GPIO)),
                                 'pullups': '1'}
    
            ET.SubElement(XML, 'configure', config_attributes)
            
            # sleep to allow the config to take effect
            ET.SubElement(XML, 'sleep', {'ms': '200'})  
        
        elif command == '<PULLUPS OFF>':
            # turn pullups off
            config_attributes = {'i2c':     str(int(pySCPI_aardvark.I2C)),
                                 'spi':     str(int(pySCPI_aardvark.SPI)),
                                 'gpio':    str(int(pySCPI_aardvark.GPIO)),
                                 'pullups': '0'}
    
            ET.SubElement(XML, 'configure', config_attributes)
            
            # sleep to allow the config to take effect
            ET.SubElement(XML, 'sleep', {'ms': '200'})              
        
        else:
            text_queue.put('*** Invalid Pullup Command, use either '\
                  '<PULLUPS ON> or <PULLUPS OFF>')
        #end if  
        
    else:
        text_queue.put('*** The configuration command ' + command + 'requested is '\
              'not valid, refer to Read Me***')
    # end if  
    
    return new_address
# end def