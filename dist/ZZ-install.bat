: mklink "%userprofile%\Start Menu\Programs\Startup\script.exe" "dist/script/script.exe"

@echo off
set TARGET='%~dp0\script\script.exe'
set SHORTCUT='%userprofile%\Start Menu\Programs\Startup\script.lnk'
set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

%PWS% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%SHORTCUT%); $S.TargetPath = %TARGET%; $S.Save()"