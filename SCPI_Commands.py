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
chksum_size = 2
wflag_size = 1
time_size = 4
length_size = 1

# Dictionary of all telemetry Commands
SCPI_Data = {
    # SupMCU Version
    'SUP:TEL? 0,data':    [wflag_size + time_size + chksum_size + 48,            'ascii'],
    'SUP:TEL? 0,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 0,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 0,ascii':   [wflag_size + time_size + chksum_size + 48,            'ascii'],
    
    # SCPI Commands Parsed
    'SUP:TEL? 1,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 1,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 1,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 1,ascii':   [wflag_size + time_size + chksum_size + 8,             'ascii'],
    
    # SCPI Command Errors
    'SUP:TEL? 2,data':    [wflag_size + time_size + chksum_size + 1,             'uint'],
    'SUP:TEL? 2,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 2,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 2,ascii':   [wflag_size + time_size + chksum_size + 1,             'ascii'],    
    
    # Voltstat
    'SUP:TEL? 3,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    
    # SupMCU CPU Selftests
    'SUP:TEL? 4,data':    [wflag_size + time_size + chksum_size + 22,            'long, long, int, int, int'],
    'SUP:TEL? 4,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 4,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 4,ascii':   [wflag_size + time_size + chksum_size + 22,            'ascii'],    
    
    # Elapsed Time in Seconds
    'SUP:TEL? 5,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 5,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 5,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 5,ascii':   [wflag_size + time_size + chksum_size + 8,             'ascii'],    
    
    # Number of context switches
    'SUP:TEL? 6,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 6,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 6,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 6,ascii':   [wflag_size + time_size + chksum_size + 8,             'ascii'],       
    
    # idling Hooks remaining
    'SUP:TEL? 7,data':    [wflag_size + time_size + chksum_size + 8,             'long long'],
    'SUP:TEL? 7,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 7,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 7,ascii':   [wflag_size + time_size + chksum_size + 8,             'ascii'],      
    
    # MCU Load
    'SUP:TEL? 8,data':    [wflag_size + time_size + chksum_size + 8,             'double'],
    'SUP:TEL? 8,name':    [wflag_size + time_size + name_size + chksum_size,     'ascii'],
    'SUP:TEL? 8,length':  [wflag_size + time_size + length_size + chksum_size,   'char'],
    'SUP:TEL? 8,ascii':   [wflag_size + time_size + chksum_size + 8,             'ascii']
    
    }

# Find the number of bytes to be read by a command if it is present in the dictionary
def read_length(command):
    if SCPI_Data.has_key(command):
        return SCPI_Data[command][0]
    else:
        print '*** Command not found in dictionary, length defaults to 16, data shown in hex ***'
        return 16
    # end
# end


# print the data array in the format specified 
def print_read(command, raw_data):
    
    if SCPI_Data.has_key(command):
        print_format = SCPI_Data[command][1]
        
        write_flag = raw_data[0:wflag_size-1]
        timestamp = raw_data[wflag_size:wflag_size+time_size]
        data = raw_data[wflag_size+time_size:-chksum_size]
        checksum = raw_data[-chksum_size:]
        
        if write_flag == 0:
            print '*** Read failed, Write flag = 0 ***'
            return 0
        
        elif ',' not in print_format:
            print 'Timestamp: ' + ' '.join(['0x%02x' % x for x in timestamp]) + '\nData:'
 
            if print_format == 'ascii':
                print ''.join([chr(x) for x in data])
                
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
            
            else:
                print '*** No valid format for data ***'
            # end
        else:
            print 'Timestamp: ' + ' '.join(['0x%02x' % x for x in timestamp]) + '\nData:'
            formats = print_format.split(', ')
            start_index = 0
            output = [None]*len(formats)
            i = 0
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
                    print '*** No valid format at list entry ' + str(i) + '***' 
                # end
                i += 1
            # end
            print output
        #end
            
    # end
    print 'Hex:\n' + ' '.join(['%02x' % x for x in raw_data])
# end