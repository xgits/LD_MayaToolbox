import maya.cmds as cmds
import maya.mel as mel
def deleteHistory():
    mods = cmds.getModifiers()
    if(mods != 0):
        mel.eval('DeleteAllHistory;')
    else: 
        mel.eval('DeleteHistory;')