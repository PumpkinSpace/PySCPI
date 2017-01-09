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

setup(windows=[{'script':'pySCPI.pyw', 
                'icon_resources': [(1, 'src/cubesatkit.ico')], 
                'dest_base': 'Pumpkin SCPI'}],
      data_files=[('src', [root + '/src/aardvark.dll']), 
                  ('src', [root + '/src/Pumpkin_Inc_Logo-medium.gif']), 
                  ('src', [root + '/src/cubesatkit.ico']),
                  ("Microsoft.VC90.CRT", glob(r'C:\Program Files\Microsoft Visual Studio 9.0\VC\redist\x86\Microsoft.VC90.CRT\*.*')),
                  ('src', [root + '/src/pySCPI README.txt'])],
      options = {'py2exe':{'includes': ['aardvark_builder', 'pySCPI_config', 'SCPI_formatting', 'aardvark_py']                       
                 }
                 }
      )