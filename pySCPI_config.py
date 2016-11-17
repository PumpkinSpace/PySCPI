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
    'BSM:TEL? 5,data':    [wflag_size + time_size + chksum_size + 1,             'hex'],
    'BSM:TEL? 5,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 5,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 5,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Channel over current event log
    'BSM:TEL? 6,data':    [wflag_size + time_size + chksum_size + 10,            'uint, uint, uint, uint, uint'],
    'BSM:TEL? 6,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BSM:TEL? 6,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BSM:TEL? 6,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    ############################### BM2 Commands ########################################
    
    ## Skip entries 1-6
    
    # Temperature
    'BM2:TEL? 8,data':    [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 8,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 8,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 8,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Voltage
    'BM2:TEL? 9,data':    [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 9,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 9,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 9,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Current
    'BM2:TEL? 10,data':   [wflag_size + time_size + chksum_size + 2,             'int'],
    'BM2:TEL? 10,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 10,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 10,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Average Current
    'BM2:TEL? 11,data':   [wflag_size + time_size + chksum_size + 2,             'int'],
    'BM2:TEL? 11,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 11,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 11,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    ## Skip entry 12
    
    # Relative State of Chrage
    'BM2:TEL? 13,data':   [wflag_size + time_size + chksum_size + 1,             'char'],
    'BM2:TEL? 13,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 13,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 13,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Absolute State of Chrage
    'BM2:TEL? 14,data':   [wflag_size + time_size + chksum_size + 1,             'char'],
    'BM2:TEL? 14,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 14,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 14,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Remaining Capacity
    'BM2:TEL? 15,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 15,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 15,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 15,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Full Charge Capacity
    'BM2:TEL? 16,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 16,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 16,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 16,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Run time to empty
    'BM2:TEL? 17,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 17,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 17,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 17,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Average time to empty
    'BM2:TEL? 18,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 18,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 18,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 18,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Average time to full
    'BM2:TEL? 19,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 19,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 19,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 19,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Charging Current
    'BM2:TEL? 20,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 20,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 20,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 20,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Charging Voltage
    'BM2:TEL? 21,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 21,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 21,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 21,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Battery Status register
    'BM2:TEL? 22,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 22,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 22,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 22,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Cycle count
    'BM2:TEL? 23,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 23,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 23,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 23,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Design Capacity
    'BM2:TEL? 24,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 24,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 24,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 24,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # Design voltage
    'BM2:TEL? 25,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 25,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 25,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 25,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    ## Skip entries 26-47
    
    # Extra Temperature sensor 1
    'BM2:TEL? 48,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 48,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 48,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 48,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Extra Temperature sensor 2
    'BM2:TEL? 49,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 49,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 49,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 49,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Extra Temperature sensor 3
    'BM2:TEL? 50,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 50,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 50,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 50,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Extra Temperature sensor 4
    'BM2:TEL? 51,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 51,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 51,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 51,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # BM2 Status
    'BM2:TEL? 52,data':   [wflag_size + time_size + chksum_size + 1,             'hex'],
    'BM2:TEL? 52,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 52,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 52,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Perminant failure time
    'BM2:TEL? 53,data':   [wflag_size + time_size + chksum_size + 15,            'ascii'],
    'BM2:TEL? 53,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 53,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 53,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Perminant failure registers
    'BM2:TEL? 54,data':   [wflag_size + time_size + chksum_size + 4,             'hex'],
    'BM2:TEL? 54,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 54,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 54,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # SBS Data Read return value
    'BM2:TEL? 55,data':   [wflag_size + time_size + chksum_size + 32,            'hex'],
    'BM2:TEL? 55,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 55,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 55,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Flash Data Read return value
    'BM2:TEL? 56,data':   [wflag_size + time_size + chksum_size + 32,            'hex'],
    'BM2:TEL? 56,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 56,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 56,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Manuracturer Access Data Read return value
    'BM2:TEL? 57,data':   [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 57,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 57,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 57,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Function call return value
    'BM2:TEL? 58,data':   [wflag_size + time_size + chksum_size + 8,             'hex'],
    'BM2:TEL? 58,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 58,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 58,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    ## Skip entry 59
    
    # Cell Voltage 4
    'BM2:TEL? 60,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 60,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 60,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 60,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Cell Voltage 3
    'BM2:TEL? 61,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 61,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 61,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 61,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    # Cell Voltage 2
    'BM2:TEL? 62,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 62,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 62,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 62,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    # Cell Voltage 1
    'BM2:TEL? 63,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 63,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 63,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 63,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    ## Skip entries 64-79
    
    # Safety Alert Register
    'BM2:TEL? 80,data':   [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 80,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 80,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 80,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Safety Status Register
    'BM2:TEL? 81,data':   [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 81,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 81,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 81,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Perminant failure alert Register
    'BM2:TEL? 82,data':   [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 82,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 82,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 82,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Perminant failure status Register
    'BM2:TEL? 83,data':   [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 83,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 83,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 83,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Operation status Register
    'BM2:TEL? 84,data':   [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 84,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 84,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 84,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Charging status Register
    'BM2:TEL? 85,data':   [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 85,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 85,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 85,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    ## Skip entries 86-89
    
    # Pack Voltage
    'BM2:TEL? 90,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 90,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 90,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 90,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],   
    
    ## Skip entries 91-92
        
    # Average Voltage
    'BM2:TEL? 93,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 93,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 93,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 93,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # TS1 temperature
    'BM2:TEL? 94,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 94,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 94,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 94,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # TS2 temperature
    'BM2:TEL? 95,data':   [wflag_size + time_size + chksum_size + 2,             'uint'],
    'BM2:TEL? 95,name':   [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 95,length': [wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 95,ascii':  [wflag_size + time_size + chksum_size + 128,           'ascii'],
    
    ## Skip entries 96-103
        
    # Safety Alert 2 Register
    'BM2:TEL? 104,data':  [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 104,name':  [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 104,length':[wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 104,ascii': [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Safety Status 2 Register
    'BM2:TEL? 105,data':  [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 105,name':  [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 105,length':[wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 105,ascii': [wflag_size + time_size + chksum_size + 128,           'ascii'], 
    
    # Perminant failure alert 2 Register
    'BM2:TEL? 106,data':  [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 106,name':  [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 106,length':[wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 106,ascii': [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    # Perminant failure status 2 Register
    'BM2:TEL? 107,data':  [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 107,name':  [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 107,length':[wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 107,ascii': [wflag_size + time_size + chksum_size + 128,           'ascii'],  
    
    ## Skip entries 108-113
            
    # Temperature Range
    'BM2:TEL? 114,data':  [wflag_size + time_size + chksum_size + 2,             'hex'],
    'BM2:TEL? 114,name':  [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'BM2:TEL? 114,length':[wflag_size + time_size + length_size + chksum_size,   'char'],
    'BM2:TEL? 114,ascii': [wflag_size + time_size + chksum_size + 128,           'ascii'],    
}   
