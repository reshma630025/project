' TrustGuard AI — Silent Background Launcher for Windows Startup
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strPath = fso.GetParentFolderName(WScript.ScriptFullName)

' Run start_trustguard.bat in hidden window mode (0)
WshShell.CurrentDirectory = strPath
WshShell.Run "cmd /c """ & strPath & "\start_trustguard.bat""", 0, False
Set WshShell = Nothing
Set fso = Nothing
