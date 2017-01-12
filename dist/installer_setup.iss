; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{8C27620E-EEDD-49FD-9D68-775CC81BDDC1}
AppName=pySCPI
AppVersion=1.1
;AppVerName=pySCPI 1.1
AppPublisher=Pumpkin Inc.
AppPublisherURL=http://www.pumpkinspace.com/
AppSupportURL=http://www.pumpkinspace.com/
AppUpdatesURL=http://www.pumpkinspace.com/
DefaultDirName={pf}\Pumpkin\pySCPI
DisableProgramGroupPage=yes
OutputBaseFilename=pySCPI setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "install_usb"; Description: "Install Aardvark USB Drivers from TotalPhase"; GroupDescription: "External drivers:";
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\CRYPT32.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\jpeg8-vc90-mt-x86.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\libmmd.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\libtiff-vc90-mt-x86.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\log_files\*"; DestDir: "{app}\log_files"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\Microsoft.VC90.CRT\*"; DestDir: "{app}\Microsoft.VC90.CRT"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\openjp2-vc90-mt.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\PIL._imaging.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\PIL._imagingtk.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\pySCPI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\python27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\pythoncom27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\pywintypes27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\svml_dispmd.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\tcl\*"; DestDir: "{app}\tcl"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\tcl85.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\tk85.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\win32api.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\win32evtlog.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\win32pipe.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\win32ui.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\xml_files\*"; DestDir: "{app}\xml_files"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\zlib1-vc90-mt.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\_cffi_backend.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\_tkinter.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\David\Desktop\Codebase\PySCPI\dist\_win32sysloader.pyd"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{commonprograms}\pySCPI"; Filename: "{app}\pySCPI.exe"
Name: "{commondesktop}\pySCPI"; Filename: "{app}\pySCPI.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\pySCPI.exe"; Description: "{cm:LaunchProgram,pySCPI}"; Flags: nowait postinstall skipifsilent
Filename: "{app}\src\TotalPhaseUSB-v2.15.exe"; StatusMsg: "Installing USB driver (IVI Foundation)"; Check: Not IsWin64(); Tasks: install_usb; Flags: skipifsilent
Filename: "{app}\src\TotalPhaseUSB-v2.15.exe"; StatusMsg: "Installing USB driver (IVI Foundation)"; Check: IsWin64(); Tasks: install_usb; Flags: skipifsilent
