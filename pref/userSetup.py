# Liudian
# gits@outlook.com
# www.xgits.com
import maya.cmds as cmds 
import maya.mel as mel
import getpass
import sys
username = getpass.getuser()
sys.path.append('c:/Users/'+username+'/Documents/maya/scripts/LD_MayaToolbox')
cmds.evalDeferred("from LDMT import *")
cmds.evalDeferred("LDMT()") 
# userSetup exists
