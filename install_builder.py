import subprocess
import os
import time

exit = False
######################### Requires py2exe Installed ########################
try:
    # Does py2exe exist?
    import py2exe
except ImportError, e:
    print '**** this build requires \'py2exe\' ****'
    exit = True
# end

if not os.path.isdir('C:/Program Files (x86)/Inno Setup 5'):
    # is Toon Setup 5 installed?
    print '**** this build requires \'Inno Setup 5\' ****'
    exit = True
# end

if exit:
    sys.exit()
# end

inst = subprocess.Popen(['python', 'setup.py', 'install'], cwd=os.getcwd())
inst.wait()
print '## Setup.py installed'

exe = subprocess.Popen(['python', 'setup.py', 'py2exe'], cwd=os.getcwd())
exe.wait()
time.sleep(1)
print '## .exe created'

time.sleep(2)
install_file = os.getcwd().replace('\\', '/') + '/dist/installer_setup.iss'

bld = subprocess.Popen(['iscc', install_file], cwd = 'C:/Program Files (x86)/Inno Setup 5', shell=True)
bld.wait()
print '## Installer created'
