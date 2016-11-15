# Aardvark batch script writer
# Pumpkin Inc.
# David Wright 2016

from Tkinter import *
from aardvark_builder import *

root = Tk()

# filename textbox
name = Entry(root)
name.pack()
name.insert(0,filename)

filename = 'aardvark_script.xml'

# Intermessage delay in miliseconds
Delay = 200

# Slave Address as text
address = '0x53'

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

mainloop()