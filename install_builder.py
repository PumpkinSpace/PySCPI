#!/usr/bin/env python
###########################################################################
#(C) Copyright Pumpkin, Inc. All Rights Reserved.
#
#This file may be distributed under the terms of the License
#Agreement provided with this software.
#
#THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,
#INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND
#FITNESS FOR A PARTICULAR PURPOSE.
###########################################################################
"""
@package install_builder.py
Script to check for errors in the code and then build the exeutable file
and installer for pySCPI.
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.0' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports

import subprocess
import os
import sys
import imp

# append file directory to the PYTHONPATH
sys.path.append('src/')

# remove unicode references to files in PYTHONPATH so that subprocess works
while u'C:\\Users\\pumpkinadmin\\Desktop\\Codebase\\PySCPI' in sys.path:
    sys.path.remove(u'C:\\Users\\pumpkinadmin\\Desktop\\Codebase\\PySCPI')
# end while

# re-add the non-unicode reference to PYTHONPATH
sys.path.append('C:\\Users\\pumpkinadmin\\Desktop\\Codebase\\PySCPI')

# flag to control exit from the program
exit_flag = False


######################## Check program dependancies #######################
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


###################### Run Static Analysis on pySCPI ######################
if not exit_flag:
    print '\nPerforming static analysis on the pySCPI code...'
    
    # list to fill with errors
    error_buffer = []
    
    # files to run static analysis on (relative to the root directory)
    file_list = ['pySCPI.pyw', 'setup.py', 'install_builder.py', 
                 'src/pySCPI_config.py', 'src/pySCPI_gui.py',
                 'src/pySCPI_aardvark.py', 'src/pySCPI_threading.py',
                 'src/pySCPI_XML.py']         

    # iterate through the desired files            
    for filename in file_list:
        # perform static analysis on the file
        (lint_stdout, lint_stderr) = lint.py_run(filename, return_std=True)
    
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


########### Modify Installer builder file for current file system #########
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
            
        else:
            new_lines.append(line)
        # end if
        
        if line.startswith('OutputBaseFilename'):
            # this detotes the name of the installer that will be created
            installer_name = '' + line.split('=')[1].strip() + '.exe'
            installer_found = True
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


############################# Install Setup.py ############################
if not exit_flag:
    print "Installing setup.py"
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


############################### run py2exe ################################
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

########################## Build the Installer ############################
if not exit_flag:
    print '\nCreating the installer for pySCPI\n'
    
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


########################## Run the Installer ############################
if not exit_flag:
    print '\nOpening the Installer'
    # attempt to run the installer
    
    if installer_found and installer_dir_found and os.path.isfile(installer_dir + '/' + installer_name):
        stp = subprocess.Popen([installer_name], cwd = installer_dir, shell=True)
        
        print 'Install building process completed successfully!'
        
    else:
        print '\n*** No installer was found to open ***'
    # end if
# end if

# keep the console open
input()s