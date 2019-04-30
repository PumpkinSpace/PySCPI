; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; Application unique ID
AppId={{8C27620E-EEDD-49FD-9D68-775CC81BDDC1}
; Application info
AppName=pySCPI
AppVersion=0.3.6
AppPublisher=Pumpkin Inc.
AppPublisherURL=http://www.pumpkinspace.com/
AppSupportURL=http://www.pumpkinspace.com/
AppUpdatesURL=http://www.pumpkinspace.com/
AppCopyright=Copyright (C) 2017 Pumpkin Inc.
; Location where all of the source files can be found
SourceDir=C:\Pumpkin\PySCPI_src\dist
; Install loaction specifiers
DefaultDirName=C:\Pumpkin\pySCPI
DisableProgramGroupPage=yes
DisableDirPage=no
AlwaysShowDirOnReadyPage=yes
; Installer filename
OutputBaseFilename=pySCPI v0.3.6 setup
; Installer location
OutputDir=Installer
; Compression specifiers
Compression=lzma
SolidCompression=yes
; Image to use in the installer window
WizardImageStretch=yes
WizardSmallImageFile=src\CubeSatKit.bmp
#define MyAppExeName "PySCPI.exe"
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName=pySCPI




[Languages]
; Language to install in
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; Optional parts of the install process, not to be confused with Run directives
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}";

[Files]
; Files to be included along with the installer, ignore revision overwrites any previous versions
Source: "bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "CRYPT32.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "jpeg8-vc90-mt-x86.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "libmmd.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "library.zip"; DestDir: "{app}"; Flags: ignoreversion
Source: "libtiff-vc90-mt-x86.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "log_files\*"; DestDir: "{app}\log_files"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "Microsoft.VC90.CRT\*"; DestDir: "{app}\Microsoft.VC90.CRT"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "openjp2-vc90-mt.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "PIL._imaging.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "PIL._imagingtk.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "pySCPI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "python27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "pythoncom27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "pywintypes27.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "svml_dispmd.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "tcl\*"; DestDir: "{app}\tcl"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "tcl85.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "tk85.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "xml_files\*"; DestDir: "{app}\xml_files"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "zlib1-vc90-mt.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "_tkinter.pyd"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Icons to use for the program
Name: "{commonprograms}\pySCPI"; Filename: "{app}\pySCPI.exe"
Name: "{commondesktop}\pySCPI"; Filename: "{app}\pySCPI.exe"; Tasks: desktopicon

[Run]
; Prompt to run the Aardvark Driver Installer
Filename: "{app}\src\TotalPhaseUSB-v2.15.exe"; StatusMsg: "Installing Aardvark USB driver (Total Phase)"; Description: "Install the required Total Phase drivers for the Aarkvark"; Flags: skipifsilent hidewizard postinstall runascurrentuser
; Then run pySCPI
Filename: "{app}\pySCPI.exe"; Description: "{cm:LaunchProgram,pySCPI}"; Flags: postinstall skipifsilent
