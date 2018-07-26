'''
Auther: Liu Dian
github: https://github.com/xgits/LD_MayaToolbox
Email: xgits@outlook.com
Website: www.xgits.com
Not perfect though
'''

import maya.cmds as cmds
import maya.mel as mel

def ldmt_rebuildSubdiv():
    #Get the selected mesh
    selectedMesh=cmds.ls( selection=True )[0]
    #Get the vertex count i.e. vertex id of last vertex...
    vertexCount=cmds.polyEvaluate( v=1 )
    edgeCount=cmds.polyEvaluate(e=1 )
    vertexId = selectedMesh+'.vtx['+str(vertexCount)+']'
    #Convert selection to edges...
    x=cmds.polyListComponentConversion(vertexId,fv=True,te=True )
    cmds.select(x)

    #get the edges number...
    k=x[0].rfind(']')
    l=x[0].rfind('[')
    start = x[0][l+1:]
    edges = str(start[:-1])
    colon = edges.split(':')

    #Select edge loops and rings...
    mel.eval('SelectEdgeLoopSp;')
    mel.eval('SelectContiguousEdges;')
    mel.eval('polySelectEdgesEveryN "edgeRing" 2;')
    selectedEdges = cmds.ls(sl=1,fl=1)
    count=0
    while len(selectedEdges)<edgeCount*10/21:
        if count >3:
            break
        mel.eval('polySelectEdgesEveryN "edgeRing" 2;')
        mel.eval('SelectContiguousEdges;')
        selectedEdges = cmds.ls(sl=1,fl=1)
        count += 1

    mel.eval('polySelectEdgesEveryN "edgeRing" 2;')
    mel.eval('polySelectEdgesEveryN "edgeRing" 2;')

    #Delete the selected edgeloops
    cmds.polyDelEdge( cv=True )
    cmds.select(selectedMesh)