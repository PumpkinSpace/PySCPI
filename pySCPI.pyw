#!/usr/bin/env python
# Aardvark batch script writer
# Pumpkin Inc.
# David Wright 2016
import sys
sys.path.insert(0, 'src/')
from Tkinter import *
from tkFileDialog import *
from aardvark_builder import *
from pySCPI_config import *       
import platform
import threading
from PIL import Image, ImageTk

def action_lock(state, active_button=None):
    button_list = [readme_button, xml_button, aardvark_button, save_button]
    if (state == 'Lock'):
        for button in button_list:
            if (button != active_button):
                button.config(state = DISABLED)
            # end
        # end
    elif (state == 'Unlock'):
        for button in button_list:
            button.config(state = NORMAL)
        # end
    # end
# end

THREAD_EXIT = False

def kill_threads():
    THREAD_EXIT = True
    root.destroy()
# end

def I2C_thread(command_list, addr_num, delay_time, ascii_time, float_dp):
    write_aardvark(command_list, addr_num, delay_time, ascii_time, float_dp, THREAD_EXIT)
    action_lock('Unlock')
    aardvark_button.config(background = default_color)
# end


# Function to call to write through the AArdvark:
def Write_I2C():
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
        delay_time = int(delay_text)
    else:
        print '*** Requested delay is not valid, reverting to default ***'
        delay.delete(0,END)
        delay.insert(0, str(default_delay))
    # end
    
    # determine ascii delay
    ascii_text = ascii.get()
    ascii_time = default_delay*4;
    if ascii_text.isdigit():
        ascii_time = int(ascii_text)
    else:
        print '*** Requested ascii delay is not valid, reverting to default ***'
        ascii.delete(0,END)
        ascii.insert(0, str(default_delay*4))
    # end    
    
    # determine I2C address to write to
    addr_string = addr_text.get()
    addr_num = 0
    if addr_string.startswith('0x') and (len(addr_string) == 4) and addr_string[2:3].isdigit():
        addr_num = int(addr_string,0)
    else:
        print '*** Invlaid address entered, reverting to device default ***'
        addr_string = address_of(slave_var.get())
        addr_num = int(addr_string,0)
    # end
    
    # get command list
    input_string = Command_text.get('1.0', END).encode('ascii', 'ignore')
    input_list = input_string.split('\n')
    command_list = []
    for item in input_list:
        item = item.strip()
        if item != '':
            command_list = command_list + [item]
        # end
    # end
    write_thread = threading.Thread(target = I2C_thread, args=(command_list, addr_num, delay_time, ascii_time, float_var.get()))
    write_thread.start()
# end

# Function to call to write XML:
def View_Readme():
    action_lock('Lock', readme_button)
    # clear output
    output_text.config(state=NORMAL)
    output_text.delete('1.0', END)
    output_text.config(state=DISABLED) 
    
    with open('src/pySCPI README.txt') as f:
        content = f.readlines() 
    # end
    
    for line in content:
        print line.rstrip()
    # end
    action_lock('Unlock')
# end

# Function to call to write XML:
def Write_XML():
    action_lock('Lock', save_button)
    # clear output
    output_text.config(state=NORMAL)
    output_text.delete('1.0', END)
    output_text.config(state=DISABLED) 
    
    # determine delay
    delay_text = delay.get()
    delay_time = default_delay;
    if delay_text.isdigit():
        delay_time = int(delay_text)
    else:
        print '*** Requested delay is not valid, reverting to default ***'
        delay.delete(0,END)
        delay.insert(0, str(default_delay))
    # end
    
    # determine ascii delay
    ascii_text = ascii.get()
    ascii_time = default_delay*4;
    if ascii_text.isdigit():
        ascii_time = int(ascii_text)
    else:
        print '*** Requested ascii delay is not valid, reverting to default ***'
        ascii.delete(0,END)
        ascii.insert(0, str(default_delay*4))
    # end       
      
    # determine I2C address to write to
    addr_string = addr_text.get()
    addr_num = 0
    if addr_string.startswith('0x') and (len(addr_string) == 4) and addr_string[2:3].isdigit():
        addr_num = int(addr_string,0)
    else:
        print '*** Invlaid address entered, reverting to device default ***'
        addr_string = address_of(slave_var.get())
        addr_num = int(addr_string,0)
    # end
    
    # get command list
    input_string = Command_text.get('1.0', END).encode('ascii', 'ignore')
    input_list = input_string.split('\n')
    command_list = []
    for item in input_list:
        item = item.strip()
        if item != '':
            command_list = command_list + [item]
        # end
    # end
            
    filename = create_XML(command_list, addr_string, delay_time, ascii_time, output_text)
    
    file_window.config(state = NORMAL)
    file_window.delete('1.0', END)
    file_window.insert(INSERT, filename.split('/')[-1])
    file_window.config(state = DISABLED)
    file_window.tag_configure('center', justify = 'center')
    file_window.tag_add('center', '1.0', END)        
    action_lock('Unlock')
# end

# Function to load commands from an XML file
def Load_XML():
    action_lock('Lock', xml_button)   
    file_opt = options = {}
    options['defaultextension'] = '.xml'
    options['filetypes'] = [('xml files', '.xml')]
    options['initialdir'] = os.getcwd() + '/xml_files'
    dir_list = os.listdir(os.getcwd() + '/xml_files')
    if 'aardvark_script.xml' in dir_list or dir_list == []:
        options['initialfile'] = 'aardvark_script.xml'
    else:
        options['initialfile'] = dir_list[1]
    options['title'] = 'Select .xml file to open'   
    
    filename = askopenfilename(**file_opt)

    commands = []
    config_found = False
    ascii_last = 0
    ascii_delay = '0'
    message_delay = '0'
    
    if (filename != ''): 
        # extract all commands from XML if present
        xml = open(filename, 'r')
        xml_strip = [line.strip() for line in xml]
        for line in xml_strip:
            if line.startswith('<!--'):
                if config_found:
                    commands = commands + [line[4:-3]]
                else:
                    config_found = True
                # end
                if ('ascii' in line):
                    ascii_last = 1
                else:
                    ascii_last = 0
                # end            
            elif line.startswith('<sleep'):
                # delay found
                slices = [s for s in line.split('"') if s.isdigit()]
                if (ascii_last == 0):
                    delay.delete(0,END)
                    message_delay = slices[0]
                    delay.insert(0, message_delay)
                else:
                    ascii_delay = slices[0]
                # end
            elif line.startswith('<i2c_write'):
                #finding address
                index = line.index('"')
                address = '0x' + line[index+3:index+5]
                addr_var.set(address)
                if address in address_of.values():
                    slave_var.set(address_of.keys()[address_of.values().index(address)])
                else:
                    addr_text.config(background = 'yellow')    
                # end
    
            # end
        # end
        
        if (ascii_delay == '0') or (ascii_delay == message_delay):
            ascii_delay = 4*int(message_delay)
        # end
        ascii.delete(0,END)
        ascii.insert(0, ascii_delay)    
            
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
    # end
    action_lock('Unlock')
# end

default_color = '#E1E5E7'
title_font = "Arial 16 bold"
label_font = "Arial 11"
text_font = "Arial 9"
                   
root = Tk()
root.geometry('1000x600')
root.config(bg = 'white')
current_column = 0

######################## Parent Frames #####################################
Header = Frame(root)
Header.config(bg = default_color)
Header.grid(row = 0, column = 0, columnspan = 2, sticky = NSEW)

Config_frame = Frame(root)
Config_frame.config(bg = default_color)
Config_frame.grid(row = 1, column = 0, columnspan = 2, sticky = NSEW, pady = 2)

Input_frame = Frame(root)
Input_frame.config(bg = default_color)
Input_frame.grid(row = 2, column = 0, sticky = NSEW, padx = 1)

Output_frame = Frame(root)
Output_frame.config(bg = default_color)
Output_frame.grid(row = 2, column = 1, sticky = NSEW, padx = 1)

##################### Header Image #############################
# Header
input_image = Image.open('src/Header.jpg')
aspect_ratio = float(input_image.size[1])/float(input_image.size[0])
header_image = input_image.resize((1000, int(1000*aspect_ratio)), Image.ANTIALIAS)
image_copy = header_image.copy()

def resize_image(event):
    new_width = event.width
    new_height = int(new_width * aspect_ratio)
    header_image = image_copy.resize((new_width, new_height), Image.ANTIALIAS)
    root.rowconfigure(0, minsize = new_height)
    Header.rowconfigure(0, minsize = new_height)
    header_photo = ImageTk.PhotoImage(header_image)
    image_label.config(image = header_photo)
    image_label.image = header_photo
# end

# Header Image
header_photo = ImageTk.PhotoImage(header_image)
image_label = Label(Header, image=header_photo)
Header.bind('<Configure>', resize_image)
image_label.grid(row = 0, column = 0, sticky = NSEW)

##################### Configuration Elements #############################


config_header = Label(Config_frame, text = 'Configuration:')
config_header.config(font=title_font, bg = default_color)
config_header.grid(row = 0, column = 0, columnspan = 7)

# Load XML Button
xml_button = Button(Config_frame, text = 'Load\nXML', command = Load_XML, activebackground = 'green')
xml_button.config(font = label_font, bg = default_color)
xml_button.grid(row = 1, column=current_column, rowspan = 2, padx = 5)
current_column += 1

# View README Button
readme_button = Button(Config_frame, text = 'View\nReadMe', command = View_Readme, activebackground = 'green')
readme_button.config(font = label_font, bg = default_color)
readme_button.grid(row = 1, column=current_column, rowspan = 2)
current_column += 1

# Slave Address selection options
def update_addr(value):
    addr_var.set(address_of[value])
    addr_text.config(background = 'white')
# end

# Slave Device selector
slave_frame = Frame(Config_frame)
slave_frame.config(bg = default_color)
slave_frame.grid(row = 2, column = current_column, rowspan = 2, padx = 5, sticky = NSEW)

slave_label = Label(Config_frame, text = 'Slave Device')
slave_label.config(font = label_font, bg = default_color)
slave_label.grid(row = 1, column= current_column, pady = 5)
devices = get_devices()
slave_var = StringVar(root)
slave_var.set(devices[0])
addr_var = StringVar(root)
addr_var.set(address_of[devices[0]])
addr_text = Entry(slave_frame, textvariable=addr_var, width = 4, justify = CENTER)
addr_text.config(font = text_font)
addr_text.grid(row = 0, column = 1, ipadx=20, pady = 5, sticky = E, ipady = 3)

slave_menu = OptionMenu(slave_frame, slave_var, *tuple(devices), command = update_addr)
if (platform.system == 'Windows'):
    slave_menu.config(width = 1, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
else:
    slave_menu.config(width = 4, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
# end
slave_menu["menu"].config(font = label_font, bg = default_color)
slave_menu.grid(row = 0, column = 0, ipadx=20, sticky=W)
current_column += 1

# delay text_box
delay_frame = Frame(Config_frame)
delay_frame.config(bg = default_color)
delay_frame.grid(row = 2, column = current_column)
delay_frame.columnconfigure(0, weight = 2)

delay_label = Label(Config_frame, text = 'Intermessage Delay')
delay_label.grid(row = 1, column = current_column, padx = 5, pady = 5)
delay_label.config(font = label_font, bg = default_color)

delay = Entry(delay_frame, justify = RIGHT)
delay.config(font = text_font)
delay.grid(row = 0, column = 0, ipady = 3, sticky = E)
delay.insert(0, str(default_delay))

delay_units = Label(delay_frame, text = 'ms')
delay_units.config(font = text_font, bg = default_color)
delay_units.grid(row = 0, column = 1, sticky = W)
current_column += 1

# ASCII Delay box
ascii_frame = Frame(Config_frame)
ascii_frame.config(bg = default_color)
ascii_frame.grid(row = 2, column = current_column)
ascii_frame.columnconfigure(0, weight = 2)

ascii_label = Label(Config_frame, text = 'ASCII Delay')
ascii_label.config(font = label_font, bg = default_color)
ascii_label.grid(row = 1, column=current_column, pady = 5)

ascii = Entry(ascii_frame, justify = RIGHT)
ascii.config(font = text_font)
ascii.grid(row = 0, column=0, ipady = 3, sticky = E)
ascii.insert(0, str(default_delay*4))

ascii_units = Label(ascii_frame, text = 'ms')
ascii_units.config(font = text_font, bg = default_color)
ascii_units.grid(row = 0, column = 1, sticky = W)
current_column += 1

# ouput float size selector
float_label = Label(Config_frame, text = 'Float DP:')
float_label.config(font = label_font, bg = default_color)
float_label.grid(row = 1, column=current_column)
float_var = IntVar(root)
float_var.set(default_dp)
float_menu = OptionMenu(Config_frame, float_var, 1,2,3,4,5,6,7,8,9,10,11,12)
if platform.system() == 'Windows':
    float_menu.config(width = 1, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
else:
    float_menu.config(width = 5, bg = default_color, activebackground = default_color, highlightbackground= default_color, font = label_font)
# ends
float_menu["menu"].config(font = label_font, bg = default_color)
float_menu.grid(row = 2, column = current_column)
current_column += 1  

# Logging period box
logging_frame = Frame(Config_frame)
logging_frame.config(bg = default_color)
logging_frame.grid(row = 2, column = current_column)
logging_frame.columnconfigure(0, weight = 2)

logging_label = Label(Config_frame, text = 'Logging Period:')
logging_label.config(font = label_font, bg = default_color)
logging_label.grid(row = 1, column=current_column, padx = 5)

logging = Entry(logging_frame, justify = RIGHT)
logging.config(font = text_font)
logging.grid(row = 0, column=0, ipady = 3, sticky = EW)
logging.insert(0, '60')

logging_units = Label(logging_frame, text = 's')
logging_units.config(font = text_font, bg = default_color)
logging_units.grid(row = 0, column = 1, sticky = W)

############################ Inputs Section ####################################

# Input block
input_header_frame = Frame(Input_frame)
input_header_frame.config(bg = default_color)
input_header_frame.grid(row = 0, column = 0)


input_header = Label(input_header_frame, text = 'Input Commands:')
input_header.config(font=title_font, bg = default_color)
input_header.grid(row = 0, column = 0, sticky = W, padx = 5)

# file text_box
file_window = Text(input_header_frame, height = 1, width = 25)
file_window.config(font = text_font, bg = default_color, state = DISABLED)
file_window.grid(row = 0, column=1, ipady = 3, sticky = EW)

def key(event):
    # when a key is pressed within the command text frame, wipe the filename
    file_window.config(state = NORMAL)
    file_window.delete('1.0', END)
    file_window.config(state = DISABLED)  

# Command input text frame
command_frame = Frame(Input_frame)
command_frame.config(bg = default_color)
command_frame.grid(row = 1, column = 0, sticky = 'NESW')


Command_text = Text(command_frame, height = 10, width = 50, padx = 3, pady = 3)
Command_text.config(font = text_font)
Command_text.insert(INSERT, '\n'.join(default_commands))
Command_text.bind('<Key>', key)
Command_text.grid(row = 0, column=0, sticky = 'NESW')

command_scroll = Scrollbar(command_frame, command = Command_text.yview)
command_scroll.grid(column = 1, row = 0, sticky = 'NESW')
Command_text['yscrollcommand'] = command_scroll.set

# Buttons
button_frame = Frame(Input_frame)
button_frame.config(bg = default_color)
button_frame.grid(row = 2, column = 0, sticky = NSEW)

# Write XML Button
save_button = Button(button_frame, text = 'Write XML', command = Write_XML, activebackground = 'green')
save_button.config(font = label_font, bg = default_color)
save_button.grid(row = 0, column=0, pady = 5, padx = 10, sticky = EW)
button_frame.columnconfigure(0, weight = 1)

# Use Aardvark Button
aardvark_button = Button(button_frame, text = 'Send Commands', command = Write_I2C, activebackground = 'green')
aardvark_button.config(font = label_font, bg = default_color)
aardvark_button.grid(row = 0, column=1, pady = 5, sticky = EW)
button_frame.columnconfigure(1, weight = 1)

# Logging
logging_button = Button(button_frame, text = 'Start Logging', command = Write_I2C, activebackground = 'green')
logging_button.config(font = label_font, bg = default_color)
logging_button.grid(row = 0, column=2, pady = 5, padx = 10, sticky = EW)
button_frame.columnconfigure(2, weight = 1)



####################### Output Frame #################################
# Output text frame
output_label = Label(Output_frame, text = 'Output:')
output_label.config(font=title_font, bg = default_color)
output_label.grid(row = 0, column = 0, columnspan = 2)

output_text = Text(Output_frame, height = 20, width = 100, padx = 3, pady = 3)
output_text.config(font = text_font)
output_text.grid(row = 1, column=0, sticky = 'NESW')
output_text.config(state=DISABLED, wrap=WORD)
output_scroll = Scrollbar(Output_frame, command = output_text.yview)
output_scroll.grid(column = 1, row = 1, sticky = 'NESW')
output_text['yscrollcommand'] = output_scroll.set

# allow for resizing
Config_frame.columnconfigure(0, weight = 2, minsize = 60)
Config_frame.columnconfigure(1, weight = 2, minsize = 60)
Config_frame.columnconfigure(2, weight = 2, minsize = 200)
Config_frame.columnconfigure(3, weight = 2, minsize = 100)
Config_frame.columnconfigure(4, weight = 2, minsize = 80)
Config_frame.columnconfigure(5, weight = 2, minsize = 60)
Config_frame.columnconfigure(6, weight = 2, minsize = 80)

Input_frame.rowconfigure(1, weight = 2)
command_frame.rowconfigure(0, weight = 2)

Output_frame.rowconfigure(1, weight = 2)
root.rowconfigure(2, weight = 2)

Output_frame.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 5, minsize = 200)
root.minsize(width = 800, height = 500)

class GUI_Writer(object):
    def __init__(self, widget):
        self.output_text = widget

    def write(self, string):
        self.output_text.config(state=NORMAL)
        self.output_text.insert(INSERT, string)
        self.output_text.config(state=DISABLED)

sys.stdout = GUI_Writer(output_text)

# define icon
root.iconbitmap(r'src/cubesatkit.ico')

# define title
root.title("PySCPI: PC control of pumpkin SCPI modules")
root.protocol("WM_DELETE_WINDOW", kill_threads)

# start
mainloop()