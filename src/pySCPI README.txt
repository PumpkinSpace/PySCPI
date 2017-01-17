Welcome to pySCPI.

This porgram provides a PC based interface for using SCPI commands to communicate with Pumpkin modules that feature SCPI command interfaces. This program can be used to send commands to modules aswell as recieving and formatting telemetry requests.

Contents:

1. Using pySCPI
	A. Using the GUI
	B. Sending SCPI commands
	C. Logging
	D. Common Issues 
2. Supported Modules

********************
1. Using pySCPI

pySCPI provides a GUI to allow users to send SCPI commands from a computer to Pumpkin modules that have SCPI capabilities, this section covers the basics of using this program.


**********
A. Using the GUI

Load Commands:
This button allows previously saved commad lists to be imported into pySCPI to by used. This also imports other data such as the delays used.

View ReadMe:
This button displays this file in the GUI Output box.

Slave Device:
The dropdown box can be used to select from a range of supported Pumpking modules. Additionally the address can be modified directly in the text box but must maintain the format 0x__.

Intermessage Delay: 
This is the millisecond delay between I2C transactions sent from this program. This value can be changed as you see fit, short delays (<20ms) may cause bad data to be returned from telemetry requests so be wary of that.

ASCII Message Delay: 
This is the millisecond delay between sending and recieving an ASCII data request. As this data takes longer for the slave to process this delay should always be significantly longer than the Intermessage Delay; >100ms is a good place to start

Float DP: 
defines the number of decimal places to be used when displaying floats in the Output box.

Logging Period:
This the period in seconds at which commands should be sent when using the logging capability of pySCPI.

Input Commands:
This text box is where you should enter the commands that you want to be sent to the slave device. Commands should be entered one per line and can have whitespace separating them. When commands are saved or loaded the name of the file is use is shown to the right of the Input Commands title, and will stay there as long as the command list matches that file.

Save Commands:
This button will save the command list and associated delays as an xml file to be imported into the program again at a later date. These XML files are also compatible with Total Phase software provided by the Aardvark manufacturer.

Send Commands:
This button initiates I2C transmission through the Aardvark device, sending the requested commands with the given configuration. This button will remain green and disabled for the duration of the transmission.

Start Logging:
This button starts a logging loop that sends the command list at the rate defined by the logging period. This data is then saved to a csv file so that it can be imported into a data analysis program of your choice.

Stop Logging:
Once logging is underway this button can be used to stop the logging at the end of the next cycle.

Ouput:
This text box is where output from the program is written. This may take the form of data returned, system messages or errors produced. For common errors see section D.


**********
B. Sending SCPI Commands

pySCPI can be used to send any supported SCPI command to a Pumpkin Module, these commands fall into two catagories; Commands and Telemetry Requests.

Commands:
A command in this context refers to the subset of SCPI commands that are not a request for telemetry, such as Starting the MCU Self tests or turing off the MCU status LED.

To send such a command it just needs to be typed into the 'Input Commands' box. A listing of these commands can be found in the supporting documentation for each specific module. Any command can be issued from pySCPI without altering the program configuration as no checking of command validity is done within the program.

Telemetry Requests:
Telemetry requests are SCPI commands that when recieved by a module cause it to load a certain data field into it's output buffer for the host to read. pySCPI takes care of both the sending of the command and the reading of the data. The time delay between read and write commands is defined by the Intermessage Delay and ASCII delay boxes in the GUI. The data recieved by pySCPI from the slave device is then formatted and displayed in the Output box. A listing of accepted telemetry requests can be found in the supporting documentation for each specific module.


**********
C. Logging

pySCPI allows the user to log data indefinately with a period defined using the 'Logging Period' field in the GUI. Logging can be started by clicking the 'Start Logging' button and then selecting the file to log to, and can then be stopped by clinking the green 'Stop Logging' button. The GUI will update it's display with each successive telemetry reading loop. 

Logging will write the output of all telemetry requests issued in the 'Input Commands' box to a .csv file that can then be imported into the data alaysis program of your choice. 

If the period requested is shorter than the time required to collect all telemetry then the logging period will be the amount of time taken to recieve all of the telemetry.

**********
B. Common Issues

*** Requested delay is not valid, reverting to default *** = The delay entered is not a valid number.

*** Requested ascii delay is not valid, reverting to default *** = The ascii delay entered is not a valid number.

*** Invlaid address entered, reverting to device default *** = Make sure the address you entered matches the format 0x__

*** Requested logging period is not valid, reverting to default *** = The logging period entered is not a valid number.

*** Warning, logging period may be shorter than the dration of the commands requested *** = The logging period entered may be sorter than the time taken to sample all of the commands, therefore the logging period may be stretched to accommodate the data reading.

*** No file given to Load *** = The Load XML window was exited without selecting a file.

*** No Logging filename selected *** = The Start Logging window was exited without selecting a valid filename

*** No XML file written *** = The Save XML window was exited without saving.

*** No Aardvark is present *** = make sure you have an Aardvark connected to the computer you are using.

*** Requested XML file is open in another program *** = The file you are trying to save to is being used by another program, close the file or select a new filename to save to.

*** Requested log file is in use by another program *** = The file you are trying to log to is being used by another program, close the file or select a new filename to save to.

*** Aardvark is being used, disconnect other application or Aardvark device *** = You either have another program using the Aardvark or a pervious program exited without closing its connection. Ensure all other programs are closed and disconnect the Aardvark and then plug it back in again.

*** Command not found in dictionary *** = You are requesting telemetry that is not supproted by this pySCPI, a default format and length will be returned. Please check your command for accuracy and contact Pumpkin if you believe that command should be supported.

*** Read failed, Write flag = 0 *** = The Processor was not ready for your request, try increasing the Intermessage Delay and ensure that the Slave address is set correctly for the command you are sending.

Data is returned as Hex: 01 01 01 01 01 01 01.... = The Aardvark is not able to communicate with the module, unsure everything is connected and the module is powered.



********************
2. Supported Modules

pySCPI currently supports the following modules:

PIM  : Payload Interface Module
BIM  : Bus Interface Module
BM2  : Battery Module 2
GPSRM: GPS Reciever Module
BSM  : battery Switching Module

********************
pySCPI created by David Wright,
(c) Pumpkin Inc. 2017
