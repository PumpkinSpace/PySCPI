Welcome to pySCPI.

This porgram provides a PC based interface for using SCPI commands to communicate with Pumpkin modules that feature SCPI command interfaces. This program can be used to send commands to modules aswell as recieving and formatting telemetry requests.

Contents:

1. Using pySCPI
	A. Using the GUI
	B. Sending SCPI commands
	C. Using XML files
	D. Common Issues 
2. Supported Modules

********************
1. Using pySCPI
pySCPI provides a GUI to allow users to send SCPI commands from a computer to Pumpkin modules that have SCPI capabilities, this section covers the basics of using this program.


**********
A. Using the GUI
The GUI is roughly laid out in two secions, inputs on the left and output on the right

Inputs:
'Load XML' Button: Loads commands from a .xml file that was previously saved by this program. see sction C for more details.

'View ReadMe' Button: Displays this file in the GUI Output window

Slave Selection: The dropdown menu allows Pumpkin module to be selected. This then updates the I2C address to the right with the default I2C address for that module. Additionally non-default Module addresses can be entered directly into the text box to the left with the format '0x__'. For more information on supported devices see section 2.

Intermessage Delay: This is the millisecond delay between I2C transactions sent from this program. This value can be changed as you see fit, short delays (<20ms) may cause bad data to be returned from telemetry requests so be wary of that.

ASCII Delay: This is the millisecond delay between sending and recieving an ASCII data request. As this data takes longer for the slave to process this delay should always be significantly londer than the Intermessage Delay >100ms is a good place to start

File Loaded: This box dinsplays the name of the .xml file loaded provided that it has not been modified since loading it.

Commands to be sent box: This text box is where you should enter the commands that you want to be sent to the slave device. Enter commands one per line.

'Write XML' Button: Write the current configuration and SCPI commands to a .xml file. See section C for more details.

'Use Aardvark' Button: This button initiates I2C transmission through the Aardvark device, sending the requested commands with the given configuration. This button will remain red and disabled for the duration of the transmission.

Ouput:

This text box is where output from the program is written. This may take the form of data returned, system messages or errors produced. For common errors see section D.

Float DP: defines the number of decimal places to be used when displaying floats


**********
B. Sending SCPI Commands
pySCPI can be used to send any supported SCPI command to a Pumpkin Module, these commands fall into two catagories; Commands and Telemetry Requests.

Commands:
A command in this context refers to the subset of SCPI commands that are not a request for telemetry, such as Starting the MCU Self tests or turing off the MCU status LED.

To send such a command it just needs to be typed into the 'Commands to be Written' box. A listing of these commands can be found in the supporting documentation for each specific module. Any command can be issued from pySCPI without altering the program configuration as no checking of command validity is done within the program.

Telemetry Requests:
Telemetry requests are SCPI commands that when recieved by a module cause it to load a certain data field into it's output buffer for the host to read. pySCPI takes care of both the sending of the command and the reading of the data. The time delay between read and write commands is defined by the Intermessage Delay and ASCII delay boxes in the GUI. The data recieved by pySCPI from the slave device is then formatted and displayed in the Output box. A listing of accepted telemetry requests can be found in the supporting documentation for each specific module.


**********
C. Using XML files
pySCPI uses XML files to store command sets for use again later.
pySCPI comes with an XML file for each module containing examples of usable commands.

Load XML: Loads a previuosly saved XML file, this loads the command list, slave name and address and the delays used in that file.

Write XML: Saves the setting currently being used to an XML file. 


**********
B. Common Issues

*** Requested delay is not valid, reverting to default *** = The delay entered is not a valid number.

*** Invlaid address entered, reverting to device default *** = Make sure the address you entered matches the format 0x__

*** No file given to Load *** = The Load XML window was exited without selecting a file.

*** No XML file written *** = The Save XML window was exited without saving.

*** No Aardvark is present *** = make sure you have an Aardvark connected to the computer you are using.

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
