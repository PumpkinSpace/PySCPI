#!/usr/bin/env python
################################################################################
#(C) Copyright Pumpkin, Inc. All Rights Reserved.
#
#This file may be distributed under the terms of the License
#Agreement provided with this software.
#
#THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,
#INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE.
################################################################################
"""
@package install_builder.py
Script to check for errors in the code and then build the exeutable file
and installer for pySCPI.
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.6' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import subprocess
import os
import sys
import imp
import xml.etree.ElementTree as ET
import shutil

# append file directory to the PYTHONPATH
sys.path.append('src/')
sys.path.append('C:\\Python27\\Scripts')

# remove unicode references to files in PYTHONPATH so that subprocess works
for path in sys.path:
    if isinstance(path, unicode):
        sys.path.remove(path)
        new_path = path.encode('ascii', 'ignore')
        sys.path.append(new_path)
    # end if
# end for

# flag to control exit from the program
exit_flag = False

######################## Check program dependancies ############################
# Requires pylint Installed 
try:
    # does pylint exist?
    from pylint import epylint as lint
except ImportError, e:
    # pylint is not installed to exit the program
    print '**** this build requires \'pylint\' ****'
    exit_flag  = True
# end try

# Requires py2exe Installed
try:
    # Does py2exe exist?
    imp.find_module('py2exe')
except ImportError, e:
    # py2exe is not installed so exit the program
    print '**** this build requires \'py2exe\' ****'
    exit_flag = True
# end try

# Requires Inno Setup 5 Installed
if not os.path.isdir('C:/Program Files (x86)/Inno Setup 5'):
    # Inno Setup 5 is not installed so exit the program
    print '**** this build requires \'Inno Setup 5\' ****'
    exit_flag = True
# end try


###################### Run Static Analysis on pySCPI ###########################
if not exit_flag:
    print '\nPerforming static analysis on the pySCPI code...'
    
    # list to fill with errors
    error_buffer = []
    
    # files to run static analysis on (relative to the root directory)
    file_list = ['pySCPI.pyw', 'setup.py', 'install_builder.py', 
                 'src/pySCPI_config.py', 'src/pySCPI_gui.py',
                 'src/pySCPI_aardvark.py', 'src/pySCPI_threading.py',
                 'src/pySCPI_XML.py']   
    
    # xml files to verify the validity of
    xml_list = ['src/SCPI_Commands.xml', 'src/pySCPI_config.xml']
    
    # list of .py file version numbers
    version_list = []

    # iterate through the desired files            
    for filename in file_list:
        # perform static analysis on the file
        (lint_stdout, lint_stderr) = lint.py_run(filename, return_std=True)
        
        py_file = open(filename, 'r')
        file_lines = py_file.readlines()
        
        # extract the version number for each file
        for line in file_lines:
            if line.startswith('__version__'):
                version_list = version_list + [line.split('\'')[1]]
            # end if
        # end for
    
        # add all output to the buffer of errors
        error_buffer = error_buffer + lint_stdout.buf.split('\n')
        
        # remove subdirectories from filename
        if '/' in filename:
            print_name = filename.split('/')[1]
            
        else:
            print_name = filename
        # end if
        
        # add extra tabs to short filenames
        if len(print_name) < 16:
            print_name = print_name + '\t'
        # end if
            
        # print the progress
        print '\t' + print_name + '\tanalysis complete'
    # end for
    
    # add all example .xml files to the xml_list
    for filename in os.listdir(os.getcwd() + '/xml_files'):
        if ((filename == 'aardvark_script.xml') or 
            filename.endswith('example.xml')):
            # add to the xml_list
            xml_list = xml_list + ['xml_files/' + filename]
        # end if
    # end for
    
    # attempt to parse all of the xml files
    for filename in xml_list:
        # attempt to parse each xml file
        try:
            x = ET.parse(filename)
            
            # remove subdirectories from filename
            if '/' in filename:
                print_name = filename.split('/')[1]
                
            else:
                print_name = filename
            # end if
        
            # add extra tabs to short filenames
            if len(print_name) < 16:
                print_name = print_name + '\t'
            # end if
            
            # print the progress
            print '\t' + print_name + '\tanalysis complete'
        
        except ET.ParseError as e:
            # remove subdirectories from filename
            if '/' in filename:
                print_name = filename.split('/')[1]
                
            else:
                print_name = filename
            # end if            
            error_buffer = error_buffer + [print_name+': Parse error - '+str(e)]
        # end try
    # end for  
    
    # check if all version numbers are the same
    if all(n == version_list[0] for n in version_list):
        exe_version = version_list[0]
    
    else:
        # convert the version numbers of each file into actual numbers
        version_numbers = []
        for version in version_list:
            version_split = version.split('.')
            version_number = 100000*int(version_split[0]) + \
                1000*int(version_split[1]) + int(version_split[2])
            version_numbers = version_numbers + [version_number]
        # end for
        
        # find the indeces of all files that are behind in revs.
        lagging_indices = [i for i, x in enumerate(version_numbers) 
                           if x == min(version_numbers)]
        
        exe_version = version_list[lagging_indices[0]]
        
        lagging_files = [file_list[x] for x in lagging_indices]
        
        for filename in lagging_files:
            # remove subdirectories from filename
            if '/' in filename:
                print_name = filename.split('/')[1]
                
            else:
                print_name = filename
            # end if   
            
            # log the version warning
            version_warning = '; version warning - The version number in'+\
                ' this file is behind the others'
            
            error_buffer = error_buffer + [' ' + print_name + version_warning]
        # end for
    # end if

    # check to see if any warnings were raised
    if any(' warning ' in item for item in error_buffer):
        # warnings were raised so print all of the warnings
        print '\n*** Warning were raised raised: ***'
        for item in error_buffer:
            # print each warning
            if ' warning ' in item:
                print '\t' + item
            # end if
        # end for
    # end if     
    
    # check to see if any errors were found in the code
    if any(' error ' in item for item in error_buffer):
        # errors were found so print all of the errors
        print '\n*** Errors found: ***'
        for item in error_buffer:
            # print each error
            if ' error ' in item:
                print '\t' + item
            # end if
        # end for
        
        # exit
        print '\n*** Fix these errors and re-run install_builder.py ***'
        exit_flag = True
    # end if
# end if


########### Modify Installer builder file for current file system ##############
if not exit_flag:
    # get current directory
    root = os.getcwd()
    
    # open installer file
    installer_file = open(root+'/dist/installer_setup.iss', 'rb')
    
    # read its lines
    installer_text = installer_file.readlines()
    
    # close the file
    installer_file.close()
    
    new_lines = []
    
    # destination of the distributable files
    dist_dir = root + '\\dist'
    # file list of that directory
    dist_list = os.listdir(dist_dir)
    
    # default installer name
    installer_name = ''
    installer_found = False
    installer_dir_found = False
    installer_dir = ''
    
    for line in installer_text:
        if line.startswith('SourceDir'):
            # this defined the source directory for this build, 
            # update it to this file system
            new_lines.append('SourceDir='+dist_dir + '\n')
            
        elif line.startswith('OutputBaseFilename'):
            # this detotes the name of the installer that will be created
            installer_name = 'pySCPI v' + exe_version + ' setup'
            installer_found = True
            new_lines.append('OutputBaseFilename='+installer_name + '\n')
            installer_name = installer_name + '.exe'
            
        elif line.startswith('AppVersion'):
            # this is the app version line
            new_lines.append('AppVersion=' + exe_version + '\n')
            
        else:
            new_lines.append(line)
        # end if
                
        if line.startswith('OutputDir'):
            # this line specifies where the installer will be put
            installer_dir = dist_dir + '\\' + line.split('=')[1].strip()
            installer_dir = installer_dir.replace('\\', '/')
            installer_dir_found = True      
        # end if
    # end for
        
    # Open the current installer file and replace all it's lines 
    # with the updated file system lines
    installer_file = open(root+'/dist/installer_setup.iss', 'wb')
    installer_file.writelines(new_lines)
    installer_file.close()
# end if


############################# Install Setup.py #################################
if not exit_flag:
    print "\nInstalling setup.py"
    # install setup.py
    inst = subprocess.Popen(['python', 'setup.py', 'install'], 
                            cwd=os.getcwd(), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    
    # get output from the subprocess
    out, err = inst.communicate()
    
    error_log = []
    warning_log = []
    # check the error log for issues
    for error in err.split('\n'):
        if 'error' in error.lower().strip():
            # an error was found so log it
            error_log = error_log + [error]
        
        elif 'UserWarning' in error:
            # a warning was found so log it
            warning_log = warning_log + [error]
        #end if
    # end for
    
    # see if warnings were found
    if len(warning_log) > 0:
        # warnings were found so print them all
        print '\n*** Warnings were raised: ***'
        for warning in warning_log:
            print '\t' + warning
        # end for
    # end if
    
    # see if errors were found
    if len(error_log) > 0:
        # they were found so print them all
        print len(error_log)
        print '\n*** Errors occurred: ***'
        
        for error in error_log:
            print '\t' + error
        # end for
        
        # exit
        print '\n*** Fix these errors and re-run install_builder.py ***'  
        exit_flag = True

    else:
        print '\nsetup.py Installation complete\n\n'
    # end if
# end if


############################### run py2exe #####################################
if not exit_flag:
    print '\nCreating the executable file\n'
    # build the .exe file
    exe = subprocess.Popen(['python', 'setup.py', 'py2exe'], 
                           cwd=os.getcwd(), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    
    # get the output from the process
    out, err = exe.communicate()
    
    # look for errors
    if len(err) == 0:
        # no errors were found
        print 'Executable file created successfully\n\n'
        
    else:
        # errors were found so print them all
        print '\n*** Errors occurred: ***'
        for error in err.split('\n'):
            print '\t' + error
        # end for
        print '\n*** Fix these errors and re-run install_builder.py ***' 
        exit_flag = True
    # end if
# end if

########################## Build the Installer #################################

if not exit_flag:   
    print '\nCreating the installer for pySCPI\n'
    
    # remove the old installer
    shutil.rmtree(installer_dir)     
    
    # full filename of the fuile that controls the installer generation
    install_file = os.getcwd().replace('\\', '/') +\
        '/dist/installer_setup.iss'
    
    # build the installer
    bld = subprocess.Popen(['iscc', install_file], 
                           cwd = 'C:/Program Files (x86)/Inno Setup 5', 
                           shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    
    # get output from the process
    out, err = bld.communicate()
    
    # look for errors
    if len(err) > 0 and 'Successful compile' not in out:
        # fatal errors were found
        print '/n*** Errors occurred: ***'
        print err
        exit_flag = True
        
        print '*** Errors caused the installer to fail ***'
    
    elif 'Successful compile' in out:
        # non-fatal errors were found (assuming these are warnings)
        if len(err) > 0:
            print'\n*** Warnings were raised: ***'
            print err
        # end if
        print 'Installer Created Successfully!\n\n'
        
    else:
        # some case that was not thought of occurred
        print "\n*** Something unexpected happened ***"
        
    # end if
# end if


########################## Run the Installer ###################################
if not exit_flag:
    print 'Opening the Installer'
    # attempt to run the installer
    
    if (installer_found and installer_dir_found and 
        os.path.isfile(installer_dir + '/' + installer_name)):
        
        # run the installer
        stp = subprocess.Popen([installer_name], cwd=installer_dir, shell=True)
        
        print '\nInstall building process completed successfully!'
        
    else:
        print '\n*** No installer was found to open ***'
    # end if
# end if

# keep the console open
input()