: mklink "%userprofile%\Start Menu\Programs\Startup\client.exe" "dist/client/client.exe"

@echo off
set TARGET='%~dp0\client\client.exe'
set SHORTCUT='%userprofile%\Start Menu\Programs\Startup\client.lnk'
set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

%PWS% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%SHORTCUT%); $S.TargetPath = %TARGET%; $S.Save()"