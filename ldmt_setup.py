'''
Auther: Liu Dian
This is called by ldmt_install.mel, used to install this maya toolbox.
'''
import os
import sys
import shutil
import ConfigParser
import maya.cmds as cmds
import maya.mel as mel
from ldmt_core import ldmt_cmds as ld

def install():
    '''
    1. Install files
    2. Insert codes to userSetup.py to show ui on startup
    '''
    # Get path
    sourceFolderPath = sys.path[0]  
    topFolderName = 'LDMT'
    mayaScriptPath = getMayaScriptPath()
    ldmtPath = mayaScriptPath + '/' + topFolderName

    sys.path.remove(sourceFolderPath)
    sys.path.insert(0,ldmtPath)

    # Install files
    deleteAndCopy(sourceFolderPath, ldmtPath)
    # Insert userSetup
    insertUserSetup(mayaScriptPath, ldmtPath)
    # showUI
    showUI(ldmtPath)
    # Add to shelf
    add2Shelf()

def getMayaScriptPath():
    mayaScriptPath = os.environ['MAYA_SCRIPT_PATH']
    mayaScriptPath = mayaScriptPath.split(';')
    for eachPath in mayaScriptPath:
        if eachPath.endswith('maya/scripts'):
            mayaScriptPath = eachPath
    return mayaScriptPath


def deleteAndCopy(sourcePath, targetPath):
    # If exsits, delete in case error
    if os.path.isdir(targetPath):
        try:
            shutil.rmtree(targetPath)
        except:
            ld.msg("Delete failed!")
    # Copy To Target Path
    try:
        shutil.copytree(sourcePath, targetPath)
    except:
        ld.msg("Copy failed!")

def insertUserSetup(mayaScriptPath, ldmtPath):
    # Insert cmds into userSetup.py
    userSetupFilePath = mayaScriptPath + '/userSetup.py'
    sourceFilePath = ldmtPath + '/userSetup.py'
    if not os.path.isfile(userSetupFilePath):
        shutil.copyfile(sourceFilePath,userSetupFilePath)
    else:
        userSetupFile = open(userSetupFilePath,'r')
        currentLines = userSetupFile.readlines()
        userSetupFile.close()

        userSetupFile = open(userSetupFilePath,'w')
        ifWriteThisLine = 1
        for index, line in enumerate(currentLines):
            if line.startswith('#LDMT'):
                ifWriteThisLine -= 1
            if ifWriteThisLine == 1 or ifWriteThisLine == -1:
                userSetupFile.write(line)
        
        sourceSetupFile = open(sourceFilePath,'r')
        sourceLines = sourceSetupFile.readlines()
        for index, line in enumerate(sourceLines):
            userSetupFile.write(line)
        sourceSetupFile.close()

def showUI(ldmtPath):
    sys.path.insert(0,ldmtPath+'/ldmt_function')
    import ldmt_ui
    reload(ldmt_ui)
    ldmt_ui.show()

def getMayaScriptPath():
    mayaScriptPath = os.environ['MAYA_SCRIPT_PATH']
    mayaScriptPath = mayaScriptPath.split(';')
    for eachPath in mayaScriptPath:
        if eachPath.endswith('maya/scripts'):
            mayaScriptPath = eachPath
    return mayaScriptPath

def add2Shelf():
    gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
    title = "ldmtButton"
    mayaScriptPath = getMayaScriptPath()
    currentShelf =cmds.tabLayout(gShelfTopLevel,h=300,q=1,st=1)
    buttonNames = cmds.shelfLayout(currentShelf,q=1,ca=1)
    for i in buttonNames:
        if i == "ldmtButton":
            return
    cmds.setParent(gShelfTopLevel + "|" + currentShelf)

    imagePath = mayaScriptPath+ "/LDMT/ldmt_icon/LDMT_pro.png"
    highlightImagePath = mayaScriptPath+ "/LDMT/ldmt_icon/LDMT_pro_highlight.png"
    cmds.shelfButton('ldmtButton',ann="Launch LD MayaToolbox",l=title,image=imagePath,highlightImage=highlightImagePath,
    command='import maya.cmds as cmds\n\
import maya.mel as mel\n\
PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")\n\
sys.path.append(PATH_MAYA_app_dir+"/scripts/LDMT")\n\
sys.path.append(PATH_MAYA_app_dir+"/scripts/LDMT/ldmt_function")\n\
cmds.evalDeferred("import ldmt_ui")\n\
cmds.evalDeferred("reload(ldmt_ui)")\n\
cmds.evalDeferred("from ldmt_ui import *")\n\
cmds.evalDeferred("show()") ')

