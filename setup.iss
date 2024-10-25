[Setup]
AppName=LIA Digital QT
AppVersion=1.0
DefaultDirName={pf}\LIA Digital QT
DefaultGroupName=LIA Digital QT
OutputBaseFilename=setup
SetupIconFile=lia_digital_qt.ico

[Files]
Source: "dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\main\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\LIA Digital QT"; Filename: "{app}\main.exe"; IconFilename: "{app}\lia_digital_qt.ico"
Name: "{group}\Uninstall LIA Digital QT"; Filename: "{uninstallexe}"