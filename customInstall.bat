@echo off
setlocal enabledelayedexpansion

set /p mayaScriptPath=<customPath.txt

set installPath="%mayaScriptPath%\scripts\LD_MayaToolbox\"
set userSetupPath="%mayaScriptPath%\scripts\userSetup.py"
set userSetupBakPath="%mayaScriptPath%\scripts\userSetup_bak.py"

echo d|xcopy /y /c ".\*" %installPath% /s 
echo d|xcopy /y /c ".\pref\2018\*" "%mayaScriptPath%\2018" /s
echo d|xcopy /y /c ".\pref\2017\*" "%mayaScriptPath%\2017" /s
echo d|xcopy /y /c ".\pref\2016.5\*" "%mayaScriptPath%\2016.5" /s
echo d|xcopy /y /c ".\pref\2016\*" "%mayaScriptPath%\2016" /s

echo f|xcopy /y /c %userSetupPath% %userSetupBakPath% /s 
echo f|xcopy /y /c ".\userSetup.py" %userSetupPath% /s 

exit