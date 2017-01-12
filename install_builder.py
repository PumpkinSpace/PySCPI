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

############## Modify Installer builder file for current file system ###########
root = os.getcwd()

# open installer file
installer_file = open(root+'/dist/installer_setup.iss', 'rb')

installer_text = installer_file.readlines()

installer_file.close()

new_lines = []

# replace text as needed
for line in installer_text:
    if '"C:\\' in line:
        # is a line to change
        start_index = line.index('C:\\') # beginning of previous absolute directory
        stop_index = line.index('\\dist\\') # end of previous absolute directory
        new_lines.append(line.replace(line[start_index:stop_index], root)) # replace
    else:
        new_lines.append(line)
    # end    
# end
installer_file = open(root+'/dist/installer_setup.iss', 'wb')
installer_file.writelines(new_lines)
installer_file.close()

# install setup.py
inst = subprocess.Popen(['python', 'setup.py', 'install'], cwd=os.getcwd())
inst.wait()
print '\n## Setup.py installed\n'

# build the .exe file
exe = subprocess.Popen(['python', 'setup.py', 'py2exe'], cwd=os.getcwd())
exe.wait()
time.sleep(1)
print '\n## .exe created\n'
time.sleep(2)

# create the installer file for the program
install_file = os.getcwd().replace('\\', '/') + '/dist/installer_setup.iss'

bld = subprocess.Popen(['iscc', install_file], cwd = 'C:/Program Files (x86)/Inno Setup 5', shell=True)
bld.wait()
print '\n## Installer created'
