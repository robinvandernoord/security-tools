@echo off
set TARGET='%~dp0\client.exe'
set SHORTCUT='%userprofile%\Start Menu\Programs\Startup\client.lnk'
: TODO: add flag to use 'shell:common startup' folder instead of user specific one

set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

%PWS% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%SHORTCUT%); $S.TargetPath = %TARGET%; $S.Save()"
