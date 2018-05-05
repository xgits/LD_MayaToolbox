# Liudian
# gits@outlook.com
# www.xgits.com
import maya.cmds as cmds 
import maya.mel as mel
import sys
PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")
sys.path.append(PATH_MAYA_app_dir+'/scripts/LD_MayaToolbox')
cmds.evalDeferred("from LDMT import *")
cmds.evalDeferred("LDMT()") 
# userSetup exists
