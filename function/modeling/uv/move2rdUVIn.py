# About ####################
# Auther:  Liu Dian
# Email:   xgits@outlook.com
# Website: www.xgits.com
# Version: Pro 
# License: GPL
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

def LD_move2rdUVIn():
    sel = cmds.ls(sl=1,o=1)
    sel = sel[0]
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    selMesh = om2.MFnMesh(selPath)

    uvid_uv = []  # generate {uvid:[u,v],} from MFnMesh.getUVs()
    uvNameIn2rd = []
    uvArray = selMesh.getUVs()

    for i in xrange(len(uvArray[0])):
        uvid_uv.append([uvArray[0][i],uvArray[1][i]])
        
    for uvid in xrange(len(uvid_uv)):
        u = uvid_uv[uvid][0]
        v = uvid_uv[uvid][1]
        if u>1 and u<2 and v>0 and v<1:
            uvNameIn2rd.append(sel+'.map['+str(uvid)+']')
    cmds.polyEditUV(uvNameIn2rd,u=-1)
                
