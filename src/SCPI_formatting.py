"""
@package SCPI_formatting.py
Module to handle the formatting of data in the pySCPI program.

Author: David Wright

(c) Pumpkin Inc. 2017
"""

from struct import unpack
import sys
from pySCPI_config import *
import csv


"""
Reads the length of a command from the dictionary.

@param[in]  command:  The command to find the length of (string).
@return     (Int)     The length of that command, or the default 
                      length if the command is not found.
"""
def read_length(command):
    if SCPI_Data.has_key(command):
        # extract the length from the dictionary
        return SCPI_Data[command][0]
    else:
        # command isn't in library so use the default length
        print '*** Command \"' + command + '\" not found in dictionary, length defaults to ' + str(default_length) + ' ***'
        return default_length
    # end if
# end def


"""
Converts the raw timestamp data into a string for printing to the GUI.

@param[in]  timestamp:  The raw hex timestamp to be converted (list of ints).
@return     (string)    The formatted string denoting the time in the format:
                        days:hours:mins:seconds.1/100th seconds.
"""
def get_time(timestamp):
    # turn the hex data into a long int
    ticks = unpack('<L', ''.join([chr(x) for x in timestamp]))[0]
    # break it down into parts
    sec = ticks/100
    dd = sec/(60*60*24)
    hh = sec/(60*60) - dd*24
    mm = sec/60 - hh*60 - dd*60*24
    ss = sec - mm*60 - hh*60*60 - dd*60*60*24
    tt = ticks - ss*100 - mm*60*100 - hh*60*60*100 - dd*60*60*24*100
    # construct the string
    return '%02d:' % dd + '%02d:' % hh + '%02d:' % mm + '%02d.' % ss + '%02d' % tt
# end def


"""
Converts the ascii timestamp data into a string for printing to the GUI.

@param[in]  data:       The data list to be converted (list of ints).
@return     (string)    The formatted string denoting the time in the format:
                        days:hours:mins:seconds.1/100th seconds.
"""
def get_ascii_time(data):
    # turn the hex data into a long int
    string_data = ''.join([chr(x) for x in data])
    ticks = int(string_data[3:string_data.find(']')])
    # break it down into parts
    sec = ticks/100
    dd = sec/(60*60*24)
    hh = sec/(60*60) - dd*24
    mm = sec/60 - hh*60 - dd*60*24
    ss = sec - mm*60 - hh*60*60 - dd*60*60*24
    tt = ticks - ss*100 - mm*60*100 - hh*60*60*100 - dd*60*60*24*100
    # construct the string
    return '%02d:' % dd + '%02d:' % hh + '%02d:' % mm + '%02d.' % ss + '%02d' % tt
# end def


"""
Converts the raw timestamp data into a float for logging.

@param[in]  timestamp:  The raw hex timestamp to be converted (list of ints).
@return     (float)     Time in seconds.
"""
def log_time(timestamp):
    ticks = unpack('<L', ''.join([chr(x) for x in timestamp]))[0]
    return ticks/100.0
# end def

"""
Formats the data that was returned from the AArdvark and then prints it to 
the GUI according to the specifications of the dictionary.

@param[in]  command:   The command that was sent (string).
@param[in]  raw_data:  The raw data provided by the Aardvark (list of ints).
@param[in]  double_dp: The number of decimal places to print for a double (int).
@return     None.
"""
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
        
        # if a checksum is included extract that
        if chksum_size != 0:
            checksum = raw_data[-chksum_size:]
            data = raw_data[wflag_size+time_size:-chksum_size]
        else:
            data = raw_data[wflag_size+time_size:]
        # end if
        
        # if there is no preamble clip the extra bytes off the end
        if not has_preamble(command):
            data = raw_data[0:-(wflag_size + time_size + chksum_size)]
        # end if
        
        if (write_flag[0] != 1) and has_preamble(command):
            # The command was sent too fast, bad data was recieved
            print '*** Read failed, Write flag = 0, try increasing the messgage delay***'
            
        elif all(byte == 1 for byte in raw_data):
            # The device is not connected
            print '*** Read failed, ensure the slave device is connected and powered ***'            
    
        # else the data is good or is in ascii formatting
        elif ',' not in print_format:
            # the data is just a single peice of data, not a list.
            
            if has_preamble(command):
                # print the timestamp
                print 'Timestamp:\t\t' + get_time(timestamp)
            # end if
            elif print_format == 'ascii':
                print 'Timestamp:\t\t' + get_ascii_time(data)
                
 
            # print the data in the appropriate format given by the dictionary
            if print_format == 'ascii':
                if 0 in data:
                    # terminate printing at the null terminator of the string
                    print 'Data:\t\t' + ''.join([chr(x) for x in data[0:data.index(0)]])
                    # store the position of the null terminator depending on whether there is a preamble
                    if not has_preamble(command):
                        stop_index = data.index(0)
                    else:
                        stop_index = data.index(0) + wflag_size + time_size
                    # end if
                else:
                    # no null terminator
                    print 'Data:\t\t' + ''.join([chr(x) for x in data])
                # end if
                
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
            # end if
            
            # print checksum if present
            if (chksum_size != 0) and has_preamble(command):
                print 'Checksum:\t\t' + ' '.join(['0x%02X' % x for x in checksum])
            # end if
            
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
            # for each item in the list print it according to the associated specification and then shift the pointer
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
                    
                # end if and iterate
                i += 1
            # end for
            
            # construct an output string
            output_string = 'Data:\t\t['
            array_len = len(output) # number of data items
            for i in range(array_len):
                if type(output[i]) is float:
                    # if the object is a float, format accordingly
                    output_string = output_string  + '{:.{dp}f}'.format(output[i], dp = double_dp)
                else:
                    output_string = output_string  + str(output[i])
                    
                if i < array_len - 1:
                    # add a comma between items
                    output_string = output_string + ', '
                # end if
            # end for
            
            # print the formatted data
            print output_string + ']'
            
            # print checksum if present
            if chksum_size != 0:
                print 'Checksum: ' + ' '.join(['0x%02X' % x for x in checksum])
            # end if        
        #end if
    # end if
    
    # print the Hex data at the end, also print in hex by default
    print 'Hex:\t\t' + ' '.join(['%02X' % x for x in raw_data[0:stop_index]])
# end def


"""
Formats the data that was returned from the AArdvark and then adds it to a 
list of data to log.

@param[in]  command:   The command that was sent (string).
@param[in]  raw_data:  The raw data provided by the Aardvark (list of ints).
@param[out] csv_row:   The list of data to add to (list).
@return     None.
"""
def log_read(command, raw_data, csv_row):
    
    if command.startswith('<READ'):
        csv_row.append(' '.join(['0x%02x' % x for x in raw_data]))

    # is the command in the dictionary
    elif SCPI_Data.has_key(command):
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
        # end if
        
        if not has_preamble(command):
            data = raw_data[0:-(wflag_size + time_size + chksum_size)]
        # end if
        
        if (write_flag[0] != 1) and has_preamble(command):
            # The command was sent too fast, bad data was recieved
            csv_row.append('WF = 0')
            for format in print_format.split(','):
                csv_row.append('WF = 0')
            # end for
            
        elif all(byte == 1 for byte in raw_data):
            # The device is not connected
            csv_row.append('No Device')
            for format in print_format.split(','):
                csv_row.append('No Device')
            # end for
            
        # else the data is good or is in ascii formatting
        elif ',' not in print_format:
            # the data is just a single peice of data, not a list.
            
            if has_preamble(command):
                # print the timestamp
                csv_row.append(log_time(timestamp))
            # end if
 
            # print the data in the appropriate format given by the dictionary
            if print_format == 'ascii':
                if 0 in data:
                    csv_row.append(''.join([chr(x) for x in data[0:data.index(0)]]))
                else:
                    csv_row.append(''.join([chr(x) for x in data]))
                # end if
                
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
            # end if
             
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
                    
                # end if and iterate
                i += 1
            # end for 
        # end if
    # end if
# end def