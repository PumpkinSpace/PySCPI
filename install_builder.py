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
    # is Inno Setup 5 installed?
    print '**** this build requires \'Inno Setup 5\' ****'
    exit = True
# end

if exit:
    sys.exit()
# end

############## Modify Installer builder file for current file system ###########

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
        # this defined the source directory for this build, update it to this file system
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
        installer_dir = installer_dir.replace('\\', '/') #+ '/' + installer_name
        installer_dir_found = True      
    # end if
# end for
    
# Open the current installer file and replace all it's lines with the updated file system lines
installer_file = open(root+'/dist/installer_setup.iss', 'wb')
installer_file.writelines(new_lines)
installer_file.close()

time.sleep(1)
# install setup.py
inst = subprocess.Popen(['python', 'setup.py', 'install'], cwd=os.getcwd())
inst.wait()
print '\n## Setup.py installed\n'
time.sleep(1)

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
print '\n## Installer created\n'

time.sleep(1)
# attempt to run the installer
if installer_found and installer_dir_found and os.path.isfile(installer_dir + '/' + installer_name):
    stp = subprocess.Popen([installer_name], cwd = installer_dir, shell=True)
else:
    '*** No installer was found to open ***'
# end if
