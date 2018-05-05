@echo off
setlocal enabledelayedexpansion

set /p mayaScriptPath=<customPath.txt

set installPath="%mayaScriptPath%\LD_MayaToolbox\"
set userSetupPath="%mayaScriptPath%\userSetup.py"
set userSetupBakPath="%mayaScriptPath%\userSetup_bak.py"

echo d|xcopy /y /c ".\*" %installPath% /s 
echo f|xcopy /y /c %userSetupPath% %userSetupBakPath% /s 
echo f|xcopy /y /c ".\userSetup.py" %userSetupPath% /s 
pause
exit