import subprocess
import os
import time

inst = subprocess.Popen(['python', 'setup.py', 'install'], cwd=os.getcwd())
inst.wait()
print '## Setup.py installed'

exe = subprocess.Popen(['python', 'setup.py', 'py2exe'], cwd=os.getcwd())
exe.wait()
time.sleep(1)
print '## .exe created'

install_file = os.getcwd().replace('\\', '/') + '/dist/installer_setup.iss'

bld = subprocess.Popen(['iscc', install_file], cwd = 'C:/Program Files (x86)/Inno Setup 5', shell=True)
bld.wait()
print '## Installer created'
