import maya.cmds as cmds
import maya.mel as mel
def resetPivot():
    mod = cmds.getModifiers()
    if mod==0:
        mel.eval('FreezeTransformations;')
        mel.eval('ResetTransformations;')
    if mod==8:
        mel.eval('FreezeTransformations;')
    if mod == 4:
        mel.eval('xform -ws -t 0 0 0;')
    if mod== 1:
        mel.eval('CenterPivot;')
    if mod == 5:
        mel.eval('move -rpr 0 0 0;')
        mel.eval('FreezeTransformations;')
    if mod == 13:
        pivotWSPos = cmds.xform(q=1,ws=1,piv=1)
        mel.eval('move -rpr 0 0 0;')
        mel.eval('FreezeTransformations;')
        cmds.move(pivotWSPos[0],pivotWSPos[1],pivotWSPos[2],rpr=1)