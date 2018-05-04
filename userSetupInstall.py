import os
import getpass
import shutil
username = getpass.getuser()
currentDir = os.getcwd()
ifexists = 0 
sourceFile = currentDir+'\\pref\\userSetup.py'
targetFile = 'C:\\Users\\'+ username + '\\Documents\\maya\\scripts\\userSetup.py'

if os.path.exists(targetFile):
    target = open(targetFile, 'r')
    target_lines = target.readlines()
    for i in range(len(target_lines)):
        if "# userSetup exists" in target_lines[i]:
            ifexists = 1
    if ifexists == 0:
        with open(targetFile, 'a') as target:
            source = open(sourceFile,'r')
            lines = source.readlines()
            for i in range(len(lines)):
                target.write(lines[i])
else:
    shutil.copy(sourceFile,targetFile)