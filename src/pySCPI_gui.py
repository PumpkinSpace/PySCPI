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
@package pySCPI_gui.py
Module to handle the creation and management of the pySCPI GUI
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.0' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import Tkinter as TK
import ttk
import pySCPI_aardvark
import pySCPI_config    
import platform
import pySCPI_XML
from functools import partial
from PIL import Image, ImageTk


# ---------
# Constants
################################ GUI defaults #############################
default_color = '#E1E5E7'
title_font = "Arial 16 bold"
label_font = "Arial 10"
button_font = "Arial 10 bold"
text_font = "Arial 9"
                   
root_width = 1000
root_height = 600

# ---------
# Classes
class gui_defaults:
    """
    Class containing all of the defalut values used to build the pySCPI GUI
    """
    
    def __init__(self):
        """
        Initialise the GUI_delault attributes to default values
        """
        # The default filename to save to and load from
        self.default_filename = 'aardvark_script.xml'
        
        # The default intermessage delay to use
        self.default_delay = 200
        
        # The default data length to read if a command is not recognised
        self.default_length = 16
        
        # The default number of decimal places to display for a float
        self.default_dp = 4
        
        # The default addresses of supported modules
        self.address_of = {'PIM':        '0x53',
                           'BM2':        '0x5C',
                           'GPSRM':      '0x51',
                           'SIM':        '0x50',
                           'BIM':        '0x52',
                           'BSM':        '0x58',
                           # Non-SCPI Devices
                           'CS EPS':     '0x2B',
                           'ADCS CTRL':  '0x1F',
                           'CS BAT':     '0x2A',
                           'EXT_LIGHT':  '0x60',
                           }
        
        # The default commands to display in the command window
        self.default_commands = ['SUP:TEL? 0,name',
                                 'SUP:TEL? 0,length',
                                 'SUP:TEL? 0,data',
                                 'SUP:TEL? 0,ascii',
                                 ]
        
        # list of errors thrown during the importing of the XML file
        self.error_log = []
        
        # flags to track adding commands and addresses
        self.no_commands = True
        self.no_addresses = True
    # end def
    
    
    def update_filename(self, new_filename):
        """ 
        Update the default filename to a new filename
        
        @param[in]  new_filename:  The new default setting (string).
        """
        if new_filename.endswith('.xml'):
            self.default_filename = new_filename
        else:
            self.error_log.append('*** Invalid default '
                                  'filename in xml file ***')
        # end if  
    # end def
    
    
    def update_delay(self, new_delay):
        """ 
        Update the default delay to a new value
        
        @param[in]  new_delay:  The new default setting (string).
        """ 
        if new_delay.isdigit():
            if int(new_delay) > 0:
                self.default_delay = int(new_delay)
            else:
                self.error_log.append('*** Invalid default '
                                      'delay in xml file ***')     
            # end if
        else:
            self.error_log.append('*** Invalid default '
                                  'delay in xml file ***')
        # end if  
    # end def   
    
    
    def update_length(self, new_length):
        """ 
        Update the default length to a new value
        
        @param[in]  new_length:  The new default setting (string).
        """ 
        if new_length.isdigit():
            if int(new_length) > 0:
                self.default_length = int(new_length)
            else:
                self.error_log.append('*** Invalid default '
                                      'length in xml file ***')  
            # end if
        else:
            self.error_log.append('*** Invalid default '
                                  'length in xml file ***')
        # end if  
    # end def      
    
    
    def update_dp(self, new_dp):
        """ 
        Update the default number of decimal places to a new value
        
        @param[in]  new_dp:  The new default setting (string).
        """ 
        if new_dp.isdigit():
            if int(new_dp) > 0:
                self.default_dp = int(new_dp)
            else:
                self.error_log.append('*** Invalid default number of '
                                      'decimal places in xml file ***')                
        else:
            self.error_log.append('*** Invalid default number of '
                                  'decimal places in xml file ***')
        # end if  
    # end def 
    
    
    def add_address(self, new_module, new_address):
        """ 
        Add the new module to the dictionary of addresses
        
        @param[in]  new_module:   The name of the module added(string).
        @param[in]  new_address:  The address of the added module(string).
        """ 
        # check the valdity of the address
        if (len(new_address) == 4) and new_address.startswith('0x') \
           and pySCPI_config.is_hex(new_address[2:]):
            # add the new address
            if self.no_addresses:
                self.address_of = {# Non-SCPI Devices
                                   'CS EPS':     '0x2B',
                                   'ADCS CTRL':  '0x1F',
                                   'CS BAT':     '0x2A',
                                   'EXT_LIGHT':  '0x60',
                                   }         
                self.no_addresses = False
            # end if
            
            self.address_of[new_module] = new_address
        else:
            self.error_log.append('*** Invalid default address for ' +
                                  new_module  + ' in xml file ***')    
        # end if        
    # end def     
    

    def add_command(self, new_command):
        """ 
        Append the new command to the existing list of commands
        
        @param[in]  new_command:  The new command to add (string).
        """ 
        if self.no_commands:
            self.default_commands = [new_command]
            self.no_commands = False
        else:
            self.default_commands.append(new_command) 
    # end def    
    
    
    def log_error(self, error):
        """ 
        Append an error to the class's error log
        
        @param[in]  error:  The error to log (string).
        """         
        self.error_log.append(error)
    # end def

# end class

class main_gui:
    """
    The main loop GUI for pySCPI
    """
    
    def __init__(self, default_values, version_number, terminator, scpi_commands):
        
        self.version = version_number
        self.defaults = default_values
        self.scpi_commands = scpi_commands
        self.terminator = terminator
        
        self.root = TK.Tk()
        self.root.geometry(str(root_width) + 'x' + str(root_height))
        self.root.config(bg = 'white') # to show through the gaps between frames
        current_column = 0        
    
        ############################ Parent Frames #####################################
        # Frame for the header image
        self.Header = TK.Frame(self.root)
        self.Header.config(bg = default_color)
        self.Header.grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW')
        
        # Frame for the configuration options
        self.Config_frame = TK.Frame(self.root)
        self.Config_frame.config(bg = default_color)
        self.Config_frame.grid(row = 1, column = 0, columnspan = 2, sticky = 'nsew', pady = 2)
        
        # frame for the inputs
        self.Input_frame = TK.Frame(self.root)
        self.Input_frame.config(bg = default_color)
        self.Input_frame.grid(row = 2, column = 0, sticky = 'nsew', padx = 1)
        
        # Frame for the outputs
        self.Output_frame = TK.Frame(self.root)
        self.Output_frame.config(bg = default_color)
        self.Output_frame.grid(row = 2, column = 1, sticky = 'nsew', padx = 1)   
        
        ################################ Header Image ##################################
        
        self.input_image = Image.open('src/Header.jpg')
        # find the images aspect ratio so it can be maintained
        self.aspect_ratio = float(self.input_image.size[1])/float(self.input_image.size[0])
        # resize to fit the window
        self.header_image = self.input_image.resize((root_width, int(root_width*self.aspect_ratio)), Image.ANTIALIAS)
        
        # Header Image
        self.header_photo = ImageTk.PhotoImage(self.header_image)
        #image_label = Label(Header, image=header_photo)
        #image_label.grid(row = 0, column = 0, sticky = NSEW)
        self.image_canvas = TK.Canvas(self.Header, width=root_width, height=int(root_width*self.aspect_ratio), highlightthickness=0, borderwidth=0)
        self.image_on_canvas = self.image_canvas.create_image(0,0, image=self.header_photo, anchor='nw')
        self.text_on_canvas = self.image_canvas.create_text(root_width-2, int(root_width*self.aspect_ratio), anchor='se', text=('v'+str(version_number)), font=button_font, fill='white')
        self.image_canvas.grid(row = 0, column = 0, sticky='nsew')
        self.Header.bind('<Configure>', self.resize_image) # link the resizing event        

        
        ##################### Configuration Elements #############################
        
        # sub-frame for the buttons
        self.but_frame = TK.Frame(self.Config_frame)
        self.but_frame.config(bg = default_color)
        self.but_frame.grid(row = 0, column = current_column, rowspan = 3, padx = 10)
        self.but_frame.columnconfigure(0, weight = 1)
        
        # Load XML Button
        self.xml_button = TK.Button(self.but_frame, text = 'Load Commands', command = partial(pySCPI_XML.Load_XML,self), activebackground = 'green', width = 15)
        self.xml_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
        self.xml_button.grid(row = 0, column=0, padx = 5)        
        
        # View README Button
        self.readme_button = TK.Button(self.but_frame, text = 'View ReadMe', command = partial(View_Readme,self), activebackground = 'green', width = 15)
        self.readme_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
        self.readme_button.grid(row = 1, column=0, padx = 5, pady = 5)
        current_column += 1
        
        # Slave Device selector sub-frame
        self.slave_frame = TK.Frame(self.Config_frame)
        self.slave_frame.config(bg = default_color)
        self.slave_frame.grid(row = 2, column = current_column, padx = 5, sticky = 'nsew')
        self.slave_frame.columnconfigure(0,weight = 2)
        self.slave_frame.columnconfigure(1,weight = 2)
        
        # Slave selector title
        self.slave_label = TK.Label(self.Config_frame, text = 'Slave Device')
        self.slave_label.config(font = label_font, bg = default_color)
        self.slave_label.grid(row = 1, column= current_column, sticky = 's')
        
        # device name variable
        self.devices = scpi_commands.get_devices()
        self.slave_var = TK.StringVar(self.root)
        self.slave_var.set(self.devices[0])
        
        # device address variable
        self.addr_var = TK.StringVar(self.root)
        self.addr_var.set(default_values.address_of[self.devices[0]])
        
        # device address display box
        self.addr_text = TK.Entry(self.slave_frame, textvariable=self.addr_var, width = 4, justify = 'center')
        self.addr_text.config(font = text_font, highlightbackground= default_color)
        self.addr_text.grid(row = 0, column = 1, ipadx=20, pady = 5,sticky = 'w', ipady = 3)
        
        # device selector drop down menu
        self.slave_menu = TK.OptionMenu(self.slave_frame, self.slave_var, *tuple(self.devices), command = self.update_addr)
        if (platform.system == 'Windows'):
            # Size differently depending on the OS
            self.slave_menu.config(width = 1, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
        else:
            self.slave_menu.config(width = 4, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
        # end if
        self.slave_menu["menu"].config(font = label_font, bg = default_color)
        self.slave_menu.grid(row = 0, column = 0, sticky = 'e', ipadx=20)
        current_column += 1
        
        # delay text box sub-frame
        self.delay_frame = TK.Frame(self.Config_frame)
        self.delay_frame.config(bg = default_color)
        self.delay_frame.grid(row = 2, column = current_column, sticky = 'ew')
        self.delay_frame.columnconfigure(0, weight = 2)
        self.delay_frame.columnconfigure(1, weight = 2)
        
        # delay title
        self.delay_label = TK.Label(self.Config_frame, text = 'Intermessage Delay')
        self.delay_label.grid(row = 1, column = current_column, padx = 5, sticky = 's')
        self.delay_label.config(font = label_font, bg = default_color)
        
        # delay entry box
        self.delay = TK.Entry(self.delay_frame, justify = 'right', width = 7)
        self.delay.config(font = text_font, highlightbackground= default_color)
        self.delay.grid(row = 0, column = 0, ipady = 3, sticky = 'e')
        self.delay.insert(0, str(default_values.default_delay))
        
        # delay units deiplay
        self.delay_units = TK.Label(self.delay_frame, text = 'ms')
        self.delay_units.config(font = text_font, bg = default_color)
        self.delay_units.grid(row = 0, column = 1, sticky = 'w')
        current_column += 1
        
        # ASCII Delay sub-frame
        self.ascii_frame = TK.Frame(self.Config_frame)
        self.ascii_frame.config(bg = default_color)
        self.ascii_frame.grid(row = 2, column = current_column, sticky = 'ew')
        self.ascii_frame.columnconfigure(0, weight = 2)
        self.ascii_frame.columnconfigure(1, weight = 2)
        
        # ascii delay title
        self.ascii_label = TK.Label(self.Config_frame, text = 'ASCII Message Delay')
        self.ascii_label.config(font = label_font, bg = default_color)
        self.ascii_label.grid(row = 1, column=current_column, sticky = 's')
        
        # ascii delay entry box
        self.ascii = TK.Entry(self.ascii_frame, justify = 'right', width = 7)
        self.ascii.config(font = text_font, highlightbackground= default_color)
        self.ascii.grid(row = 0, column=0, ipady = 3, sticky = 'e')
        self.ascii.insert(0, str(default_values.default_delay*4))
        
        # ascii units display
        self.ascii_units = TK.Label(self.ascii_frame, text = 'ms')
        self.ascii_units.config(font = text_font, bg = default_color)
        self.ascii_units.grid(row = 0, column = 1, sticky = 'w')
        current_column += 1
        
        # ouput float size selector title
        self.float_label = TK.Label(self.Config_frame, text = 'Float DP')
        self.float_label.config(font = label_font, bg = default_color)
        self.float_label.grid(row = 1, column=current_column, sticky = 's')
        
        # float size variable
        self.float_var = TK.IntVar(self.root)
        self.float_var.set(default_values.default_dp)
        
        # float size drop down menu
        self.float_menu = TK.OptionMenu(self.Config_frame, self.float_var, 1,2,3,4,5,6,7,8,9,10,11,12)
        if platform.system() == 'Windows':
            # adjust size for different OSs
            self.float_menu.config(width = 1, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
        else:
            self.float_menu.config(width = 7, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
            self.float_menu["menu"].config(fg = 'black')
        # end if
        self.float_menu["menu"].config(font = label_font, bg = default_color)
        self.float_menu.grid(row = 2, column = current_column)
        current_column += 1  
        
        # Logging period sub-frame
        self.logging_frame = TK.Frame(self.Config_frame)
        self.logging_frame.config(bg = default_color)
        self.logging_frame.grid(row = 2, column = current_column, sticky = 'ew')
        self.logging_frame.columnconfigure(0, weight = 2)
        self.logging_frame.columnconfigure(1, weight = 2)
        
        #logging period title
        self.logging_label = TK.Label(self.Config_frame, text = 'Logging Period')
        self.logging_label.config(font = label_font, bg = default_color)
        self.logging_label.grid(row = 1, column=current_column, padx = 5, sticky = 's')
        
        # logging period entry box
        self.logging = TK.Entry(self.logging_frame, justify = 'right', width = 7)
        self.logging.config(font = text_font, highlightbackground= default_color)
        self.logging.grid(row = 0, column=0, ipady = 3, sticky = 'e')
        self.logging.insert(0, '60')
        
        # logging period unit display
        self.logging_units = TK.Label(self.logging_frame, text = 's')
        self.logging_units.config(font = text_font, bg = default_color)
        self.logging_units.grid(row = 0, column = 1, sticky = 'w')
        current_column += 1  
        
        # error count sub-frame
        self.error_frame = TK.Frame(self.Config_frame)
        self.error_frame.config(bg = default_color)
        self.error_frame.grid(row = 2, column = current_column, sticky = 'ew', padx = 10)
        self.error_frame.columnconfigure(0, weight = 2)
        self.error_frame.columnconfigure(1, weight = 2)
        
        # error count title
        self.error_label = TK.Label(self.Config_frame, text = 'Error count')
        self.error_label.config(font = label_font, bg = default_color)
        self.error_label.grid(row = 1, column=current_column, padx = 5, sticky = 's')
        
        # error count entry box
        self.errors = TK.Entry(self.error_frame, justify = 'center', width = 7)
        self.errors.config(font = text_font, highlightbackground= default_color, disabledforeground = 'black', disabledbackground = 'white')
        self.errors.grid(row = 0, column=0, ipady = 3, sticky = 'e')
        self.errors.insert(0, '0')
        self.errors.config(state = 'disabled')  
        
        # error clearing button
        self.error_button = TK.Button(self.error_frame, text = 'Zero', command = self.zero_errors, activebackground = 'green', width = 5)
        self.error_button.config(font = label_font, bg = default_color, highlightbackground= default_color)
        self.error_button.grid(row = 0, column=1, sticky = 'w')
        
        
        ############################ Inputs Section ####################################
        
        # Input header sub-frame
        self.input_header_frame = TK.Frame(self.Input_frame)
        self.input_header_frame.config(bg = default_color)
        self.input_header_frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        # input title
        self.input_header = TK.Label(self.input_header_frame, text = 'Input Commands:')
        self.input_header.config(font=title_font, bg = default_color)
        self.input_header.grid(row = 0, column = 0, sticky = 'w', padx = 5)
        
        # file text_box
        self.file_window = TK.Text(self.input_header_frame, height = 1, width = 33)
        self.file_window.config(font = text_font, bg = default_color, state = 'disabled', highlightbackground= default_color)
        self.file_window.grid(row = 0, column=1, ipady = 3, sticky = 'e')
        
        # Command input sub-frame
        self.command_frame = TK.Frame(self.Input_frame)
        self.command_frame.config(bg = default_color)
        self.command_frame.grid(row = 1, column = 0, sticky = 'nsew')
        
        # text box to enter commands into
        self.Command_text = TK.Text(self.command_frame, height = 10, width = 58, padx = 3, pady = 3)
        self.Command_text.config(font = text_font, highlightbackground= default_color)
        self.Command_text.insert('insert', '\n'.join(default_values.default_commands))
        self.Command_text.bind('<Key>', self.update_filename)
        self.Command_text.grid(row = 0, column=0, sticky = 'nsew')
        
        # scrollbar for the command text box, linked to the text box
        self.command_scroll = TK.Scrollbar(self.command_frame, command = self.Command_text.yview)
        self.command_scroll.grid(column = 1, row = 0, sticky = 'nsew')
        self.Command_text['yscrollcommand'] = self.command_scroll.set
        
        # Buttons subframe
        self.button_frame = TK.Frame(self.Input_frame)
        self.button_frame.config(bg = default_color)
        self.button_frame.grid(row = 2, column = 0, sticky = 'nsew')
        
        # Write XML Button
        self.save_button = TK.Button(self.button_frame, text = 'Save Commands', command = partial(pySCPI_XML.Write_XML, self), activebackground = 'green', width = 13)
        self.save_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
        self.save_button.grid(row = 0, column=0, pady = 5, padx = 10, sticky = 'ew')
        self.button_frame.columnconfigure(0, weight = 1)
        
        # Use Aardvark Button
        self.aardvark_button = TK.Button(self.button_frame, text = 'Send Commands', command = partial(pySCPI_aardvark.Write_I2C, self), activebackground = 'green', width = 13)
        self.aardvark_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
        self.aardvark_button.grid(row = 0, column=1, pady = 5, sticky = 'ew')
        self.button_frame.columnconfigure(1, weight = 1)
        
        # Logging button
        self.logging_button = TK.Button(self.button_frame, text = 'Start Logging', command = partial(pySCPI_aardvark.start_logging, self), activebackground = 'green', width = 13)
        self.logging_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
        self.logging_button.grid(row = 0, column=2, pady = 5, padx = 10, sticky = 'ew')
        self.button_frame.columnconfigure(2, weight = 1)
        
        ############################## Output Frame ####################################
        
        # Output Title Frame
        self.output_title_frame = TK.Frame(self.Output_frame)
        self.output_title_frame.config(bg = default_color)
        self.output_title_frame.grid(row = 0, column = 0, columnspan = 2, sticky = 'nsew')
        
        
        # Output title
        self.output_label = TK.Label(self.output_title_frame, text = 'Output:')
        self.output_label.config(font=title_font, bg = default_color)
        self.output_label.grid(row = 0, column = 0)
        
        # Output Progress Bar
        self.progress = ttk.Progressbar(self.output_title_frame, orient = 'horizontal', mode = 'determinate', length = 200)
        self.progress.grid(row = 0, column = 1)
        
        # output text box
        self.output_text = TK.Text(self.Output_frame, height = 20, width = 100, padx = 3, pady = 3)
        self.output_text.config(font = text_font, highlightbackground= default_color)
        self.output_text.grid(row = 1, column=0, sticky = 'nsew')
        self.output_text.config(state='disabled', wrap='word')
        
        # scrolbar for the output textbox, linked to the text box
        self.output_scroll = TK.Scrollbar(self.Output_frame, command = self.output_text.yview)
        self.output_scroll.grid(column = 1, row = 1, sticky = 'nsew')
        self.output_text['yscrollcommand'] = self.output_scroll.set
        
        # highlight tag
        self.output_text.tag_config('error', foreground = 'red')
        
        ############################# Resizing #########################################
        
        # allow for resizing of the configuration frame columns
        self.Config_frame.columnconfigure(1, weight = 1, minsize = 200)
        self.Config_frame.columnconfigure(2, weight = 2, minsize = 100)
        self.Config_frame.columnconfigure(3, weight = 2, minsize = 80)
        self.Config_frame.columnconfigure(4, weight = 2, minsize = 60)
        self.Config_frame.columnconfigure(5, weight = 2, minsize = 80)
        self.Config_frame.columnconfigure(6, weight = 1, minsize = 80)
        
        # allow for resizing of the input frame row containing the text box
        self.Input_frame.rowconfigure(1, weight = 2)
        self.command_frame.rowconfigure(0, weight = 2)
        
        # allow for resizing of the otuput frame row containing the text box
        self.Output_frame.rowconfigure(1, weight = 2)
        self.root.rowconfigure(2, weight = 2)
        
        # allow for resizing of the otuput frame column
        self.Output_frame.columnconfigure(0, weight = 2)
        self.root.columnconfigure(1, weight = 5, minsize = 200)
        self.output_title_frame.columnconfigure(0, weight = 2)
        self.output_title_frame.columnconfigure(1, weight = 2)
        
        # set window minsize to prevent objects crashing
        self.root.minsize(width = 900, height = 500)      
        
        
        # define icon
        self.root.iconbitmap(r'src/cubesatkit.ico')
        
        # define window title
        self.root.title("PySCPI: PC control of pumpkin SCPI modules")
        self.root.protocol("WM_DELETE_WINDOW", partial(terminator.kill_threads, self))
        
    # end def
    
    def output_clear(self):
        """
        Clear the output text window
        """        
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.config(state='disabled')   
    # end def
    
    def start(self, gui_defs, command_defs):
        """
        Begin the GUI execution after printing any start up errors
        """
        for error in gui_defs.error_log:
            print error
        # end for
        
        for error in command_defs.error_log:
            print error
        # end for
            
        self.root.mainloop()
    # end def
       
    
    def zero_errors(self):
        """ 
        Zero the error count on the GUI
        """
        self.errors.config(state = 'normal', disabledforeground = 'black')
        self.errors.delete(0,'end')
        self.errors.insert(0, '0')     
        self.errors.config(state = 'disabled')
    # end
    
    
    def add_error(self):
        """ 
        Increment the GUI error counter
        """
        try:
            current = int(self.errors.get())
        except ValueError:
            current = 1
        # end try
        self.errors.config(state = 'normal', disabledforeground = 'red')
        self.errors.delete(0,'end')
        self.errors.insert(0, str(current + 1))     
        self.errors.config(state = 'disabled')  
    # end        
    
    
    def update_addr(self, value):
        """
        Update the address in the GUI
        """
        self.addr_var.set(self.defaults.address_of[value])
        self.addr_text.config(background = 'white')
    # end def       
       
        
    def resize_image(self, event):
        """
        Event function to auto-resize the header image with the window
        
        TODO try and speed up this function
        """            
        # find new geometry
        new_width = event.width
        new_height = int(new_width * self.aspect_ratio)
        # resize
        self.header_image = self.input_image.resize((new_width, new_height), Image.ANTIALIAS)
        # snap the Frame rows around it
        self.root.rowconfigure(0, minsize = new_height)
        self.Header.rowconfigure(0, minsize = new_height)
        # load the new image
        self.header_photo = ImageTk.PhotoImage(self.header_image)
        self.image_canvas.config(width=new_width, height=new_height)
        self.image_canvas.itemconfig(self.image_on_canvas, image=self.header_photo)
        text_move_x = new_width - self.image_canvas.coords(self.text_on_canvas)[0] - 2
        text_move_y = new_height - self.image_canvas.coords(self.text_on_canvas)[1]
        self.image_canvas.move(self.text_on_canvas, text_move_x, text_move_y)
    # end def   
        
    
    def action_lock(self, state, active_button=None):
        """
        Disable the function of all the buttons on the GUI except the one requested 
        and then reenable them.
        
        @param[in]  state (string): 'Lock':   Lock all buttons except the active_button
                                    'Unlock': Unlock all of the buttons
        @param[in]  active_button:  Optional-The button not to lock (tkinter.Button).
        """      
        # list of all the buttons
        button_list = [self.readme_button, self.xml_button, self.aardvark_button, self.save_button, self.logging_button]
        if (state == 'Lock'):
            # lock the bottons
            for button in button_list:
                if (button != active_button):
                    # lock this button
                    button.config(state = 'disabled')
                # end if
            # end for
        elif (state == 'Unlock'):
            # Unlock all the buttons
            for button in button_list:
                button.config(state = 'normal', background = default_color)
            # end for
        # end if
    # end def   
    
    def logging_button_state(self, state):
        """
        Function to change the configuration of the logging button.
        
        @param[in]    state:    The desired state of the button, 
                                Either 'start' or 'stop' (string).
        """
        # define the partial to start the logging
        start_command = partial(pySCPI_aardvark.start_logging, self)
        
        # determine which state to put the button into
        if state == 'start':
            # Change the logging button so that it starts logging
            self.logging_button.config(text = 'Start Logging', 
                                       command = start_command)   
            
        elif state == 'stop':
            # Change the logging button so that it stops logging
            self.logging_button.config(state = 'normal', 
                                      text = 'Stop Logging', 
                                      command = self.terminator.kill_log) 
            
        else:
            # a valid button state was not requested, default to stop
            print '*** invalid logging button state requested ***'
            self.logging_button.config(state = 'normal', 
                                      text = 'Stop Logging', 
                                      command = self.terminator.kill_log)  
        # end if
    # end def
    
    def update_filename(self, filename = ''):
        """
        Function to change the loaded filename to display
        
        @param[in]  filename:   The filename to updte the gui to show
                                (string).
        """     
        self.file_window.config(state='normal')
        self.file_window.delete('1.0', 'end')
        if filename != '':
            self.file_window.insert('insert', filename.split('/')[-1])
        # end
        self.file_window.config(state = 'disabled')
        self.file_window.tag_configure('center', justify = 'center')
        self.file_window.tag_add('center', '1.0', 'end') 
    # end def
    
    def update_fields(self, directives, device_detected):
        """
        Function to update the gui with values read from an xml file
        
        @param[in]  directives:      Information to update the gui with 
                                     (pySCPI_config.write_directives)
        @param[in]  device_detected: The device name that was read from the 
                                     xml file (string).
        """         
        
        # update the delay field
        self.delay.delete(0,'end')
        self.delay.insert(0, directives.delay_time)  
        
        
        # update the address field
        address = directives.addr
        self.addr_var.set(address)
                            
        # create local address dictionary to compare to
        local_addrs = self.defaults.address_of.copy()
        local_addrs['GPS'] = '0x51' # add the GPS
        
        # check to see if the device is in the dictionary
        if device_detected in local_addrs.keys():
            
            # see if the device address matches the default
            if address == local_addrs[device_detected]:
                # address matches a device
                
                # update the gui
                if device_detected == 'GPS':
                    # substitute the GPS name
                    self.slave_var.set('GPSRM')
                    
                else:
                    self.slave_var.set(device_detected)
                # end if
                
            else:
                # address does not math the default 
                # so color it yellow as a warning
                self.addr_text.config(background = 'yellow') 
                
                print '*** Warning, loaded device address '\
                      'does not match a device default ***'
            # end if  
        elif address in local_addrs.values():
            # address matches a device
            device = local_addrs.keys()[local_addrs.values().index(address)]
            self.slave_var.set(device)
        else:
            # address does not so color it yellow as a warning
            self.addr_text.config(background = 'yellow') 
            print '*** Warning, loaded device address '\
                  'does not match a device default ***'
        # end if
       
       
        # check the appropriateness of the ascii delay
        if (directives.ascii_time == '0') or \
           (directives.ascii_time <= directives.delay_time):
            # it is too short, go to the default delay
            directives.ascii_time = 4*int(directives.delay_time)
        # end if
        
        # update the ascii_delay
        self.ascii.delete(0,'end')
        self.ascii.insert(0, directives.ascii_time)      
        
        # empty command box and add new commands
        self.Command_text.delete('1.0', 'end')
        self.Command_text.insert('insert', '\n'.join(directives.command_list))        
    # end def
    
 
    def get_delay(self):
        """
        Function to find the desired delay that was entered in the gui.
        
        @return     (int)         The delay that will be used in ms.
        """        
        # read the delay from the gui
        delay_text = self.delay.get()
        # establish the default delay
        delay_time = self.defaults.default_delay
        
        # verify if the delay is valid
        if delay_text.isdigit():
            # is a good delay so set it as the delay time
            delay_time = int(delay_text)
            
        else:
            # the delay is not valid
            print '*** Requested delay is not valid, '\
                  'reverting to default ***'
            # restore the default delay
            self.delay.delete(0,'end')
            self.delay.insert(0, str(delay_time))
        # end if    
        
        return delay_time
    # end def
    
    def get_ascii_delay(self):
        """
        Function to find the desired ascii delay that was entered 
        in the gui.
        
        @return     (int)         The delay that will be used in ms.
        """    
        # read the ascii delay from the gui
        ascii_text = self.ascii.get()
        # establish the default delay
        ascii_time = self.defaults.default_delay*4
        
        # verify that the delay is valid
        if ascii_text.isdigit():
            # is a good delay so set it as the ascii time
            ascii_time = int(ascii_text)
            
        else:
            # the delay is invalid
            print '*** Requested ascii delay is not valid, '\
                  'reverting to default ***'
            
            # restore the default delay
            self.ascii.delete(0,'end')
            self.ascii.insert(0, str(ascii_time))
        # end if 
        
        return ascii_time
    # end def
    
    
    def get_i2c_address(self):
        """
        Function to find the desired I2C address that was entered 
        in the gui.
        
        @return     (int)         The I2C address that will be used.
        """  
        # read the address from the gui
        addr_string = self.addr_text.get()
        
        # verify the validity of the delay
        if addr_string.startswith('0x') and (len(addr_string) == 4) and \
           pySCPI_config.is_hex(addr_string[2:]):
            # is a good address so use it
            addr_num = int(addr_string,16)
            
        else:
            # is it not a valid delay
            print '*** Invalid address entered, '\
                  'reverting to device default ***'
            
            # restore the defalut delay for the selected module
            addr_string = self.defaults.address_of[self.slave_var.get()]
            self.addr_var.set(addr_string)
            addr_num = int(addr_string,16)
        # end if
        
        return addr_num
    # end def
    
    
    def get_command_list(self):
        """
        Function to find the desired I2C address that was entered 
        in the gui.
        
        @return    (list of strings) The list of commands to be sent.
        """  
        # read in the commands
        commands = self.Command_text.get('1.0', 'end').encode('ascii', 'ignore')
        # split them into a list
        input_list = commands.split('\n')
        # define list to construct into
        command_list = []
        
        # construct the list
        for item in input_list:
            # remove white space and add to list
            item = item.strip()
            
            if item != '':
                # item is not empty so add it to the list
                command_list = command_list + [item]
            # end if
        # end for
        
        return command_list
    # end def
    
    
    def get_logging_period(self, command_list, delay_time, ascii_time):
        """
        Function to find the logging period that will be used for 
        logging by looking at the gui.
        
        @param[in] delay_time:       The intermessage delay in use (int).
        @param[in] ascii_delay:      The ascii delay in use (int).
        @return    (int)             The logging period to be used.
        """      
        
        # find the amount of time taken for the all the commands to be 
        # executed in a single iteration of the loop
        loop_time = 0
        
        # add up all of the commands
        for command in [c for c in command_list if not c.startswith('#')]:
            # add up the time of all the commands in the list
            if 'ascii' in command:
                # is ascii do add both delays
                loop_time += (ascii_time + delay_time)
                
            elif 'TEL?' in command:
                # is telemetry so there are two delay periods
                loop_time += (2*delay_time)
                
            elif command.startswith('<DELAY'):
                # is is a delay command so add that delay
                delay_command = int(command.split(' ')[2][:-1])
                loop_time += delay_command 
                
            else:
                # is just a command so only add a single delay
                loop_time += delay_time
            # end if
        # end for
        
        # convert the loop time into seconds and round up.
        loop_time = (loop_time/1000)+1
        
        
        # extract the requested logging period from the gui
        logging_text = self.logging.get()
        
        # determine the validity of the delay
        if logging_text.isdigit():
            # delay is a number so it is acceptible
            logging_time = int(logging_text)
            
        else:
            # the logging delay is unacceptible
            print '*** Requested logging period is not valid, '\
                  'reverting to default ***'
            
            # revert to the length of time taken to execute all commands
            logging_time = loop_time * 2          
            
            self.logging.delete(0,'end')
            self.logging.insert(0, str(logging_time))
            
        # end if
        
        # see if the delay is long enough
        if logging_time <= loop_time*1.2:
            # this is deemed to short for consistant operaton so 
            # warn the user
            print '*** Warning, logging period may be shorter than '\
                  'the duration of the commands requested ***'
            
        # end if 
        
        return logging_time
    # end def
# end class


class GUI_Writer(object):
    """
    Class to handle the re-mapping of stdout to the GUI
    """    
    def __init__(self, gui):
        self.output_text = gui.output_text
        self.add_error = gui.add_error
    # end def
        
    # what to do when a 'print' command is issued 
    def write(self, string):
        self.output_text.config(state='normal')
        if string.startswith('*'):
            self.output_text.insert('insert', string, 'error')
            self.add_error()
        else:
            self.output_text.insert('insert', string)
        # end
        self.output_text.config(state='disabled')
    # end def
# end class

                
#
# ----------------
# Public Functions 


#
# ----------------
# Private Functions 


def View_Readme(gui):
    """
    Function to display the readme file in the GUI window.
    """    
    # lock buttons
    gui.action_lock('Lock', gui.readme_button)
    # clear output
    gui.output_text.config(state='normal')
    gui.output_text.delete('1.0', 'end')
    gui.output_text.config(state='disabled') 
    
    # read all lines from the readme
    with open('src/pySCPI README.txt', 'r') as f:
        content = f.readlines() 
    # end with
    
    print content[0].rstrip() + ' v' + gui.version + '.'
    
    # print each line to the gui
    for line in content[1:]:
        print line.rstrip()
    # end for
    
    gui.zero_errors()
    
    # unlock buttons
    gui.action_lock('Unlock')
# end def

         
def test():
    # test the gui defaults code
    sample_gui_defaults = gui_defaults()
    
    sample_gui_defaults.update_filename('this is a test.xml')
    sample_gui_defaults.update_delay('1000')
    sample_gui_defaults.update_dp('6')
    sample_gui_defaults.update_length('12')
    sample_gui_defaults.add_address('NEW', '0x44')
    sample_gui_defaults.add_command('NEW COMMAND')
    
    first_errors = len(sample_gui_defaults.error_log)
    
    print str(8-first_errors)  + '/8 sample tests passed'
    
    sample_gui_defaults.update_filename('this is a test.xm')
    sample_gui_defaults.update_delay('10g0')
    sample_gui_defaults.update_dp('0')
    sample_gui_defaults.update_length('-4')
    sample_gui_defaults.add_address('NEW', 'AD')
    sample_gui_defaults.add_command('NEW COMMAND')
    
    new_errors = len(sample_gui_defaults.error_log) - first_errors
    
    print str(new_errors)  + '/8 sample tests failed (want 6)'    


if __name__ == '__main__':
    test()
# end if
        