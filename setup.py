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
@package setup.py
Script to control the generation of the .exe for pySCPI
"""

__author__ = 'David Wright (david@pumpkininc.com)'
__version__ = '0.3.8' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
# -------
# Imports
from distutils.core import setup
import sys
sys.path.insert(0, 'src/')
import os
from glob import glob
import py2exe # is needed!!!

# dummy usage to suppress py2exe import warning
not_used = py2exe.__doc__


# get current working directory
root = os.getcwd()

# add .dll directory to system path
sys.path.append("C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")

# list of required .dll files
dll_files = [('src', [root + '/src/aardvark.dll']),
             ('Microsoft.VC90.CRT', 
              glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]

# find all .xml files in directory
xml_files = []

xml_list = os.listdir(root + '/xml_files')
for filename in xml_list:
    if 'example' in filename:
        # only include files that are labelled as examples
        xml_files = xml_files + [('xml_files', 
                                  [root + '/xml_files/' + filename])]
    # end
# end

log_files = []

log_list = os.listdir(root + '/log_files')
for filename in log_list:
    if 'example' in filename:
        # only include files that are labelled as examples
        log_files = log_files + [('log_files', 
                                  [root + '/log_files/' + filename])]
    # end
# end

# create the required setup configuration
setup(windows=[{'script':'pySCPI.pyw', # Top level file to read in
                'icon_resources': [(1, 'src/cubesatkit.ico')], # desired .exe icon
                'dest_base': 'pySCPI'}], # base directory
      data_files= dll_files + xml_files + log_files + # data file lists declared above
                  [('src', [root + '/src/Header.jpg']), # Header image for the GUI
                  ('src', [root + '/src/cubesatkit.ico']), # icon image for the program
                  ('src', [root + '/src/CubeSatKit.bmp']), # image for the install wizard
                  ('src', [root + '/src/pySCPI README.txt']), # readme file
                  ('src', [root + '/src/pySCPI_config.xml']), # configuration file
                  ('src', [root + '/src/SCPI_Commands.xml'])], # SCPI Command Library
      options = {'py2exe':{'includes': ['pySCPI_aardvark', 'pySCPI_config', 
                                        'pySCPI_formatting', 'aardvark_py', 
                                        'pySCPI_XML', 'pySCPI_gui'], # include files required by program
                           'dll_excludes': ['MSVCP90.dll']}} # TODO!!!!!! should not need this exclude
      )