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
__version__ = '0.3.6' #Versioning: http://www.python.org/dev/peps/pep-0386/


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
import Queue


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
    
    @attribute default_filename (string) The default filename to save/load
    @attribute default_delay    (int)    The default intermessage delay in ms
    @attribute default_length   (int)    The default command length in bytes
    @attribute default_dp       (int)    The default number of dp for floats
    @attribute address_of       (dict)   The default module addresses
    @attribute default_commands (list)   The default set of commands (strings)
    @attribute error_log        (list)   List of errors (strings) thrown on boot
    @attribute no_commands      (bool)   True if no commands were loaded on boot
    @attribute no_addresses     (bool)   True if no addresses were loaded
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
    Class that manages the main loop of the gui and all the actions that occur 
    within it.
    
    @attribute version         (string)           PySCPI version number
    @attribute defaults        (GUI_defaults)     Default values for GUI
    @attribute terminator      (terminator_event) Controls exiting pySCPI
    @attribute scpi_commands   (list)             Known commands (strings)
    @attribute root            (TK root)          GUI root object
    @attribute Header          (TK Frame)         Frame for the header image
    @attribute input_image     (Image)            Raw header image
    @attribute aspect_ratio    (int)              AR of the header image
    @attribute img_canvas      (TK Canvas)        Canvas for the header image
    @attribute canvas_img      (Image)            Image on the canvas
    @attribute canvas_txt      (TK label)         Version text on header image
    @attribute xml_button      (TK Button)        'Load XML' Button
    @attribute readme_button   (TK Button)        'View Readme' Button
    @attribute slave_var       (TK string var)    Name of slave device in use
    @attribute addr_var        (TK string var)    Slave address in use
    @attribute addr_text       (TK Entry)         Slave address text box
    @attribute delay           (TK Entry)         Intermessage Delay text box
    @attribute ascii           (TK Entry)         Ascii Delay text box
    @attribute logging         (TK Entry)         Logging Period text box 
    @attribute errors          (TK Entry)         Error counter text box
    @attribute error_button    (TK Button)        'Zero Errors' Button
    @attribute file_window     (TK Entry)         Filename display text box
    @attribute Command_text    (TK Text)          Text box for writing commands
    @attribute save_button     (TK Button)        'Save to XML' Button
    @attribute aardvark_button (TK Button)        'Write Commands' Button
    @attribute logging_button  (TK Button)        'Start Logging' Button
    @attribute progress        (ttk Progressbar)  Progress bar on the GUI
    @attribute output_text     (TK text)          Output text box
    @attribute text_queue      (Queue)            Output text queue
    @attribute line_queue      (Queue)            Line in the command box highlighting queue
    @attribute progress_queue  (Queue)            Progressbar position queue
    """
    
    def __init__(self,default_values,version_number,terminator,scpi_commands):
        """ 
        Construct the GUI
        
        @param[in]  default_values: The default values to load into the GUI
                                    (pySCPI_gui.gui_defaults)
        @param[in]  version_number: The version number for pySCPI (string)
        @param[in]  terminator:     The object to control pySCPI termination 
                                    (pySCPI_threading.terminator_event)
        @param[in]  scpi_commands:  Library of all of the known SCPI commands 
                                    (Dictionary)
        """           
        
        self.version = version_number
        self.defaults = default_values
        self.terminator = terminator
        self.scpi_commands = scpi_commands
        
        self.log_file = open("log_file.txt", "w")
        self.text_queue = Queue.Queue()
        self.line_queue = Queue.Queue()
        self.progress_queue = Queue.Queue()
        
        self.root = TK.Tk()
        self.root.geometry(str(root_width) + 'x' + str(root_height))
        self.root.config(bg = 'white') # to show through the gaps between frames
        current_column = 0        
    
        ############################ Parent Frames #############################
        # Frame for the header image
        self.Header = TK.Frame(self.root)
        self.Header.config(bg = default_color)
        self.Header.grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW')
        
        # Frame for the configuration options
        Config_frame = TK.Frame(self.root)
        Config_frame.config(bg = default_color)
        Config_frame.grid(row = 1, column = 0, columnspan = 2, 
                          sticky = 'nsew', pady = 2)
        
        # frame for the inputs
        Input_frame = TK.Frame(self.root)
        Input_frame.config(bg = default_color)
        Input_frame.grid(row = 2, column = 0, sticky = 'nsew', padx = 1)
        
        # Frame for the outputs
        Output_frame = TK.Frame(self.root)
        Output_frame.config(bg = default_color)
        Output_frame.grid(row = 2, column = 1, sticky = 'nsew', padx = 1)   
        
        ################################ Header Image #########################
        
        self.input_image = Image.open('src/Header.jpg')
        # find the images aspect ratio so it can be maintained
        self.aspect_ratio = (float(self.input_image.size[1])/
                             float(self.input_image.size[0]))
        # resize to fit the window
        header_height = int(root_width*self.aspect_ratio)
        self.header_image = self.input_image.resize((root_width, header_height), 
                                               Image.ANTIALIAS)
        
        # Header Image
        self.header_photo = ImageTk.PhotoImage(self.header_image)
        self.img_canvas = TK.Canvas(self.Header, width=root_width, 
                                      height=header_height, 
                                      highlightthickness=0, borderwidth=0)
        self.canvas_img = self.img_canvas.create_image(0,0, 
                                                       image=self.header_photo, 
                                                       anchor='nw')
        
        # Version text on the image
        version_text = ('v'+str(version_number))
        self.canvas_txt = self.img_canvas.create_text(root_width-2, 
                                                      header_height, 
                                                      anchor='se', 
                                                      text=version_text, 
                                                      font=button_font, 
                                                      fill='white')
        
        self.img_canvas.grid(row = 0, column = 0, sticky='nsew')
        self.Header.bind('<Configure>', self.resize_image) # link the event        

        
        ##################### Configuration Elements ###########################
        
        # sub-frame for the buttons
        but_frame = TK.Frame(Config_frame)
        but_frame.config(bg = default_color)
        but_frame.grid(row = 0, column = current_column, rowspan = 3, padx = 10)
        but_frame.columnconfigure(0, weight = 1)
        
        # Load XML Button
        self.xml_button = TK.Button(but_frame, text = 'Load Commands', 
                                    command = partial(pySCPI_XML.Load_XML,self),
                                    activebackground = 'green', width = 15)
        self.xml_button.config(font = button_font, bg = default_color, 
                               highlightbackground= default_color)
        self.xml_button.grid(row = 0, column=0, padx = 5)        
        
        # View README Button
        self.readme_button = TK.Button(but_frame, text = 'View ReadMe', 
                                       command = partial(View_Readme,self), 
                                       activebackground = 'green', width = 15)
        self.readme_button.config(font = button_font, bg = default_color, 
                                  highlightbackground= default_color)
        self.readme_button.grid(row = 1, column=0, padx = 5, pady = 5)
        current_column += 1
        
        # Slave Device selector sub-frame
        slave_frame = TK.Frame(Config_frame)
        slave_frame.config(bg = default_color)
        slave_frame.grid(row = 2, column = current_column, 
                         padx = 5, sticky = 'nsew')
        slave_frame.columnconfigure(0,weight = 2)
        slave_frame.columnconfigure(1,weight = 2)
        
        # Slave selector title
        slave_label = TK.Label(Config_frame, text = 'Slave Device')
        slave_label.config(font = label_font, bg = default_color)
        slave_label.grid(row = 1, column= current_column, sticky = 's')
        
        # device name variable
        devices = scpi_commands.get_devices()
        self.slave_var = TK.StringVar(self.root)
        self.slave_var.set(devices[0])
        
        # device address variable
        self.addr_var = TK.StringVar(self.root)
        self.addr_var.set(default_values.address_of[devices[0]])
        
        # device address display box
        self.addr_text = TK.Entry(slave_frame, textvariable=self.addr_var, 
                                  width = 4, justify = 'center')
        self.addr_text.config(font = text_font, 
                              highlightbackground = default_color)
        self.addr_text.grid(row = 0, column = 1, ipadx=20, 
                            pady = 5, sticky = 'w', ipady = 3)
        
        # device selector drop down menu
        slave_menu = TK.OptionMenu(slave_frame, self.slave_var, *tuple(devices),
                                   command = self.update_addr)
        if (platform.system == 'Windows'):
            # Size differently depending on the OS
            slave_menu.config(width = 1, bg = default_color, 
                              activebackground = default_color, 
                              highlightbackground = default_color, 
                              font = label_font)
        else:
            slave_menu.config(width = 4, bg = default_color, 
                              activebackground = default_color, 
                              highlightbackground = default_color, 
                              font = label_font)
        # end if
        
        slave_menu["menu"].config(font = label_font, bg = default_color)
        slave_menu.grid(row = 0, column = 0, sticky = 'e', ipadx=20)
        current_column += 1
        
        # delay text box sub-frame
        delay_frame = TK.Frame(Config_frame)
        delay_frame.config(bg = default_color)
        delay_frame.grid(row = 2, column = current_column, sticky = 'ew')
        delay_frame.columnconfigure(0, weight = 2)
        delay_frame.columnconfigure(1, weight = 2)
        
        # delay title
        delay_label = TK.Label(Config_frame, text = 'Intermessage Delay')
        delay_label.grid(row = 1, column = current_column,padx = 5,sticky = 's')
        delay_label.config(font = label_font, bg = default_color)
        
        # delay entry box
        self.delay = TK.Entry(delay_frame, justify = 'right', width = 7)
        self.delay.config(font = text_font, highlightbackground= default_color)
        self.delay.grid(row = 0, column = 0, ipady = 3, sticky = 'e')
        self.delay.insert(0, str(default_values.default_delay))
        
        # delay units deiplay
        delay_units = TK.Label(delay_frame, text = 'ms')
        delay_units.config(font = text_font, bg = default_color)
        delay_units.grid(row = 0, column = 1, sticky = 'w')
        current_column += 1
        
        # ASCII Delay sub-frame
        ascii_frame = TK.Frame(Config_frame)
        ascii_frame.config(bg = default_color)
        ascii_frame.grid(row = 2, column = current_column, sticky = 'ew')
        ascii_frame.columnconfigure(0, weight = 2)
        ascii_frame.columnconfigure(1, weight = 2)
        
        # ascii delay title
        ascii_label = TK.Label(Config_frame, text = 'ASCII Message Delay')
        ascii_label.config(font = label_font, bg = default_color)
        ascii_label.grid(row = 1, column=current_column, sticky = 's')
        
        # ascii delay entry box
        self.ascii = TK.Entry(ascii_frame, justify = 'right', width = 7)
        self.ascii.config(font = text_font, highlightbackground= default_color)
        self.ascii.grid(row = 0, column=0, ipady = 3, sticky = 'e')
        self.ascii.insert(0, str(default_values.default_delay*4))
        
        # ascii units display
        ascii_units = TK.Label(ascii_frame, text = 'ms')
        ascii_units.config(font = text_font, bg = default_color)
        ascii_units.grid(row = 0, column = 1, sticky = 'w')
        current_column += 1
        
        # ouput float size selector title
        float_label = TK.Label(Config_frame, text = 'Float DP')
        float_label.config(font = label_font, bg = default_color)
        float_label.grid(row = 1, column=current_column, sticky = 's')
        
        # float size variable
        self.float_var = TK.IntVar(self.root)
        self.float_var.set(default_values.default_dp)
        
        # float size drop down menu
        float_menu = TK.OptionMenu(Config_frame, self.float_var, 
                                   1,2,3,4,5,6,7,8,9,10,11,12)
        
        if platform.system() == 'Windows':
            # adjust size for different OSs
            float_menu.config(width = 1, bg = default_color, 
                              activebackground = default_color, 
                              highlightbackground = default_color, 
                              font = label_font)
        else:
            float_menu.config(width = 7, bg = default_color, 
                              activebackground = default_color, 
                              highlightbackground = default_color, 
                              font = label_font)
            float_menu["menu"].config(fg = 'black')
        # end if
        
        float_menu["menu"].config(font = label_font, bg = default_color)
        float_menu.grid(row = 2, column = current_column)
        current_column += 1  
        
        # Logging period sub-frame
        logging_frame = TK.Frame(Config_frame)
        logging_frame.config(bg = default_color)
        logging_frame.grid(row = 2, column = current_column, sticky = 'ew')
        logging_frame.columnconfigure(0, weight = 2)
        logging_frame.columnconfigure(1, weight = 2)
        
        #logging period title
        logging_label = TK.Label(Config_frame, text = 'Logging Period')
        logging_label.config(font = label_font, bg = default_color)
        logging_label.grid(row = 1, column=current_column,padx = 5,sticky = 's')
        
        # logging period entry box
        self.logging = TK.Entry(logging_frame, justify = 'right', width = 7)
        self.logging.config(font = text_font, highlightbackground=default_color)
        self.logging.grid(row = 0, column=0, ipady = 3, sticky = 'e')
        self.logging.insert(0, '60')
        
        # logging period unit display
        logging_units = TK.Label(logging_frame, text = 's')
        logging_units.config(font = text_font, bg = default_color)
        logging_units.grid(row = 0, column = 1, sticky = 'w')
        current_column += 1  
        
        # error count sub-frame
        error_frame = TK.Frame(Config_frame)
        error_frame.config(bg = default_color)
        error_frame.grid(row = 2, column=current_column,sticky = 'ew',padx = 10)
        error_frame.columnconfigure(0, weight = 2)
        error_frame.columnconfigure(1, weight = 2)
        
        # error count title
        error_label = TK.Label(Config_frame, text = 'Error count')
        error_label.config(font = label_font, bg = default_color)
        error_label.grid(row = 1, column=current_column, padx = 5, sticky = 's')
        
        # error count entry box
        self.errors = TK.Entry(error_frame, justify = 'center', width = 7)
        self.errors.config(font = text_font, highlightbackground= default_color,
                           disabledforeground = 'black', 
                           disabledbackground = 'white')
        self.errors.grid(row = 0, column=0, ipady = 3, sticky = 'e')
        self.errors.insert(0, '0')
        self.errors.config(state = 'disabled')  
        
        # error clearing button
        self.error_button = TK.Button(error_frame, text = 'Zero', 
                                      command = self.zero_errors, 
                                      activebackground = 'green', width = 5)
        self.error_button.config(font = label_font, bg = default_color, 
                                 highlightbackground = default_color)
        self.error_button.grid(row = 0, column=1, sticky = 'w')
        
        
        ############################ Inputs Section ############################
        
        # Input header sub-frame
        input_header_frame = TK.Frame(Input_frame)
        input_header_frame.config(bg = default_color)
        input_header_frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        # input title
        input_header = TK.Label(input_header_frame, text = 'Input Commands:')
        input_header.config(font=title_font, bg = default_color)
        input_header.grid(row = 0, column = 0, sticky = 'w', padx = 5)
        
        # file text_box
        self.file_window = TK.Text(input_header_frame, height = 1, width = 33)
        self.file_window.config(font = text_font, bg = default_color, 
                                state = 'disabled', 
                                highlightbackground = default_color)
        self.file_window.grid(row = 0, column=1, ipady = 3, sticky = 'e')
        
        # Command input sub-frame
        command_frame = TK.Frame(Input_frame)
        command_frame.config(bg = default_color)
        command_frame.grid(row = 1, column = 0, sticky = 'nsew')
        
        # text box to enter commands into
        self.Command_text = TK.Text(command_frame, height = 10, width = 58, 
                                    padx = 3, pady = 3)
        self.Command_text.config(font = text_font, 
                                 highlightbackground = default_color)
        self.Command_text.insert('insert', 
                                 '\n'.join(default_values.default_commands))
        self.Command_text.bind('<Key>', self.update_filename)
        self.Command_text.bind('<Control-Key-3>', self.comment_line) 
        self.Command_text.grid(row = 0, column=0, sticky = 'nsew')
        
        # scrollbar for the command text box, linked to the text box
        command_scroll = TK.Scrollbar(command_frame, 
                                      command = self.Command_text.yview)
        command_scroll.grid(column = 1, row = 0, sticky = 'nsew')
        self.Command_text['yscrollcommand'] = command_scroll.set
        
        # Buttons subframe
        button_frame = TK.Frame(Input_frame)
        button_frame.config(bg = default_color)
        button_frame.grid(row = 2, column = 0, sticky = 'nsew')
        
        # Write XML Button
        self.save_button = TK.Button(button_frame, text = 'Save Commands', 
                                     command=partial(pySCPI_XML.Write_XML,self), 
                                     activebackground = 'green', width = 13)
        self.save_button.config(font = button_font, bg = default_color, 
                                highlightbackground = default_color)
        self.save_button.grid(row = 0, column=0, pady = 5, 
                              padx = 10, sticky = 'ew')
        button_frame.columnconfigure(0, weight = 1)
        
        # Use Aardvark Button
        self.aardvark_button = TK.Button(button_frame, text = 'Send Commands', 
                                         command = partial(pySCPI_aardvark.Write_I2C, self), 
                                         activebackground = 'green', width = 13)
        self.aardvark_button.config(font = button_font, bg = default_color, 
                                    highlightbackground = default_color)
        self.aardvark_button.grid(row = 0, column=1, pady = 5, sticky = 'ew')
        button_frame.columnconfigure(1, weight = 1)
        
        # Logging button
        self.logging_button = TK.Button(button_frame, text = 'Start Logging', 
                                        command = partial(pySCPI_aardvark.start_logging, self), 
                                        activebackground = 'green', width = 13)
        self.logging_button.config(font = button_font, bg = default_color, 
                                   highlightbackground = default_color)
        self.logging_button.grid(row = 0, column=2, pady = 5, 
                                 padx = 10, sticky = 'ew')
        button_frame.columnconfigure(2, weight = 1)
        
        ############################## Output Frame ############################
        
        # Output Title Frame
        output_title_frame = TK.Frame(Output_frame)
        output_title_frame.config(bg = default_color)
        output_title_frame.grid(row = 0, column = 0, columnspan = 2, 
                                sticky = 'nsew')
        
        
        # Output title
        output_label = TK.Label(output_title_frame, text = 'Output:')
        output_label.config(font=title_font, bg = default_color)
        output_label.grid(row = 0, column = 0)
        
        # Output Progress Bar
        self.progress = ttk.Progressbar(output_title_frame, 
                                        orient = 'horizontal', 
                                        mode = 'determinate', length = 200)
        self.progress.grid(row = 0, column = 1)
        
        # output text box
        self.output_text = TK.Text(Output_frame, height = 20, width = 100, 
                                   padx = 3, pady = 3)
        self.output_text.config(font = text_font, 
                                highlightbackground = default_color)
        self.output_text.grid(row = 1, column=0, sticky = 'nsew')
        self.output_text.config(state='disabled', wrap='word')
        
        # scrolbar for the output textbox, linked to the text box
        output_scroll = TK.Scrollbar(Output_frame, 
                                     command = self.output_text.yview)
        output_scroll.grid(column = 1, row = 1, sticky = 'nsew')
        self.output_text['yscrollcommand'] = output_scroll.set
        
        # highlight tag
        self.output_text.tag_config('error', foreground = 'red')
        
        ############################# Resizing #########################################
        
        # allow for resizing of the configuration frame columns
        Config_frame.columnconfigure(1, weight = 1, minsize = 200)
        Config_frame.columnconfigure(2, weight = 2, minsize = 100)
        Config_frame.columnconfigure(3, weight = 2, minsize = 80)
        Config_frame.columnconfigure(4, weight = 2, minsize = 60)
        Config_frame.columnconfigure(5, weight = 2, minsize = 80)
        Config_frame.columnconfigure(6, weight = 1, minsize = 80)
        
        # allow for resizing of the input frame row containing the text box
        Input_frame.rowconfigure(1, weight = 2)
        command_frame.rowconfigure(0, weight = 2)
        
        # allow for resizing of the otuput frame row containing the text box
        Output_frame.rowconfigure(1, weight = 2)
        self.root.rowconfigure(2, weight = 2)
        
        # allow for resizing of the otuput frame column
        Output_frame.columnconfigure(0, weight = 2)
        self.root.columnconfigure(1, weight = 5, minsize = 200)
        output_title_frame.columnconfigure(0, weight = 2)
        output_title_frame.columnconfigure(1, weight = 2)
        
        # set window minsize to prevent objects crashing
        self.root.minsize(width = 900, height = 500)      
        
        
        # define icon
        self.root.iconbitmap(r'src/cubesatkit.ico')
        
        # define window title
        self.root.title("PySCPI: PC control of pumpkin SCPI modules")
        self.root.protocol("WM_DELETE_WINDOW", 
                           partial(terminator.kill_threads, self))
        
    # end def
    
    def update_gui(self):
        """
        Check the queues for pending change to the gui and implement them.
        """
        
        # check for items to print to the output window
        if not self.text_queue.empty():
            # open the output text box for editing
            self.output_text.config(state='normal')
            
            # write any pending messages
            while not self.text_queue.empty():
                string = self.text_queue.get()
                
                if string ==  None:
                    self.output_text.delete('1.0', 'end')
                else:
                    string = string+ '\n'
                    
                    # write to log file
                    self.log_file.write(string)                
                    
                    if string.startswith('*'):
                        self.output_text.insert('end', string, 'error')
                        self.add_error()
                    else:
                        self.output_text.insert('end', string)
                    # end if                    
                # end if
            # end while
            
            self.output_text.see('end')
            self.output_text.config(state='disabled')        
        # end if
        
        
        # check for lines to highlight in the command box
        if not self.line_queue.empty():

            # highlight lines
            while not self.line_queue.empty():
                line = self.line_queue.get()
                
                self.highlight_line(line)
                
                if line != None:
                    self.Command_text.see(str(line+1) + '.0')
                    
                else:
                    self.Command_text.see('0.0')
                # end if                
            # end while
        #end if
        
        # check for progress bar progress
        if not self.progress_queue.empty():

            # highlight lines
            while not self.progress_queue.empty():
                progress = self.progress_queue.get()
                
                if progress == 'step':
                    self.progress.step()
                    
                elif progress == 'start':
                    self.progress.start(100)
                    
                elif type(progress) == str:
                    # changing the maximum
                    self.progress.config(maximum = int(progress))
                    
                elif progress != None:
                    self.progress.config(value = 0)
                        
                else:
                    self.progress.stop()
                # end if                
            # end while
        #end if        
        
        self.root.after(10, self.update_gui)
    # end def
    
    def start(self, gui_defs, command_defs):
        """
        Begin the GUI execution after printing any start up errors
        
        @param[in]  gui_defs:     The default values to load into the GUI
                                  (pySCPI_gui.gui_defaults)
        @param[in]  command_defs: Library of all of the known SCPI commands 
                                  (Dictionary)
        """   
        for error in gui_defs.error_log:
            self.text_queue.put(error)
        # end for
        
        for error in command_defs.error_log:
            self.text_queue.put(error)
        # end for
            
        self.root.after(10, self.update_gui)
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
    
    
    def update_addr(self, device):
        """
        Update the address in the GUI
        
        @param[in]  device:     The name of the address whose address should be
                                put in the address box (String).
        """
        self.addr_var.set(self.defaults.address_of[device])
        self.addr_text.config(background = 'white')
    # end def       
       
        
    def resize_image(self, event):
        """
        Event function to auto-resize the header image with the window
        
        TODO try and speed up this function
        
        @param[in]  event:      The event that called this function
        """            
        # find new geometry
        new_width = event.width
        new_height = int(new_width * self.aspect_ratio)
        # resize
        self.header_image = self.input_image.resize((new_width, new_height), 
                                                    Image.ANTIALIAS)
        # snap the Frame rows around it
        self.root.rowconfigure(0, minsize = new_height)
        self.Header.rowconfigure(0, minsize = new_height)
        # load the new image
        self.header_photo = ImageTk.PhotoImage(self.header_image)
        self.img_canvas.config(width=new_width, height=new_height)
        self.img_canvas.itemconfig(self.canvas_img, image=self.header_photo)
        text_move_x = new_width - self.img_canvas.coords(self.canvas_txt)[0] - 2
        text_move_y = new_height - self.img_canvas.coords(self.canvas_txt)[1]
        self.img_canvas.move(self.canvas_txt, text_move_x, text_move_y)
    # end def   
        
    
    def action_lock(self, state, active_button=None):
        """
        Disable the function of all the buttons on the GUI except the one 
        requested and then reenable them.
        
        @param[in]  state (string): 'Lock':   Lock all buttons except the 
                                              active_button
                                    'Unlock': Unlock all of the buttons
        @param[in]  active_button:  Optional-The button not to lock 
                                    (tkinter.Button).
        """      
        # list of all the buttons
        button_list = [self.readme_button, 
                       self.xml_button, 
                       self.aardvark_button, 
                       self.save_button, 
                       self.logging_button]
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
            self.text_queue.put('*** invalid logging button state requested ***')
            self.logging_button.config(state = 'normal', 
                                      text = 'Stop Logging', 
                                      command = self.terminator.kill_log)  
        # end if
    # end def
    
    def aardvark_button_state(self, state):
        """
        Function to change the configuration of the send commands button.
        
        @param[in]    state:    The desired state of the button, 
                                Either 'start' or 'stop' (string).
        """
        # define the partial to start the logging
        start_command = partial(pySCPI_aardvark.Write_I2C, self)
        
        # determine which state to put the button into
        if state == 'start':
            # Change the button so that it sends commands
            self.aardvark_button.config(text = 'Send Commands', 
                                       command = start_command)   
            
        elif state == 'stop':
            # Change the button so that it stops commands
            self.aardvark_button.config(state = 'normal', 
                                      text = 'Stop Commands', 
                                      command = self.terminator.kill_log) 
            
        else:
            # a valid button state was not requested, default to stop
            self.text_queue.put('*** invalid Send commands button state requested ***')
            self.aardvark_button.config(state = 'normal', 
                                      text = 'Stop Commands', 
                                      command = self.terminator.kill_log)  
        # end if
    # end def    
    
    def is_altering_keypress(self, event):
        """
        Function to determine whether a key press alters the text in the 
        command text box.
    
        @param[in]    event:    The keypress event that is to be examined 
                                (TK.event)
        @return       (bool)    Whether or not this kepress affects the text.
                                
        """
        
        # catch for Null events
        if event == None:
            return False
        # end if
        
        # initialise the return boolean
        is_altering = False
        
        # extract the character of the keypress
        key_char = event.char
        
        # determin the keypress's ascii value
        key_ascii = 0
        if len(key_char) != 0:
            key_ascii = ord(key_char)
        # end if
        
        # extract the name of the key
        key_name = event.keysym
        
        # a list of altering key names
        key_names = ['Enter', 'Return', 'Delete', 'BackSpace', 'Tab', '3']
        
        # check to see if the keypress is altering.
        if (key_ascii >= 32) and (key_ascii <= 254):
            # key is a printing ascii character
            is_altering = True
            
        elif (key_name in key_names):
            # key changes the text in another way
            is_altering = True
        # end if
        
        return is_altering
    # end def
        
    def update_filename(self, event = None, filename = ''):
        """
        Function to change the loaded filename to display
        
        @param[in]  filename:   The filename to updte the gui to show
                                (string).
        """
        
        if (event == None):
            # this function was called not by a keypress
            
            # shorten the filename if required
            print_filename = filename.split('/')[-1]
            if (len(print_filename) > 33):
                print_filename = print_filename[0:29] + '...'
            # end if            
            
            self.file_window.config(state='normal')
            self.file_window.delete('1.0', 'end')
            self.file_window.insert('insert', print_filename)
            self.file_window.config(state = 'disabled')
            self.file_window.tag_configure('center', justify = 'center')
            self.file_window.tag_add('center', '1.0', 'end') 
            
        else:
            # a keypress called this function
            if self.is_altering_keypress(event):
                # the keypress changed what was in the text box so delete
                # the filename
                self.file_window.config(state='normal')
                self.file_window.delete('1.0', 'end')
                self.file_window.config(state = 'disabled')
                self.file_window.tag_configure('center', justify = 'center')
                self.file_window.tag_add('center', '1.0', 'end') 
            # end if
        # end if
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
                
                self.text_queue.put('*** Warning, loaded device address '\
                      'does not match a device default ***')
            # end if  
        elif address in local_addrs.values():
            # address matches a device
            device = local_addrs.keys()[local_addrs.values().index(address)]
            self.slave_var.set(device)
        else:
            # address does not so color it yellow as a warning
            self.addr_text.config(background = 'yellow') 
            self.text_queue.put('*** Warning, loaded device address '\
                  'does not match a device default ***')
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
            self.text_queue.put('*** Requested delay is not valid, '\
                  'reverting to default ***')
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
            self.text_queue.put('*** Requested ascii delay is not valid, '\
                  'reverting to default ***')
            
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
            self.text_queue.put('*** Invalid address entered, '\
                  'reverting to device default ***')
            
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
            self.text_queue.put('*** Requested logging period is not valid, '\
                  'reverting to default ***')
            
            # revert to the length of time taken to execute all commands
            logging_time = loop_time * 2          
            
            self.logging.delete(0,'end')
            self.logging.insert(0, str(logging_time))
            
        # end if
        
        # see if the delay is long enough
        if logging_time <= loop_time*1.2:
            # this is deemed to short for consistant operaton so 
            # warn the user
            self.text_queue.put('*** Warning, logging period may be shorter than '\
                  'the duration of the commands requested ***')
            
        # end if 
        
        return logging_time
    # end def
    
    def comment_line(self, event):
        """
        Function to comment the current line of execution, called by 
        a particular keypress (Ctrl+3).
    
        @param[in] event:        The keypress event that called this function.
        """ 
        
        # delete the filename displayed
        self.update_filename(event)
        
        if self.Command_text.tag_ranges(TK.SEL):
            # if there is selected text, find the start and end positions of 
            # that text.
            [start, end] = self.Command_text.tag_ranges(TK.SEL)
            
            # extract the first and last line indicies of the selected text.
            line_start = int(str(start).split('.')[0])
            line_end = int(str(end).split('.')[0])
            
            # build a list of the selected line indicies
            line_list = range(line_start, line_end+1)
            
        else:
            # there is no selected text so pull the cursor line index
            line_list = [int(self.Command_text.index(TK.INSERT).split('.')[0])]
        # end if
        
        line_starts = []
        line_ends = []
        line_texts = []
        
        # find the start and end indicies of the selected lines
        for index in range(len(line_list)):
            line_starts.append(str(line_list[index]) + '.0')
            line_ends.append(str(line_list[index]+1) + '.0')
            line_texts.append(self.Command_text.get(line_starts[index], line_ends[index]).encode('ascii', 'ignore'))
        # end for
        
        # if any line in the range is commented the uncomment those lines
        if any([line.startswith('#') for line in line_texts]):
            
            # check each line to see if a comment needs to be removed
            for index in range(len(line_texts)):
                if line_texts[index].startswith('#'):
                    # this line has a comment so remove it
                    self.Command_text.delete(line_starts[index])
                # end if
            # end for
            
        else:
            # no lines have comments
            for index in range(len(line_texts)):
                # add a comment character to each line
                self.Command_text.insert(line_starts[index], '#')
            # end for
        # end if
    # end def
    
    def highlight_line(self, line=None):
        """
        Function to highlight a particular line in the command list.
    
        @param[in] line:         The line to highlight(0 indexed), 
                                 None = remove all comments (int)
        """         
        
        # get the names of all tags currently in use
        names = self.Command_text.tag_names()
        
        if 'hlight' in names:
            # if the highlighting tag is already present, remove it
            self.Command_text.tag_delete('hlight')
        # end if
        
        if line != None:
            # highlighting of a line has been requested
            # enable editing of the text box
            self.Command_text.config(state = 'normal')
            
            # define the start and end points for the highlighting
            self.Command_text.mark_set('tag_start', str(line+1) + '.0')
            self.Command_text.mark_set('tag_end', str(line+2) + '.0')
            
            # highlight that line
            self.Command_text.tag_config('hlight', background='blue', 
                                         foreground = 'white')
            self.Command_text.tag_add('hlight', 'tag_start', 'tag_end')
            
            # re-lock the command text box
            self.Command_text.config(state = 'disabled')
        # end if
    # end def

# end class


#class GUI_Writer(object):
    #"""
    #Class to handle the re-mapping of stdout to the GUI
    
    #@attribute output_text (TK text) Text box on gui to write to.
    #@attribute add_error   (Fuction) remapping of gui.add_error function to 
                                     #log errors that are counted.
    #@attribute log_file    (File)    Text file that contains all output
    #"""    
    #def __init__(self, gui):
        #"""
        #Construct the GUI_Writer object
        
        #@param[in] gui:      The GUI to print output to (pySCPI_gui.main_gui)
        #"""           
        #self.output_text = gui.output_text
        #self.add_error = gui.add_error
        #self.log_file = open("log_file.txt", "w")
        #self.old_stdout = sys.stdout
        
    ## end def
        
    ## what to do when a 'print' command is issued 
    #def write(self, string):
        #"""
        #Write to the GUI text box.
        
        #@param[in] string:   The string to write to the GUI.
        #"""          
        
        ## write to log file
        #self.log_file.write(string)
        
        #try:
            #self.output_text.config(state='normal')
            #if string.startswith('*'):
                #self.output_text.insert('end', string, 'error')
                #self.add_error()
            #else:
                #self.output_text.insert('end', string)
            ## end
            #self.output_text.see('end')
            #self.output_text.config(state='disabled')
            
        #except:
            ## could not write to the output text frame
            #self.old_stdout.write(string + '\n')    
        ## end try
        
    ## end def
## end class

                
#
# ----------------
# Private Functions 


def View_Readme(gui):
    """
    Function to display the readme file in the GUI window.
    
    @param  gui:   The GUI in which to display the readme (pySCPI_gui.main_gui)
    """    
    # lock buttons
    gui.action_lock('Lock', gui.readme_button)
    # clear output
    gui.text_queue.put(None)
    
    # read all lines from the readme
    with open('src/pySCPI README.txt', 'r') as f:
        content = f.readlines() 
    # end with
    
    gui.text_queue.put(content[0].rstrip() + ' v' + gui.version + '.')
    
    # print each line to the gui
    for line in content[1:]:
        gui.text_queue.put(line.rstrip())
    # end for
    
    gui.zero_errors()
    
    # unlock buttons
    gui.action_lock('Unlock')
# end def

         
def test():
    """
    Test code for this module.
    """
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
    
    print str(new_errors)  + '/8 sample tests failed (want 5)'    
#end def

if __name__ == '__main__':
    # if this code is not running as an imported module run test code
    test()
# end if