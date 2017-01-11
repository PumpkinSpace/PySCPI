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
sys.path.append("C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")

root = os.getcwd()

dll_files = [('src', [root + '/src/aardvark.dll']),('Microsoft.VC90.CRT', glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*'))]

xml_files = []

xml_list = os.listdir(root + '/xml_files')
for filename in xml_list:
    if 'example' in filename:
        xml_files = xml_files + [('xml_files', [root + '/xml_files/' + filename])]
    # end
# end

setup(windows=[{'script':'pySCPI.pyw', 
                'icon_resources': [(1, 'src/cubesatkit.ico')], 
                'dest_base': 'pySCPI'}],
      data_files= dll_files + xml_files +  
                  [('src', [root + '/src/Header.jpg']), 
                  ('src', [root + '/src/cubesatkit.ico']),
                  ('src', [root + '/src/pySCPI README.txt'])],
      options = {'py2exe':{'includes': ['aardvark_builder', 'pySCPI_config', 'SCPI_formatting', 'aardvark_py'],
                           'dll_excludes': ['MSVCP90.dll']
                 }
                 }
      )