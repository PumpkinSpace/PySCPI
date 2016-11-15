# Dictionary of SCPI Commands for Pumpkin Projects
#
# Each entry is a follows
#
# 'Command': [int length, 'format'],
#
# where format can be one of:
#     ascii
#     hex
#     int
#     uint
#     double
#     long
#     long long
#     char
#     list of any combination of the above without brackets and separated by ', '

from struct import unpack

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
    'SUP:TEL? 2,data':    [wflag_size + time_size + chksum_size + 1,             'uint'],
    'SUP:TEL? 2,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 2,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 2,ascii':   [wflag_size + time_size + chksum_size + 128,           'ascii'],    
    
    # Voltstat
    'SUP:TEL? 3,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    
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



# Find the number of bytes to be read by a command if it is present in the dictionary
def read_length(command):
    if SCPI_Data.has_key(command):
        # extract the length from the dictionary
        return SCPI_Data[command][0]
    else:
        # command isn't in library so use the default length
        print '*** Command not found in dictionary, length defaults to 16, data shown in hex ***'
        return 16
    # end
# end


# print the data array in the format specified 
def print_read(command, raw_data):
    
    # is the command in the dictionary
    if SCPI_Data.has_key(command):
        # extract the format of the command from the dictionary
        print_format = SCPI_Data[command][1]
        
        # split the incoming command into its respective parts
        write_flag = raw_data[0:wflag_size]
        timestamp = raw_data[wflag_size:wflag_size+time_size]
        
        # index to stop printing at
        stop_index = len(raw_data)
        
        
        if chksum_size != 0:
            checksum = raw_data[-chksum_size:]
            data = raw_data[wflag_size+time_size:-chksum_size]
        else:
            data = raw_data[wflag_size+time_size:]
        # end
        
        if write_flag[0] == 0:
            # The command was sent too fast, bad data was recieved
            print '*** Read failed, Write flag = 0 ***'
            
        # else the data is good
        elif ',' not in print_format:
            # the data is just a single peice of data, not a list.
            
            # print the timestamp
            print 'Timestamp: ' + ' '.join(['0x%02x' % x for x in timestamp]) + '\nData:'
 
            # print the data in the appropriate format given by the dictionary
            if print_format == 'ascii':
                print ''.join([chr(x) for x in data[0:data.index(0)]])
                stop_index = data.index(0) + 5
                
            elif print_format == 'int':
                print unpack('<h', ''.join([chr(x) for x in data]))[0]
                
            elif print_format == 'long':
                print unpack('<l', ''.join([chr(x) for x in data]))[0]
                
            elif print_format == 'long long':
                print unpack('<q', ''.join([chr(x) for x in data]))[0]        
                
            elif print_format == 'uint':
                print unpack('<H', ''.join([chr(x) for x in data]))[0]  
                
            elif print_format == 'double':
                print unpack('<d', ''.join([chr(x) for x in data]))[0]
                
            elif print_format == 'char':
                print unpack('<B', ''.join([chr(x) for x in data]))[0] 
            
            elif print_format == 'hex':
                print ' '.join(['0x%02x' % x for x in data])
            
            else:
                # the format in the dictionary does not match one of the supported types
                print '*** No valid format for data ***'
            # end
            
            # print checksum if present
            if chksum_size != 0:
                print 'Checksum: ' + ' '.join(['0x%02x' % x for x in checksum])
            # end
            
        else:
            # the data received is a list so process each piece individually
            # does not accept hex or ascii parts in the list
            
            # print the timestamp
            print 'Timestamp: ' + ' '.join(['0x%02x' % x for x in timestamp]) + '\nData:'
            
            # split the list into individual formats
            formats = print_format.split(', ')
            start_index = 0
            output = [None]*len(formats)
            i = 0
            # for each item in the list print it according to the associated specification
            for spec in formats:
                if spec == 'int':
                    output[i] =  unpack('<h', ''.join([chr(x) for x in data[start_index:start_index+2]]))[0]
                    start_index += 2
                    
                elif spec == 'long':
                    output[i] =  unpack('<l', ''.join([chr(x) for x in data[start_index:start_index+4]]))[0]
                    start_index += 4
                    
                elif spec == 'long long':
                    output[i] =  unpack('<q', ''.join([chr(x) for x in data[start_index:start_index+8]]))[0]
                    start_index += 8
                    
                elif spec == 'uint':
                    output[i] =  unpack('<H', ''.join([chr(x) for x in data[start_index:start_index+2]]))[0]  
                    start_index += 2
                    
                elif spec == 'double':
                    output[i] =  unpack('<d', ''.join([chr(x) for x in data[start_index:start_index+8]]))[0]
                    start_index += 8
                    
                elif spec == 'char':
                    output[i] =  unpack('<B', ''.join([chr(x) for x in data[start_index]]))[0]
                    start_index += 1
                else:
                    # the format is not accepted by this code
                    print '*** No valid format at list entry ' + str(i) + '***' 
                    
                # end and iterate
                i += 1
            # end
            print output
            
            # print checksum if present
            if chksum_size != 0:
                print 'Checksum: ' + ' '.join(['0x%02x' % x for x in checksum])
            # end            
        #end
    else:
        print '*** This command is not in the library ***\nHex:'
    # end
    
    # print the Hex data at the end, also print in hex by default
    print 'Hex:\n' + ' '.join(['%02x' % x for x in raw_data[0:stop_index]])
# end