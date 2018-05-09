import maya.cmds as cmds
import maya.mel as mel

def add2Shelf():
    gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
    title = "LD MayaToolbox"
    currentShelf =cmds.tabLayout(gShelfTopLevel,h=300,q=1,st=1)
    cmds.setParent(gShelfTopLevel + "|" + currentShelf)

    PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")
    imagePath = PATH_MAYA_app_dir+ "/scripts/LD_MayaToolbox/pref/icon/LD_MayaToolbox.png"
    cmds.shelfButton(ann="Launch LD MayaToolbox",l=title,image1=imagePath,
    command='import maya.cmds as cmds\n\
import maya.mel as mel\n\
PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")\n\
sys.path.append(PATH_MAYA_app_dir+"/scripts/LD_MayaToolbox")\n\
cmds.evalDeferred("import LDMT")\n\
cmds.evalDeferred("reload(LDMT)")\n\
cmds.evalDeferred("from LDMT import *")\n\
cmds.evalDeferred("LDMT()") ')
