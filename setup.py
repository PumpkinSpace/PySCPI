from distutils.core import setup
import py2exe
import sys
sys.path.insert(0, 'src/')
import aardvark_builder
import pySCPI_config
import SCPI_formatting
import aardvark_py
import os
from glob import glob

# get current working directory
root = os.getcwd()

# add .dll directory to system path
sys.path.append("C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")

# list of required .dll files
dll_files = [('src', [root + '/src/aardvark.dll']),('Microsoft.VC90.CRT', glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]

# find all .xml files in directory
xml_files = []

xml_list = os.listdir(root + '/xml_files')
for filename in xml_list:
    if 'example' in filename:
        xml_files = xml_files + [('xml_files', [root + '/xml_files/' + filename])]
    # end
# end

log_files = []

log_list = os.listdir(root + '/log_files')
for filename in log_list:
    if 'example' in filename:
        log_files = log_files + [('log_files', [root + '/log_files/' + filename])]
    # end
# end

# create the required setup configuration
setup(windows=[{'script':'pySCPI.pyw', # Top level file to read in
                'icon_resources': [(1, 'src/cubesatkit.ico')], # desired .exe icon
                'dest_base': 'pySCPI'}], # base directory
      data_files= dll_files + xml_files + log_files + # data file lists declared above
                  [('src', [root + '/src/Header.jpg']), # Header image for the GUI
                  ('src', [root + '/src/cubesatkit.ico']), # icon image for the program
                  ('src', [root + '/src/pySCPI README.txt'])], # readme file
      options = {'py2exe':{'includes': ['aardvark_builder', 'pySCPI_config', 'SCPI_formatting', 'aardvark_py'], # include files required by program
                           'dll_excludes': ['MSVCP90.dll'] # TODO!!!!!! should not need this exclude
                 }
                 }
      )