import maya.cmds as cmds
import maya.api.OpenMaya as om2
def selectUVEdgeBorders():
    try:
        sel = cmds.ls(sl=1,o=1)
        sel = sel[0]
        selList = om2.MSelectionList()
        selList.add(sel)
        selPath = selList.getDagPath(0)
        selEdgeIter = om2.MItMeshEdge(selPath)
        cmds.select(sel+'.map[*]',r=1)
        newSelection = cmds.polySelectConstraint(uv=1,bo=0,m=2,returnSelection=1) 
        newSelection = cmds.polySelectConstraint(t=0x0010,uv=0,bo=1,m=2,returnSelection=1)
        cmds.polySelectConstraint(dis=1)
        cmds.select(cl=1)
        finalBorder = []
        uvBorder = cmds.polyListComponentConversion(newSelection,te=1,internal=1)
        uvBorder = cmds.ls(uvBorder,fl=1)
        for border in uvBorder:
            borderUV = cmds.polyListComponentConversion(border,tuv=1)
            borderUV = cmds.ls(borderUV,fl=1)
            if len(borderUV) > 2:
                finalBorder.append(border)
        #HardBorder    
        hardBorder = []
        while not selEdgeIter.isDone():
            edgeIndex = selEdgeIter.index()
            if selEdgeIter.onBoundary():
                hardBorder.append(sel+'.e['+str(edgeIndex)+']')
            selEdgeIter.next()
        cmds.select(finalBorder+hardBorder,r=1)
    except:
        print("TIP: There is no selection, select something first!")
