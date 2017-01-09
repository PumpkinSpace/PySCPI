Welcome to Pumpkin SCPI.

This porgram provides a PC based interface for using SCPI commands to communicate with Pumpkin modules that feature SCPI command interfaces. This program can be used to send commands to modules aswell as recieving and formatting telemetry requests.

Contents:

1. Using Pumpkin SCPI
	A. Using the GUI
	B. Sending SCPI commands
	C. Using XML files
	D. Common Issues 
2. Supported Modules
3. Adding Functionality

********************
1. Using Pumpkin SCPI
Pumpkin SCPI build on the PySCPI python program to provide a GUI to allow users to send SCPI commands to Pumpkin modules that have SCPI capabilities, this section covers the basics of using this program.


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
Pumpkin SCPI can be used to send any supported SCPI command to a Pumpkin Module, these commands fall into two catagories; Commands and Telemetry Requests.

Commands:
A command in this context refers to the subset of SCPI commands that are not a request for telemetry, such as Starting the MCU Self tests or turing off the MCU status LED.

To send such a command it just needs to be typed into the 'Commands to be Written' box. A listing of these commands can be found in the supporting documentation for each specific module. Any command can be issued from Pumpkin SCPI without altering the program configuration as no checking of command validity is done within the program.

Telemetry Requests:
Telemetry requests are SCPI commands that when recieved by a module cause it to load a certain data field into it's output buffer for the host to read. Pumpkin SCPI takes care of both the sending of the command and the reading of the data. The time delay between read and write commands is defined by the Intermessage Delay and ASCII delay boxes in the GUI. The data recieved by Pumpkin SCPI from the slave device is then formatted and displayed in the Output box. A listing of accepted telemetry requests can be found in the supporting documentation for each specific module.


**********
B. Using XML files
Pumpkin SCPI uses XML files to store command sets 
