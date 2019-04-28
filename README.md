# PySCPI
Python scripts for SCPI I2C commands


#### INSTALLING ####
To install the windows executable install using dist/Installer/pySCPI...
or run the "Run Installer.bat" script


####   NOTES   ####
pySCPI is written in python and has a few (but not many) dependencies so should run in a python environment on most PCs. 
For those of you that are comfortable with Python I would ask that you use the python source for pySCPI because it gives 
more detailed output if a crash does occur (provided that you run it in such a way that output is obtainable).

In order to make pySCPI more usable for non-python people, pySCPI is then compiled into an executable (on my machine) 
this executable is found in the \dist folder of the repository and it is my understanding that this will not necessarily 
run on other PCs as it was compiled on mine. setup.py in the root directory manages this compilation so is not quite 
the setup you may expect a file with such a name to be.

That is where the installer comes in, this allows pySCPI to be installed on any computer in such a way that it will 
run (hopefully, PLEASE let me know if you have issues here). This installer is located in /dist/Installer but can 
also be executed with hte newly created Run Installer.bat file in the root folder. 

install_builder.py is the script that creates the installer and has a few dependencies which most people won't just happen to have. 
This code should protect the installer from corruption if you don't have the correct dependencies, but it is probably best not 
to rely on that! So please do not run this file unless you know what you're doing.

In either the installed directory or the repository there is a SCPI_Commands.xml file. Feel free to add new SCPI telemetry items 
that you create to this file, the format should be obvious. If you edit this in the installed executable's directory note 
that it will not be under version control. 

In either the installed directory or the repository there is a psSCPI_config.xml file which contains the list of modules and 
their default I2C addresses. Feel free to add new modules to this file as required, the format should be obvious. 
Again, if you edit this in the installed executable's directory note that it will not be under version control. 
