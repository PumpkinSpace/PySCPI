#!/usr/bin/env python
"""
@package pySCPI_config.py
Top level interface for the pySCPI program. to facilitate to control of SCPI 
capable module sproduced by Pumpkin Inc. This program utalizes the Aardvark 
device manufactured by Total Phase.

Author: David Wright

(c) Pumpkin Inc. 2017
"""

import sys
sys.path.insert(0, 'src/')
from Tkinter import *
from tkFileDialog import *
from aardvark_builder import *
from pySCPI_config import *       
import platform
import threading
from PIL import Image, ImageTk

"""
Disable the function of all the buttons on the GUI except the one requested 
and then reenable them.

@param[in]  state (string): 'Lock':   Lock all buttons except the active_button
                            'Unlock': Unlock all of the buttons
@param[in]  active_button:  Optional-The button not to lock (tkinter.Button).
"""  
def action_lock(state, active_button=None):
    # list of all the buttons
    button_list = [readme_button, xml_button, aardvark_button, save_button, logging_button]
    if (state == 'Lock'):
        # lock the bottons
        for button in button_list:
            if (button != active_button):
                # lock this button
                button.config(state = DISABLED)
            # end if
        # end for
    elif (state == 'Unlock'):
        # Unlock all the buttons
        for button in button_list:
            button.config(state = NORMAL, background = default_color)
        # end for
    # end if
# end def

# Event used to trigger the termination of threads
kill_event = threading.Event()

"""
Kill all threads and close the program.
"""  
def kill_threads():
    kill_event.set()
    root.destroy()
# end def

"""
Kill all threads, intended for use with the logging thread.
"""  
def kill_log():
    kill_event.set()
# end

"""
Wrapper for the I2C writing thread to control the startup and shut down of 
the thread.

@param[in]  exit_event:   Event to terminate the function (threading.Event).
@param[in]  command_list: List of commands to be sent (list of strings).
@param[in]  addr_num:     I2C address of the slave device (int).
@param[in]  delay_time:   Millisecond delay to wait between transmissions (int).
@param[in]  ascii_time:   Millisecond delay to wait before reading an 'ascii' 
                          request (int).
@param[in]  float_dp:     The number of decimal places to print a float to (int).
"""  
def I2C_thread(exit_event, command_list, addr_num, delay_time, ascii_time, float_dp):
    # write via the Aardvark
    write_aardvark(exit_event, command_list, addr_num, delay_time, ascii_time, float_dp)
    # clear the thread termination flag
    exit_event.clear()
    # unlock all of the GUI buttons
    action_lock('Unlock')
# end def


"""
Wrapper for the logging thread to control the startup and shut down of 
the thread.

@param[in]  exit_event:   Event to terminate the function (threading.Event).
@param[in]  command_list: List of commands to be sent (list of strings).
@param[in]  addr_num:     I2C address of the slave device (int).
@param[in]  delay_time:   Millisecond delay to wait between transmissions (int).
@param[in]  ascii_time:   Millisecond delay to wait before reading an 'ascii' 
                          request (int).
@param[in]  float_dp:     The number of decimal places to print a float to (int).
@param[in]  logging_p:    Period of the logging task in seconds (int)
@param[in]  filename:     absolute directory of the file to log to (string).
"""  
def I2C_log_thread(exit_event, command_list, addr_num, delay_time, ascii_time, float_dp, logging_p, filename):
    # Change the role of the logging button so that it stops logging
    logging_button.config(state = NORMAL, text = 'Stop Logging', command = kill_log)
    # start logging
    log_aardvark(exit_event, command_list, addr_num, delay_time, ascii_time, float_dp, logging_p, filename, output_text)
    # clear the flag that stopped logging
    exit_event.clear()
    # unlock all GUI buttons
    action_lock('Unlock')
    # Reset the logging button back to it's initial state
    logging_button.config(text = 'Start Logging', command = start_logging)
# end def


"""
Function to command the I2C writing thread to start if all tests are passed.
"""
# Function to call to write through the AArdvark:
def Write_I2C():
    # Lock all buttons
    action_lock('Lock', None)
    aardvark_button.config(background = 'green')
    
    # clear output
    output_text.config(state=NORMAL)
    output_text.delete('1.0', END)
    output_text.config(state=DISABLED) 
    
    # determine delay
    delay_text = delay.get()
    delay_time = default_delay;
    if delay_text.isdigit():
        # is a good delay
        delay_time = int(delay_text)
    else:
        print '*** Requested delay is not valid, reverting to default ***'
        delay.delete(0,END)
        delay.insert(0, str(default_delay))
    # end if
    
    # determine ascii delay
    ascii_text = ascii.get()
    ascii_time = default_delay*4;
    if ascii_text.isdigit():
        # is a good delay
        ascii_time = int(ascii_text)
    else:
        print '*** Requested ascii delay is not valid, reverting to default ***'
        ascii.delete(0,END)
        ascii.insert(0, str(default_delay*4))
    # end if 
    
    # determine I2C address to write to
    addr_string = addr_text.get()
    addr_num = 0
    if addr_string.startswith('0x') and (len(addr_string) == 4) and addr_string[2:3].isdigit():
        # is a good address
        addr_num = int(addr_string,0)
    else:
        print '*** Invlaid address entered, reverting to device default ***'
        addr_string = address_of[slave_var.get()]
        addr_var.set(addr_string)
        addr_num = int(addr_string,0)
    # end if
    
    # get command list from GUI
    input_string = Command_text.get('1.0', END).encode('ascii', 'ignore')
    input_list = input_string.split('\n')
    command_list = []
    for item in input_list:
        # add all acceptible command to the list
        item = item.strip()
        if item != '':
            command_list = command_list + [item]
        # end if
    # end for
    
    # start the thread to perform the writing
    write_thread = threading.Thread(target = I2C_thread, args=(kill_event, command_list, addr_num, delay_time, ascii_time, float_var.get()))
    write_thread.start()
# end def

"""
Function to command the loggingthread to start if all tests are passed.
"""
def start_logging():
    # lock all the GUI buttons
    action_lock('Lock', None)
    logging_button.config(background = 'green')
    
    # clear output
    output_text.config(state=NORMAL)
    output_text.delete('1.0', END)
    output_text.config(state=DISABLED) 
    
    # determine delay
    delay_text = delay.get()
    delay_time = default_delay;
    if delay_text.isdigit():
        # delay is good
        delay_time = int(delay_text)
    else:
        print '*** Requested delay is not valid, reverting to default ***'
        delay.delete(0,END)
        delay.insert(0, str(default_delay))
    # end if
    
    # determine ascii delay
    ascii_text = ascii.get()
    ascii_time = default_delay*4;
    if ascii_text.isdigit():
        # delay is good
        ascii_time = int(ascii_text)
    else:
        print '*** Requested ascii delay is not valid, reverting to default ***'
        ascii.delete(0,END)
        ascii.insert(0, str(default_delay*4))
    # end if 
    
    # determine I2C address to write to
    addr_string = addr_text.get()
    addr_num = 0
    if addr_string.startswith('0x') and (len(addr_string) == 4) and addr_string[2:3].isdigit():
        # address is good
        addr_num = int(addr_string,0)
    else:
        print '*** Invlaid address entered, reverting to device default ***'
        addr_string = address_of[slave_var.get()]
        addr_var.set(addr_string)
        addr_num = int(addr_string,0)
    # end if
    
    # get command list
    input_string = Command_text.get('1.0', END).encode('ascii', 'ignore')
    input_list = input_string.split('\n')
    command_list = []
    for item in input_list:
        # add all commands to a list
        item = item.strip()
        if item != '':
            command_list = command_list + [item]
        # end if
    # end for
    
    # find the required loop period
    loop_time = 0
    for command in command_list:
        # add up the time of all the commands in the list
        if 'ascii' in command:
            # is ascii
            loop_time += (ascii_time + delay_time)
        elif 'TEL?' in command:
            # is telemetry
            loop_time += (2*delay_time)
        else:
            # is just a command
            loop_time += delay_time
        # end if
    # end for
    
    # evaluate the perscribed loop period
    logging_text = logging.get()
    logging_time = (loop_time/1000)+1;
    if logging_text.isdigit():
        # delay is a number
        logging_time = int(logging_text)
    else:
        print '*** Requested logging period is not valid, reverting to default ***'
        logging.delete(0,END)
        logging.insert(0, str(logging_time))
    # end if
    
    if logging_time*1000.0 <= loop_time*1.2:
        print '*** Warning, logging period may be shorter than the dration of the commands requested ***'
    # end if
    
    # open a save file window
    file_opt = options = {}
    options['defaultextension'] = '.csv'
    options['filetypes'] = [('csv files', '.csv')]
    options['initialdir'] = os.getcwd() + '\\log_files'
    options['initialfile'] = 'example_log.csv'
    options['title'] = 'Save .csv log file as:'       
    
    filename_full = asksaveasfilename(**file_opt)
    
    if (filename_full == ''):
        # No file was selected
        output_text.config(state=NORMAL)
        output_text.delete('1.0', END)
        output_text.config(state=DISABLED)        
        print '*** No Logging filename selected ***'
        # unlock buttons
        action_lock('Unlock')
    else: 
        # start the logging thread
        log_thread = threading.Thread(target = I2C_log_thread, args=(kill_event, command_list, addr_num, delay_time, ascii_time, float_var.get(), logging_time, filename_full))
        log_thread.start()
    # end if
# end def


"""
Function to display the readme file in the GUI window.
"""
def View_Readme():
    # lock buttons
    action_lock('Lock', readme_button)
    # clear output
    output_text.config(state=NORMAL)
    output_text.delete('1.0', END)
    output_text.config(state=DISABLED) 
    
    # read all lines from the readme
    with open('src/pySCPI README.txt', 'r') as f:
        content = f.readlines() 
    # end with
    
    # print each line to the gui
    for line in content:
        print line.rstrip()
    # end for
    
    # unlock buttons
    action_lock('Unlock')
# end def


"""
Function to start the process of saving the commands to xml.
"""
def Write_XML():
    # lock buttons
    action_lock('Lock', save_button)
    # clear output
    output_text.config(state=NORMAL)
    output_text.delete('1.0', END)
    output_text.config(state=DISABLED) 
    
    # determine delay
    delay_text = delay.get()
    delay_time = default_delay;
    if delay_text.isdigit():
        # delay is good
        delay_time = int(delay_text)
    else:
        print '*** Requested delay is not valid, reverting to default ***'
        delay.delete(0,END)
        delay.insert(0, str(default_delay))
    # end if
    
    # determine ascii delay
    ascii_text = ascii.get()
    ascii_time = default_delay*4;
    if ascii_text.isdigit():
        # delay is good
        ascii_time = int(ascii_text)
    else:
        print '*** Requested ascii delay is not valid, reverting to default ***'
        ascii.delete(0,END)
        ascii.insert(0, str(default_delay*4))
    # end if    
      
    # determine I2C address to write to
    addr_string = addr_text.get()
    addr_num = 0
    if addr_string.startswith('0x') and (len(addr_string) == 4) and addr_string[2:3].isdigit():
        # address is good
        addr_num = int(addr_string,0)
    else:
        print '*** Invlaid address entered, reverting to device default ***'
        addr_string = address_of(slave_var.get())
        addr_var.set(addr_string)
        addr_num = int(addr_string,0)
    # end if
    
    # get command list
    input_string = Command_text.get('1.0', END).encode('ascii', 'ignore')
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
    filename = create_XML(command_list, addr_string, delay_time, ascii_time)
    
    # update the filename display window to show the filename saved
    file_window.config(state=NORMAL)
    file_window.delete('1.0', END)
    file_window.insert(INSERT, filename.split('/')[-1])
    file_window.config(state = DISABLED)
    file_window.tag_configure('center', justify = 'center')
    file_window.tag_add('center', '1.0', END)     
    
    # unlock the buttons
    action_lock('Unlock')
# end def


"""
Function to load a command set, delays and address from a saved xml file
"""
def Load_XML():
    # lock the buttons
    action_lock('Lock', xml_button)   
    
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
    filename = askopenfilename(**file_opt)

    commands = []
    config_found = False
    ascii_last = 0
    ascii_delay = '0'
    message_delay = '0'
    device_detected = ''
    printed = False
    
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
                    delay.delete(0,END)
                    message_delay = slices[0]
                    delay.insert(0, message_delay)
                else:
                    # is an ascii delay
                    ascii_delay = slices[0]
                # end
            elif line.startswith('<i2c_write'):
                # finding address
                index = line.index('"')
                address = '0x' + line[index+3:index+5]
                addr_var.set(address)
                
                # create local address dictionary to compare to
                local_address_of = address_of.copy()
                local_address_of['GPS'] = '0x51'
                
                if device_detected in local_address_of.keys():
                    if address == local_address_of[device_detected]:
                        # address matches a device
                        if device_detected == 'GPS':
                            slave_var.set('GPSRM')
                        else:
                            slave_var.set(device_detected)
                        # end if
                    else:
                        # address does not so color it yellow as a warning
                        addr_text.config(background = 'yellow') 
                        if not printed:
                            print '*** Warning, loaded device address does not match default for that device ***'
                            printed = True
                        # end if
                    # end if  
                else:
                    if address in address_of.values():
                        # address matches a device
                        slave_var.set(address_of.keys()[address_of.values().index(address)])
                    else:
                        # address does not so color it yellow as a warning
                        addr_text.config(background = 'yellow') 
                        if not printed:
                            print '*** Warning, loaded device address does not match default for that device ***'
                            printed = True
                        # end if
                    # end if
                # end if
            # end if
        # end if
        
        
        if (ascii_delay == '0') or (ascii_delay == message_delay):
            # if ascii delay is too short, go to the default delay
            ascii_delay = 4*int(message_delay)
        # end if
        ascii.delete(0,END)
        ascii.insert(0, ascii_delay)    
        
        # update the filename display window to show the filename loaded   
        file_window.config(state = NORMAL)
        file_window.delete('1.0', END)
        file_window.insert(INSERT, filename.split('/')[-1])
        file_window.config(state = DISABLED)
        file_window.tag_configure('center', justify = 'center')
        file_window.tag_add('center', '1.0', END)    
        
        
        # empty command box and add new commands
        Command_text.delete('1.0', END)
        Command_text.insert(INSERT, '\n'.join(commands))
        xml.close()
    else:
        output_text.config(state=NORMAL)
        output_text.delete('1.0', END)
        output_text.config(state=DISABLED)        
        print '*** No file given to Load ***'
    # end if
    
    # unlock buttons
    action_lock('Unlock')
# end def

################################ GUI defaults ##################################
default_color = '#E1E5E7'
title_font = "Arial 16 bold"
label_font = "Arial 10"
button_font = "Arial 10 bold"
text_font = "Arial 9"
                   
root = Tk()
root.geometry('1000x600')
root.config(bg = 'white') # to show through the gaps between frames
current_column = 0

############################ Parent Frames #####################################
# Frame for the header image
Header = Frame(root)
Header.config(bg = default_color)
Header.grid(row = 0, column = 0, columnspan = 2, sticky = NSEW)

# Frame for the configuration options
Config_frame = Frame(root)
Config_frame.config(bg = default_color)
Config_frame.grid(row = 1, column = 0, columnspan = 2, sticky = NSEW, pady = 2)

# frame for the inputs
Input_frame = Frame(root)
Input_frame.config(bg = default_color)
Input_frame.grid(row = 2, column = 0, sticky = NSEW, padx = 1)

# Frame for the outputs
Output_frame = Frame(root)
Output_frame.config(bg = default_color)
Output_frame.grid(row = 2, column = 1, sticky = NSEW, padx = 1)

################################ Header Image ##################################

input_image = Image.open('src/Header.jpg')
# find the images aspect ratio so it can be maintained
aspect_ratio = float(input_image.size[1])/float(input_image.size[0])
# resize to fit the window
header_image = input_image.resize((1000, int(1000*aspect_ratio)), Image.ANTIALIAS)
image_copy = header_image.copy()


"""
Event function to auto-resize the header image with the window

TODO try and speed up this function
"""
def resize_image(event):
    # find new geometry
    new_width = event.width
    new_height = int(new_width * aspect_ratio)
    # resize
    header_image = input_image.resize((new_width, new_height), Image.ANTIALIAS)
    # snap the Frame rows around it
    root.rowconfigure(0, minsize = new_height)
    Header.rowconfigure(0, minsize = new_height)
    # load the new image
    header_photo = ImageTk.PhotoImage(header_image)
    image_label.config(image = header_photo)
    image_label.image = header_photo
# end def

# Header Image
header_photo = ImageTk.PhotoImage(header_image)
image_label = Label(Header, image=header_photo)
Header.bind('<Configure>', resize_image) # link the resizing event
image_label.grid(row = 0, column = 0, sticky = NSEW)

##################### Configuration Elements #############################
## Configuration title
#config_header = Label(Config_frame, text = 'Configuration:')
#config_header.config(font=title_font, bg = default_color)
#config_header.grid(row = 0, column = 1, columnspan = 5)

# sub-frame for the buttons
but_frame = Frame(Config_frame)
but_frame.config(bg = default_color)
but_frame.grid(row = 0, column = current_column, rowspan = 3, padx = 10)
but_frame.columnconfigure(0, weight = 1)

# Load XML Button
xml_button = Button(but_frame, text = 'Load Commands', command = Load_XML, activebackground = 'green', width = 15)
xml_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
xml_button.grid(row = 0, column=0, padx = 5)

# View README Button
readme_button = Button(but_frame, text = 'View ReadMe', command = View_Readme, activebackground = 'green', width = 15)
readme_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
readme_button.grid(row = 1, column=0, padx = 5, pady = 5)
current_column += 1

# Slave Address selection options
def update_addr(value):
    addr_var.set(address_of[value])
    addr_text.config(background = 'white')
# end

# Slave Device selector sub-frame
slave_frame = Frame(Config_frame)
slave_frame.config(bg = default_color)
slave_frame.grid(row = 2, column = current_column, padx = 5, sticky = NSEW)
slave_frame.columnconfigure(0,weight = 2)
slave_frame.columnconfigure(1,weight = 2)

# Slave selector title
slave_label = Label(Config_frame, text = 'Slave Device')
slave_label.config(font = label_font, bg = default_color)
slave_label.grid(row = 1, column= current_column, sticky = S)

# device name variable
devices = get_devices()
slave_var = StringVar(root)
slave_var.set(devices[0])

# device address variable
addr_var = StringVar(root)
addr_var.set(address_of[devices[0]])

# device address display box
addr_text = Entry(slave_frame, textvariable=addr_var, width = 4, justify = CENTER)
addr_text.config(font = text_font, highlightbackground= default_color)
addr_text.grid(row = 0, column = 1, ipadx=20, pady = 5,sticky = W, ipady = 3)

# device selector drop down menu
slave_menu = OptionMenu(slave_frame, slave_var, *tuple(devices), command = update_addr)
if (platform.system == 'Windows'):
    # Size differently depending on the OS
    slave_menu.config(width = 1, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
else:
    slave_menu.config(width = 4, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
# end if
slave_menu["menu"].config(font = label_font, bg = default_color)
slave_menu.grid(row = 0, column = 0, sticky = E, ipadx=20)
current_column += 1

# delay text box sub-frame
delay_frame = Frame(Config_frame)
delay_frame.config(bg = default_color)
delay_frame.grid(row = 2, column = current_column, sticky = EW)
delay_frame.columnconfigure(0, weight = 2)
delay_frame.columnconfigure(1, weight = 2)

# delay title
delay_label = Label(Config_frame, text = 'Intermessage Delay')
delay_label.grid(row = 1, column = current_column, padx = 5, sticky = S)
delay_label.config(font = label_font, bg = default_color)

# delay entry box
delay = Entry(delay_frame, justify = RIGHT, width = 7)
delay.config(font = text_font, highlightbackground= default_color)
delay.grid(row = 0, column = 0, ipady = 3, sticky = E)
delay.insert(0, str(default_delay))

# delay units deiplay
delay_units = Label(delay_frame, text = 'ms')
delay_units.config(font = text_font, bg = default_color)
delay_units.grid(row = 0, column = 1, sticky = W)
current_column += 1

# ASCII Delay sub-frame
ascii_frame = Frame(Config_frame)
ascii_frame.config(bg = default_color)
ascii_frame.grid(row = 2, column = current_column, sticky = EW)
ascii_frame.columnconfigure(0, weight = 2)
ascii_frame.columnconfigure(1, weight = 2)

# ascii delay title
ascii_label = Label(Config_frame, text = 'ASCII Message Delay')
ascii_label.config(font = label_font, bg = default_color)
ascii_label.grid(row = 1, column=current_column, sticky = S)

# ascii delay entry box
ascii = Entry(ascii_frame, justify = RIGHT, width = 7)
ascii.config(font = text_font, highlightbackground= default_color)
ascii.grid(row = 0, column=0, ipady = 3, sticky = E)
ascii.insert(0, str(default_delay*4))

# ascii units display
ascii_units = Label(ascii_frame, text = 'ms')
ascii_units.config(font = text_font, bg = default_color)
ascii_units.grid(row = 0, column = 1, sticky = W)
current_column += 1

# ouput float size selector title
float_label = Label(Config_frame, text = 'Float DP')
float_label.config(font = label_font, bg = default_color)
float_label.grid(row = 1, column=current_column, sticky = S)

# float size variable
float_var = IntVar(root)
float_var.set(default_dp)

# float size drop down menu
float_menu = OptionMenu(Config_frame, float_var, 1,2,3,4,5,6,7,8,9,10,11,12)
if platform.system() == 'Windows':
    # adjust size for different OSs
    float_menu.config(width = 1, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
else:
    float_menu.config(width = 7, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
    float_menu["menu"].config(fg = 'black')
# end if
float_menu["menu"].config(font = label_font, bg = default_color)
float_menu.grid(row = 2, column = current_column)
current_column += 1  

# Logging period sub-frame
logging_frame = Frame(Config_frame)
logging_frame.config(bg = default_color)
logging_frame.grid(row = 2, column = current_column, sticky = EW)
logging_frame.columnconfigure(0, weight = 2)
logging_frame.columnconfigure(1, weight = 2)

#logging period title
logging_label = Label(Config_frame, text = 'Logging Period')
logging_label.config(font = label_font, bg = default_color)
logging_label.grid(row = 1, column=current_column, padx = 5, sticky = S)

# logging period entry box
logging = Entry(logging_frame, justify = RIGHT, width = 7)
logging.config(font = text_font, highlightbackground= default_color)
logging.grid(row = 0, column=0, ipady = 3, sticky = E)
logging.insert(0, '60')

# logging period unit display
logging_units = Label(logging_frame, text = 's')
logging_units.config(font = text_font, bg = default_color)
logging_units.grid(row = 0, column = 1, sticky = W)
current_column += 1  

# error count sub-frame
error_frame = Frame(Config_frame)
error_frame.config(bg = default_color)
error_frame.grid(row = 2, column = current_column, sticky = EW, padx = 10)
error_frame.columnconfigure(0, weight = 2)
error_frame.columnconfigure(1, weight = 2)

# error count title
error_label = Label(Config_frame, text = 'Error count')
error_label.config(font = label_font, bg = default_color)
error_label.grid(row = 1, column=current_column, padx = 5, sticky = S)

# error count entry box
errors = Entry(error_frame, justify = CENTER, width = 7)
errors.config(font = text_font, highlightbackground= default_color, disabledforeground = 'black', disabledbackground = 'white')
errors.grid(row = 0, column=0, ipady = 3, sticky = E)
errors.insert(0, '0')
errors.config(state = DISABLED)

def zero_errors():
    errors.config(state = NORMAL, disabledforeground = 'black')
    errors.delete(0,END)
    errors.insert(0, '0')     
    errors.config(state = DISABLED)
# end

def add_error():
    current = int(errors.get())
    errors.config(state = NORMAL, disabledforeground = 'red')
    errors.delete(0,END)
    errors.insert(0, str(current + 1))     
    errors.config(state = DISABLED)  
# end

# error clearing button
error_button = Button(error_frame, text = 'Zero', command = zero_errors, activebackground = 'green', width = 5)
error_button.config(font = label_font, bg = default_color, highlightbackground= default_color)
error_button.grid(row = 0, column=1, sticky = W)


############################ Inputs Section ####################################

# Input header sub-frame
input_header_frame = Frame(Input_frame)
input_header_frame.config(bg = default_color)
input_header_frame.grid(row = 0, column = 0, sticky = NSEW)

# input title
input_header = Label(input_header_frame, text = 'Input Commands:')
input_header.config(font=title_font, bg = default_color)
input_header.grid(row = 0, column = 0, sticky = W, padx = 5)

# file text_box
file_window = Text(input_header_frame, height = 1, width = 33)
file_window.config(font = text_font, bg = default_color, state = DISABLED, highlightbackground= default_color)
file_window.grid(row = 0, column=1, ipady = 3, sticky = E)

"""
Event function to clear the filename wnidow if the commands are edited
"""
def key(event):
    # when a key is pressed within the command text frame, wipe the filename
    file_window.config(state = NORMAL)
    file_window.delete('1.0', END)
    file_window.config(state = DISABLED)  
# end def

# Command input sub-frame
command_frame = Frame(Input_frame)
command_frame.config(bg = default_color)
command_frame.grid(row = 1, column = 0, sticky = NSEW)

# text box to enter commands into
Command_text = Text(command_frame, height = 10, width = 58, padx = 3, pady = 3)
Command_text.config(font = text_font, highlightbackground= default_color)
Command_text.insert(INSERT, '\n'.join(default_commands))
Command_text.bind('<Key>', key)
Command_text.grid(row = 0, column=0, sticky = NSEW)

# scrollbar for the command text box, linked to the text box
command_scroll = Scrollbar(command_frame, command = Command_text.yview)
command_scroll.grid(column = 1, row = 0, sticky = NSEW)
Command_text['yscrollcommand'] = command_scroll.set

# Buttons subframe
button_frame = Frame(Input_frame)
button_frame.config(bg = default_color)
button_frame.grid(row = 2, column = 0, sticky = NSEW)

# Write XML Button
save_button = Button(button_frame, text = 'Save Commands', command = Write_XML, activebackground = 'green', width = 13)
save_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
save_button.grid(row = 0, column=0, pady = 5, padx = 10, sticky = EW)
button_frame.columnconfigure(0, weight = 1)

# Use Aardvark Button
aardvark_button = Button(button_frame, text = 'Send Commands', command = Write_I2C, activebackground = 'green', width = 13)
aardvark_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
aardvark_button.grid(row = 0, column=1, pady = 5, sticky = EW)
button_frame.columnconfigure(1, weight = 1)

# Logging button
logging_button = Button(button_frame, text = 'Start Logging', command = start_logging, activebackground = 'green', width = 13)
logging_button.config(font = button_font, bg = default_color, highlightbackground= default_color)
logging_button.grid(row = 0, column=2, pady = 5, padx = 10, sticky = EW)
button_frame.columnconfigure(2, weight = 1)

############################## Output Frame ####################################
# Output title
output_label = Label(Output_frame, text = 'Output:')
output_label.config(font=title_font, bg = default_color)
output_label.grid(row = 0, column = 0, columnspan = 2)

# output text box
output_text = Text(Output_frame, height = 20, width = 100, padx = 3, pady = 3)
output_text.config(font = text_font, highlightbackground= default_color)
output_text.grid(row = 1, column=0, sticky = 'NESW')
output_text.config(state=DISABLED, wrap=WORD)

# scrolbar for the output textbox, linked to the text box
output_scroll = Scrollbar(Output_frame, command = output_text.yview)
output_scroll.grid(column = 1, row = 1, sticky = 'NESW')
output_text['yscrollcommand'] = output_scroll.set

# highlight tag
output_text.tag_config('error', foreground = 'red')

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
root.rowconfigure(2, weight = 2)

# allow for resizing of the otuput frame column
Output_frame.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 5, minsize = 200)

# set window minsize to prevent objects crashing
root.minsize(width = 900, height = 500)


"""
Class to handle the re-mapping of stdout to the GUI
"""
class GUI_Writer(object):
    def __init__(self, widget):
        self.output_text = widget
    # end def
        
    # what to do when a 'print' command is issued 
    def write(self, string):
        self.output_text.config(state=NORMAL)
        if string.startswith('*'):
            self.output_text.insert(INSERT, string, 'error')
            add_error()
        else:
            self.output_text.insert(INSERT, string)
        # end
        self.output_text.config(state=DISABLED)
    # end def
# end class

# remap stdout to the GUI
sys.stdout = GUI_Writer(output_text)

# define icon
root.iconbitmap(r'src/cubesatkit.ico')

# define window title
root.title("PySCPI: PC control of pumpkin SCPI modules")
root.protocol("WM_DELETE_WINDOW", kill_threads)

# start the GUI
mainloop()