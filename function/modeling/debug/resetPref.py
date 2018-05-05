import maya.cmds as cmds
import maya.mel as mel
import os
import getpass
def resetPref():
    username = getpass.getuser()
    MAYAVERSION = cmds.about(v=1)

    MAYA_scriptPath = mel.eval("getenv \"MAYA_SCRIPT_PATH\"")
    MAYA_scriptPath = MAYA_scriptPath.split(";")
    for i in MAYA_scriptPath:
        if i.endswith("Documents/maya/scripts"):
            PATH_Doc_maya = i[:-8]
    try: PATH_Doc_maya
    except: PATH_Doc_maya = "C:/Users/" + USER_name + "/Documents/maya"

    PATH_debug = PATH_Doc_maya + "/scripts/LD_MayaToolbox/function/modeling/debug"
    path_prefBat =  PATH_debug +"/prefmanage/get_userprefs_"+MAYAVERSION+".bat"
    os.startfile(path_prefBat)

#open maya

    path_mayaLoc =  mel.eval("getenv \"MAYA_LOCATION\"")
    path_maya = path_mayaLoc+"/bin/maya.exe"
    os.startfile(path_maya)
