@echo off
setlocal enabledelayedexpansion

echo d| xcopy /y /c ".\*" "%userprofile%\Documents\maya\scripts\LD_MayaToolbox" /s 
echo f| xcopy /y /c "%userprofile%\Documents\maya\scripts\userSetup.py" "%userprofile%\Documents\maya\scripts\userSetup_bak.py" /s 
echo f| xcopy /y /c ".\userSetup.py" "%userprofile%\Documents\maya\scripts\userSetup.py" /s 
pause
exit