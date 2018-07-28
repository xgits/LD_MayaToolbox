@echo off
setlocal enabledelayedexpansion

echo d| xcopy /y /c ".\*" "%userprofile%\Documents\maya\scripts\LD_MayaToolbox" /s 
echo d| xcopy /y /c ".\pref\2018\*" "%userprofile%\Documents\maya\2018" /s 
echo d| xcopy /y /c ".\pref\2017\*" "%userprofile%\Documents\maya\2017" /s 
echo d| xcopy /y /c ".\pref\2016.5\*" "%userprofile%\Documents\maya\2016.5" /s
echo d| xcopy /y /c ".\pref\2016\*" "%userprofile%\Documents\maya\2016" /s 
echo f| xcopy /y /c "%userprofile%\Documents\maya\scripts\userSetup.py" "%userprofile%\Documents\maya\scripts\userSetup_bak.py" /s 
echo f| xcopy /y /c ".\userSetup.py" "%userprofile%\Documents\maya\scripts\userSetup.py" /s 

exit