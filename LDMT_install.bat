@echo off
setlocal enabledelayedexpansion
 
echo d| xcopy /y /c ".\*" "C:\Users\%username%\Documents\maya\scripts\LD_MayaToolbox" /s 
echo f| xcopy /y /c "C:\Users\%username%\Documents\maya\scripts\userSetup.py" "C:\Users\%username%\Documents\maya\scripts\userSetup_bak.py" /s 
echo f| xcopy /y /c ".\pref\userSetup.py" "C:\Users\%username%\Documents\maya\scripts\userSetup.py" /s 
pause
exit