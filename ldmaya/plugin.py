import maya.cmds as cmds
import maya.mel as mel
def ifExists(command):
    if not mel.eval('exists "'+command+'"'):
        return 0
    else:
        return 1
    