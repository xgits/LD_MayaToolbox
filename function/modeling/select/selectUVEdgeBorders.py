import maya.cmds as cmds
import maya.mel as mel
def selectUVEdgeBorders():
    finalborder = []
    sel = cmds.ls(sl=1,o=1)
    edges = cmds.polyListComponentConversion(sel,te=1)
    cmds.select(edges,r=1)
    cmds.polySelectConstraint(m=2,t=0x8000,sm=1)
    cmds.polySelectConstraint(dis=1)
    hardedges = cmds.ls(sl=1)

    seluv = cmds.polyListComponentConversion(sel,tuv=1)
    cmds.select(seluv)
    mel.eval("polySelectBorderShell 1;")
    uvborder = cmds.ls(sl=1)
    uvborder = cmds.polyListComponentConversion(uvborder,te=1,internal=1)
    uvborder = cmds.ls(uvborder,fl=1)
    for border in uvborder:
        borderuv = cmds.polyListComponentConversion(border,tuv=1)
        borderuv = cmds.ls(borderuv,fl=1)
        if len(borderuv) > 2:
            finalborder.append(border)

    cmds.select(finalborder,r=1)
    cmds.select(hardedges,add=1)
