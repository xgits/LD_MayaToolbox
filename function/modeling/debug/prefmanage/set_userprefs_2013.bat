
@echo off

set docLoc=Documents

set mayaVersion=2013
echo Copying prefs directory...
rd /s /q "%userprofile%\%docLoc%\maya\%mayaVersion%"
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs"
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\scripts "%userprofile%\%docLoc%\maya\%mayaVersion%\scripts"
rd /s /q C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%

set mayaVersion="2013-x64"
echo Copying prefs directory...
rd /s /q "%userprofile%\%docLoc%\maya\%mayaVersion%"
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\prefs "%userprofile%\%docLoc%\maya\%mayaVersion%\prefs"
%systemroot%\system32\xcopy.exe /S /R /Y /C /V /I C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%\scripts "%userprofile%\%docLoc%\maya\%mayaVersion%\scripts"
rd /s /q C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox\pref\%mayaVersion%

if errorlevel 0 goto success
if errorlevel 1 goto nofiles
if errorlevel 4 goto nomem
if errorlevel 5 goto diskerr

:nofiles
echo no files found to be copied
echo this will tell you the file was copied
echo but the file did not. it is a problem with
echo microsofts implementation of xcopy and errror levels
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