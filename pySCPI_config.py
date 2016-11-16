# Configurable inputs to the PySCPI program

# defauult filename used in the GUI
default_filename = 'aardvark_script.xml'

# default intermessage delay used in the GUI
default_delay = 200

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


# commands loaded into the GUI on startup
default_commands = ['SUP:TEL? 0,name',
                    'SUP:TEL? 0,length',
                    'SUP:TEL? 0,data',
                    'SUP:TEL? 0,ascii',
                    ]


# constants that define the structure of telemetry data
name_size = 32
chksum_size = 0
wflag_size = 1
time_size = 4
length_size = 1


# Dictionary of all telemetry Commands
SCPI_Data = {
    # perscribed format:
    #'SCPI:COMMAND':      [length of data to be read,                            'format of the data'],
    ############################### SupMCU Commands #####################################
    # SupMCU Version
    'SUP:TEL? 0,data':    [wflag_size + time_size + chksum_size + 48,            'ascii'],
    'SUP:TEL? 0,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 0,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 0,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # SCPI Commands Parsed
    'SUP:TEL? 1,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 1,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 1,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 1,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # SCPI Command Errors
    'SUP:TEL? 2,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 2,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 2,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 2,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Voltstat
    'SUP:TEL? 3,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 3,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 3,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],     
    
    # SupMCU CPU Selftests
    'SUP:TEL? 4,data':    [wflag_size + time_size + chksum_size + 22,            'long, long, int, int, int'],
    'SUP:TEL? 4,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 4,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 4,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Elapsed Time in Seconds
    'SUP:TEL? 5,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 5,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 5,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 5,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Number of context switches
    'SUP:TEL? 6,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 6,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 6,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 6,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],       
    
    # idling Hooks remaining
    'SUP:TEL? 7,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 7,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 7,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 7,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],      
    
    # MCU Load
    'SUP:TEL? 8,data':    [wflag_size + time_size + chksum_size + 8,             'double'],
    'SUP:TEL? 8,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 8,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 8,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    ############################### PIM Commands ########################################
    # Channel Currents
    'PIM:TEL? 0,data':    [wflag_size + time_size + chksum_size + 8,             'uint, uint, uint, uint'],
    'PIM:TEL? 0,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'PIM:TEL? 0,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'PIM:TEL? 0,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # Shunt Resistor Values
    'PIM:TEL? 1,data':    [wflag_size + time_size + chksum_size + 8,             'uint, uint, uint, uint'],
    'PIM:TEL? 1,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'PIM:TEL? 1,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'PIM:TEL? 1,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # Channel Current Limits
    'PIM:TEL? 2,data':    [wflag_size + time_size + chksum_size + 8,             'uint, uint, uint, uint'],
    'PIM:TEL? 2,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'PIM:TEL? 2,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'PIM:TEL? 2,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Channel Current offsets for linear fit
    'PIM:TEL? 3,data':    [wflag_size + time_size + chksum_size + 32,            'double, double, double, double'],
    'PIM:TEL? 3,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'PIM:TEL? 3,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'PIM:TEL? 3,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Channel Curretn scaling factors for linear fit
    'PIM:TEL? 4,data':    [wflag_size + time_size + chksum_size + 32,            'double, double, double, double'],
    'PIM:TEL? 4,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'PIM:TEL? 4,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'PIM:TEL? 4,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Status Register
    'PIM:TEL? 5,data':    [wflag_size + time_size + chksum_size + 1,             'hex'],
    'PIM:TEL? 5,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'PIM:TEL? 5,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'PIM:TEL? 5,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # Channel over current event log
    'PIM:TEL? 6,data':    [wflag_size + time_size + chksum_size + 8,             'uint, uint, uint, uint'],
    'PIM:TEL? 6,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'PIM:TEL? 6,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'PIM:TEL? 6,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    ############################### BSM Commands ########################################
    # Channel Currents
    'BSM:TEL? 0,data':    [wflag_size + time_size + chksum_size + 10,            'uint, uint, uint, uint, uint'],
    'BSM:TEL? 0,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 0,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 0,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Channel Shunt resistor values
    'BSM:TEL? 1,data':    [wflag_size + time_size + chksum_size + 10,            'uint, uint, uint, uint, uint'],
    'BSM:TEL? 1,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 1,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 1,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],     
    
    # Channel Current limits
    'BSM:TEL? 2,data':    [wflag_size + time_size + chksum_size + 10,            'uint, uint, uint, uint, uint'],
    'BSM:TEL? 2,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 2,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 2,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Channel Current offsets for linear fit
    'BSM:TEL? 3,data':    [wflag_size + time_size + chksum_size + 40,            'double, double, double, double, double'],
    'BSM:TEL? 3,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 3,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 3,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # Channel Current scaling factors for linear fit
    'BSM:TEL? 4,data':    [wflag_size + time_size + chksum_size + 40,            'double, double, double, double, double'],
    'BSM:TEL? 4,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 4,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 4,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # Status register
    'BSM:TEL? 5,data':    [wflag_size + time_size + chksum_size + 1,             'char'],
    'BSM:TEL? 5,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 5,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 5,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Channel over current event log
    'BSM:TEL? 6,data':    [wflag_size + time_size + chksum_size + 10,            'uint, uint, uint, uint, uint'],
    'BSM:TEL? 6,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 6,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 6,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],     
    }
