# Functions that format the SCPI Command output

from struct import unpack
import sys
from pySCPI_config import *
import csv

# Find the number of bytes to be read by a command if it is present in the dictionary
def read_length(command):
    if SCPI_Data.has_key(command):
        # extract the length from the dictionary
        return SCPI_Data[command][0]
    else:
        # command isn't in library so use the default length
        print '*** Command \"' + command + '\" not found in dictionary, length defaults to ' + str(default_length) + ' ***'
        return default_length
    # end
# end

# convert the timestamp number into a string
def get_time(timestamp):
    ticks = unpack('<L', ''.join([chr(x) for x in timestamp]))[0]
    sec = ticks/100
    dd = sec/(60*60*24)
    hh = sec/(60*60) - dd*24
    mm = sec/60 - hh*60 - dd*60*24
    ss = sec - mm*60 - hh*60*60 - dd*60*60*24
    tt = ticks - ss*100 - mm*60*100 - hh*60*60*100 - dd*60*60*24*100
    return '%02d:' % dd + '%02d:' % hh + '%02d:' % mm + '%02d.' % ss + '%02d' % tt
# end

# convert the timestamp number into a string
def log_time(timestamp):
    ticks = unpack('<L', ''.join([chr(x) for x in timestamp]))[0]
    return ticks/100.0
# end

# print the data array in the format specified 
def print_read(command, raw_data, double_dp):
    
    # index to stop printing at
    stop_index = len(raw_data)    
    
    # is the command in the dictionary
    if SCPI_Data.has_key(command):
        # extract the format of the command from the dictionary
        print_format = SCPI_Data[command][1]
              
        # split the incoming command into its respective parts
        write_flag = raw_data[0:wflag_size]
        timestamp = raw_data[wflag_size:wflag_size+time_size]       
        
        if chksum_size != 0:
            checksum = raw_data[-chksum_size:]
            data = raw_data[wflag_size+time_size:-chksum_size]
        else:
            data = raw_data[wflag_size+time_size:]
        # end
        
        if not has_preamble(command):
            data = raw_data[0:-(wflag_size + time_size + chksum_size)]
        # end
        
        if (write_flag[0] != 1) and has_preamble(command):
            # The command was sent too fast, bad data was recieved
            print '*** Read failed, Write flag = 0 ***'
            
        # else the data is good or is in ascii formatting
        elif ',' not in print_format:
            # the data is just a single peice of data, not a list.
            
            if has_preamble(command):
                # print the timestamp
                print 'Timestamp:\t\t' + get_time(timestamp)
            # end
 
            # print the data in the appropriate format given by the dictionary
            if print_format == 'ascii':
                if 0 in data:
                    print 'Data:\t\t' + ''.join([chr(x) for x in data[0:data.index(0)]])
                    if not has_preamble(command):
                        stop_index = data.index(0)
                    else:
                        stop_index = data.index(0) + 5
                    # end
                else:
                    print 'Data:\t\t' + ''.join([chr(x) for x in data])
                # end
                
            elif print_format == 'int':
                print 'Data:\t\t' + str(unpack('<h', ''.join([chr(x) for x in data]))[0])
                
            elif print_format == 'long':
                print 'Data:\t\t' + str(unpack('<l', ''.join([chr(x) for x in data]))[0])
                
            elif print_format == 'long long':
                print 'Data:\t\t' + str(unpack('<q', ''.join([chr(x) for x in data]))[0])        
                
            elif print_format == 'uint':
                print 'Data:\t\t' + str(unpack('<H', ''.join([chr(x) for x in data]))[0]) 
                
            elif print_format == 'double':
                print 'Data:\t\t' + '{:.{dp}f}'.format(unpack('<d', ''.join([chr(x) for x in data]))[0], dp=double_dp) 
                
            elif print_format == 'char':
                print 'Data:\t\t' + str(unpack('<B', ''.join([chr(x) for x in data]))[0]) 
            
            elif print_format == 'hex':
                print 'Data:\t\t' + ' '.join(['0x%02x' % x for x in data])
            
            else:
                # the format in the dictionary does not match one of the supported types
                print '*** No valid format for data ***'
            # end
            
            # print checksum if present
            if (chksum_size != 0) and has_preamble(command):
                print 'Checksum:\t\t' + ' '.join(['0x%02X' % x for x in checksum])
            # end
            
        else:
            # the data received is a list so process each piece individually
            # does not accept hex or ascii parts in the list
            
            # print the timestamp
            print 'Timestamp:\t\t' + get_time(timestamp)
            
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
                    output[i] =  unpack('<B', ''.join([chr(x) for x in data[start_index:start_index+1]]))[0]
                    start_index += 1
                else:
                    # the format is not accepted by this code
                    print '*** No valid format at list entry ' + str(i) + '***' 
                    
                # end and iterate
                i += 1
            # end
            
            # construct an output string
            output_string = 'Data:\t\t['
            array_len = len(output)
            for i in range(array_len):
                if type(output[i]) is float:
                    # if the object is a float, format accordingly
                    output_string = output_string  + '{:.{dp}f}'.format(output[i], dp = double_dp)
                else:
                    output_string = output_string  + str(output[i])
                    
                if i < array_len - 1:
                    output_string = output_string + ', '
            print output_string + ']'
            
            # print checksum if present
            if chksum_size != 0:
                print 'Checksum: ' + ' '.join(['0x%02X' % x for x in checksum])
            # end            
        #end
    # end
    
    # print the Hex data at the end, also print in hex by default
    print 'Hex:\t\t' + ' '.join(['%02X' % x for x in raw_data[0:stop_index]])
# end

# print the data array in the format specified 
def log_read(command, raw_data, csv_row):
    
    # is the command in the dictionary
    if SCPI_Data.has_key(command):
        # extract the format of the command from the dictionary
        print_format = SCPI_Data[command][1]
              
        # split the incoming command into its respective parts
        write_flag = raw_data[0:wflag_size]
        timestamp = raw_data[wflag_size:wflag_size+time_size]       
        
        if chksum_size != 0:
            checksum = raw_data[-chksum_size:]
            data = raw_data[wflag_size+time_size:-chksum_size]
        else:
            data = raw_data[wflag_size+time_size:]
        # end
        
        if not has_preamble(command):
            data = raw_data[0:-(wflag_size + time_size + chksum_size)]
        # end
        
        if (write_flag[0] != 1) and has_preamble(command):
            # The command was sent too fast, bad data was recieved
            csv_row.append('WF = 0')
            for format in print_format.split(','):
                csv_row.append('WF = 0')
            # end
            
        # else the data is good or is in ascii formatting
        elif ',' not in print_format:
            # the data is just a single peice of data, not a list.
            
            if has_preamble(command):
                # print the timestamp
                csv_row.append(log_time(timestamp))
            # end
 
            # print the data in the appropriate format given by the dictionary
            if print_format == 'ascii':
                if 0 in data:
                    csv_row.append(''.join([chr(x) for x in data[0:data.index(0)]]))
                    # end
                else:
                    csv_row.append(''.join([chr(x) for x in data]))
                # end
                
            elif print_format == 'int':
                csv_row.append(unpack('<h', ''.join([chr(x) for x in data]))[0])
                
            elif print_format == 'long':
                csv_row.append(unpack('<l', ''.join([chr(x) for x in data]))[0])
                
            elif print_format == 'long long':
                csv_row.append(unpack('<q', ''.join([chr(x) for x in data]))[0])        
                
            elif print_format == 'uint':
                csv_row.append(unpack('<H', ''.join([chr(x) for x in data]))[0])
                
            elif print_format == 'double':
                csv_row.append(unpack('<d', ''.join([chr(x) for x in data]))[0])
                
            elif print_format == 'char':
                csv_row.append(unpack('<B', ''.join([chr(x) for x in data]))[0]) 
            
            elif print_format == 'hex':
                csv_row.append(' '.join(['0x%02x' % x for x in data]))
            
            else:
                # the format in the dictionary does not match one of the supported types
                csv_row.append('invalid format')
            # end
             
        else:
            # the data received is a list so process each piece individually
            # does not accept hex or ascii parts in the list
            
            # print the timestamp
            csv_row.append(log_time(timestamp))
            
            # split the list into individual formats
            formats = print_format.split(', ')
            start_index = 0
            i = 0
            # for each item in the list print it according to the associated specification
            for spec in formats:
                if spec == 'int':
                    csv_row.append(unpack('<h', ''.join([chr(x) for x in data[start_index:start_index+2]]))[0])
                    start_index += 2
                    
                elif spec == 'long':
                    csv_row.append(unpack('<l', ''.join([chr(x) for x in data[start_index:start_index+4]]))[0])
                    start_index += 4
                    
                elif spec == 'long long':
                    csv_row.append(unpack('<q', ''.join([chr(x) for x in data[start_index:start_index+8]]))[0])
                    start_index += 8
                    
                elif spec == 'uint':
                    csv_row.append(unpack('<H', ''.join([chr(x) for x in data[start_index:start_index+2]]))[0])  
                    start_index += 2
                    
                elif spec == 'double':
                    csv_row.append(unpack('<d', ''.join([chr(x) for x in data[start_index:start_index+8]]))[0])
                    start_index += 8
                    
                elif spec == 'char':
                    csv_row.append(unpack('<B', ''.join([chr(x) for x in data[start_index:start_index+1]]))[0])
                    start_index += 1
                else:
                    # the format is not accepted by this code
                    csv_row.append('invalid format') 
                    
                # end and iterate
                i += 1
            # end    
        #end
    # end
# end

# Get a list of devices supported by the dictionary
def get_devices():
    devices = []
    keys = SCPI_Data.keys()
    dev_keys = [key.split(':')[0] for key in keys]
    for key in dev_keys:
        if (key not in devices) and (key != 'SUP'):
            devices = devices + [key]
        # end
    # end
    devices = ['GPSRM' if device == 'GPS' else device for device in devices]
    return devices
#end
        