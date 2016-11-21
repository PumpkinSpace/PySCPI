Welcome to pySCPI.

This porgram provides a PC based interface for using SCPI commands to communicate with Pumpkin modules with a SCPI command interfaces. This program can be used to send commands to modules aswell as recieving and formatting telemetry requests.

Contents:

1. Using PySCPI
	A. Using the GUI
	B. Sending SCPI commands
	C. Using XML files
	D. Common Issues 
2. Supported Modules
3. Adding Functionality

**********************
1. Using PySCPI
PySCPI provided a GUI to allow a user to send scpi commands to Pumpkin modules that have SCPI capabilities, this section covers the basics of using this program.

A. Using the GUI
The GUI is roughly laid out in two secions, inputs on the left and output on the right

Inputs:
'Load XML' Button: Loads commands from a .xml file that was previously saved by this program. see sction C for more details.

'View ReadMe' Button: Displays this file in the GUI Output window

Slave Settings: The dropdown menu allows Pumpkin module to be selected. This then updates the I2C address to the left with the default I2C address for that module. Additionally non-default Module addresses can be entered directly into the text box to the left. For more information on supported devices see section 2.

Intermessage Delay: This is the millisecond delay between I2C transactions sent from this program. This value can be changed as you see fit, short delays may cause bad data to be returned from telemetry requests so be wary of that.

Commands to be written box: This text box is where you should neter the commands that you want to be sent to the slave device. Enter commands one per line.

'Write XML' Button: Write the current configuration and SCPI commands to a .xml file. See section C for more details.

'Use Aardvark' Button: This button initiates I2C transmission through the Aardvark device, sending the requested commands with the given configuration. This button will remain red and disabled for the duration of the transmission.

Ouput Box: This text box is where output from the program is written. This may take the form of data returned, system messages or errors produced. For common erros see section D.