import maya.cmds as cmds
def selectHardEdges():
    selList = cmds.ls(sl=1)
    if selList!=[]:
        edges = cmds.polyListComponentConversion(selList,te=1)
        cmds.select(edges,r=1)
        cmds.polySelectConstraint(m=2,t=0x8000,sm=1)
        cmds.polySelectConstraint(dis=1)