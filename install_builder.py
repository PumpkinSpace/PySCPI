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

dist_dir = root + '\\dist\\'
dist_list = os.listdir(dist_dir)

no_source_yet = True

source_start = 'Source: "'  + dist_dir
source_mid = '"; DestDir: "{app}'
source_ignore = ' recursesubdirs createallsubdirs'
source_end = '"; Flags: ignoreversion'

for line in installer_text:
    if line.startswith('Source'):
        if no_source_yet:
            for item in dist_list:
                if (('.' not in item) or item.endswith('.CRT')) and (item != 'Output'):
                    # it is a folder
                    new_lines.append(source_start + item + '\\*' + source_mid + '\\' + item + source_end + source_ignore + '\n')
                elif not(item.endswith('.md') or item.startswith('.') or item.endswith('.iss') or item.endswith('.log') or (item == 'Output')):
                    new_lines.append(source_start + item + source_mid + source_end + '\n')
                # end if
            # end for
            no_source_yet = False
        # end if
    else:
        new_lines.append(line)
    # end if
# end for
    
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
