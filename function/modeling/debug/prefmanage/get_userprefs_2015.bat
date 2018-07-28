
@echo off

set docLoc=Documents
set mayaVersion=2015

%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs\hotkeys" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs\hotkeys
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs\shelves" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs\shelves
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I "%userprofile%\%docLoc%\maya\%mayaVersion%\scripts" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\scripts
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I "%userprofile%\%docLoc%\maya\%mayaVersion%\scripts" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\scripts
%systemroot%\system32\xcopy.exe /S /R /Y /C /V    "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs\userNamedCommands.mel" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs\userNamedCommands.mel*
%systemroot%\system32\xcopy.exe /S /R /Y /C /V    "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs\userRunTimeCommands.mel" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs\userRunTimeCommands.mel*
call C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\set_userprefs_2017.bat

set mayaVersion="2015-x64"

%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs\hotkeys" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs\hotkeys
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs\shelves" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs\shelves
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I "%userprofile%\%docLoc%\maya\%mayaVersion%\scripts" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\scripts
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I "%userprofile%\%docLoc%\maya\%mayaVersion%\scripts" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\scripts
%systemroot%\system32\xcopy.exe /S /R /Y /C /V    "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs\userNamedCommands.mel" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs\userNamedCommands.mel*
%systemroot%\system32\xcopy.exe /S /R /Y /C /V    "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs\userRunTimeCommands.mel" C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs\userRunTimeCommands.mel*
call C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\set_userprefs_2017.bat

if errorlevel 0 goto success
if errorlevel 1 goto nofiles
if errorlevel 4 goto nomem
if errorlevel 5 goto diskerr

:nofiles
echo no files found to be copied
goto exit

:nomem
echo no memory available or invalid drive name
goto exit

:diskerr
echo disk error occurred. contact your system admin
goto exit

:success
goto exit

:abort 
echo You pressed CTRL+C to end the copy operation. 
goto exit 

:exit
:pause