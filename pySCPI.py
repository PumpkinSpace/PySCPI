#!/usr/bin/env python
# Aardvark batch script writer
# Pumpkin Inc.
# David Wright 2016

from Tkinter import *
from aardvark_builder import *
from pySCPI_config import *       

# Function to call to write through the AArdvark:
def Write_I2C():
    
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
    
    # determine filename
    name_text = name.get()
    if not name_text.endswith('.xml'):
        print '*** Requested file name is not valid, reverting to default ***'
        name.delete(0,END)
        name.insert(0,default_filename)
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
    
    write_aardvark(command_list, addr_num, delay_time)
# end

# Function to call to write XML:
def Write_XML():
    
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
    
    # determine filename
    name_text = name.get()
    if not name_text.endswith('.xml'):
        print '*** Requested file name is not valid, reverting to default ***'
        name.delete(0,END)
        name.insert(0,default_filename)
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
            
    create_XML(command_list, addr_string, delay_time, name_text)
# end

# Function to load commands from an XML file
def Load_XML():
    filename = name.get()

    commands = []
    config_found = False
     
    # extract all commands from XML if present
    if filename in os.listdir(os.getcwd()):
        xml = open(filename, 'r')
        xml_strip = [line.strip() for line in xml]
        for line in xml_strip:
            if line.startswith('<!--'):
                if config_found:
                    commands = commands + [line[4:-3]]
                else:
                    config_found = True
                # end
            elif line.startswith('<sleep'):
                # delay found
                slices = [s for s in line.split('"') if s.isdigit()]
                delay.delete(0,END)
                delay.insert(0, slices[0])
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
        
        # empty command box and add new commands
        Command_text.delete('1.0', END)
        Command_text.insert(INSERT, '\n'.join(commands))
        xml.close()
    else:
        # clear output
        output_text.config(state=NORMAL)
        output_text.delete('1.0', END)
        output_text.config(state=DISABLED)        
        print '*** Requested XML file not found ***'
    # end
# end
                    
root = Tk()
current_row = 0
# Header Image
image_file = PhotoImage(file = 'Pumpkin_Inc_Logo-medium.gif')
image_label = Label(root, image=image_file)
image_label.grid(row = current_row, column = 0, columnspan = 4)
current_row += 1

# Header
header = Label(root, text = 'I2C Command Writer')
header.config(font=("Courier", 22))
header.grid(row = current_row, column = 0, columnspan = 4)
current_row += 1

def update_addr(value):
    addr_var.set(address_of[value])
    addr_text.config(background = 'white')
# end
    
# Slave Device selector
slave_label = Label(root, text = 'Slave Device:')
slave_label.grid(row = current_row, column=0, rowspan = 1)
devices = get_devices()
slave_var = StringVar(root)
slave_var.set(devices[0])
addr_var = StringVar(root)
addr_var.set(address_of[devices[0]])
addr_text = Entry(root, textvariable=addr_var, width = 60, justify = RIGHT)
#addr_text.insert(INSERT, address_of[devices[0]])
addr_text.grid(row = current_row, column = 1, ipadx=20)

slave_menu = OptionMenu(root, slave_var, *tuple(devices), command = update_addr)
slave_menu.grid(in_=addr_text, sticky=E)
current_row += 1


# filename textbox
name_label = Label(root, text = 'XML Filename:')
name_label.grid(row = current_row, column=0)
name = Entry(root, justify = CENTER)
name.grid(row = current_row, column=1)
name.insert(0,default_filename)
current_row += 1

# Load XML Button
execute = Button(root, text = 'Load XML', command = Load_XML, activebackground = 'green')
execute.grid(row = current_row, column=0, columnspan = 2, pady = 5)
current_row += 1

# delay text_box
delay_label = Label(root, text = 'Intermessage Delay (ms):')
delay_label.grid(row = current_row, column=0)
delay = Entry(root, justify = CENTER)
delay.grid(row = current_row, column=1)
delay.insert(0, str(default_delay))
current_row += 1

# Command input text frame
Command_label = Label(root, text = 'Commands to be sent', anchor = S)
Command_label.config(font=("Courier", 16))
Command_label.grid(row = current_row, column=0, columnspan = 2, pady = 10)
current_row += 1
command_scroll = Scrollbar(root)
#command_scroll.pack(side=RIGHT, fill = Y)
Command_text = Text(root, height = 10, width = 40, yscrollcommand=command_scroll.set)
Command_text.insert(INSERT, '\n'.join(default_commands))
Command_text.grid(row = current_row, column=0, columnspan = 2, padx = 5, sticky = 'NESW')
current_row += 1

# Use Aardvark Button
execute = Button(root, text = 'Use Aardvark', command = Write_I2C, activebackground = 'red')
execute.grid(row = current_row, column=1, pady = 5)

# Write XML Button
execute = Button(root, text = 'Write XML', command = Write_XML, activebackground = 'red')
execute.grid(row = current_row, column=0, pady = 5)

# Output text frame
output_label = Label(root, text = 'Output')
output_label.config(font=("Courier", 16))
output_label.grid(row = 2, column=2, columnspan = 2, pady = 10)
output_text = Text(root, height = 20, width = 100)
output_text.grid(row = 3, column=2, columnspan = 2, rowspan = current_row-2, padx = 5, pady = 5, sticky = 'NESW')
output_text.config(state=DISABLED, wrap=WORD)

root.columnconfigure(3, weight = 2)
root.rowconfigure(current_row-1, weight = 2)

class GUI_Writer(object):
    def __init__(self, widget):
        self.output_text = widget

    def write(self, string):
        self.output_text.config(state=NORMAL)
        self.output_text.insert(INSERT, string)
        self.output_text.config(state=DISABLED)

sys.stdout = GUI_Writer(output_text)
mainloop()