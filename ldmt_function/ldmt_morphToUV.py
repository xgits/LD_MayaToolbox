import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
def deleteNoUV():
    selObj = cmds.ls(sl=1,o=1)
    selObj = selObj[0]
    selObj_face = selObj + '.f[*]'
    selObj_face = cmds.ls(selObj_face, fl=1)
    selObj_uv = cmds.polyListComponentConversion(selObj,tuv=1)
    selObj_face_hasUV = cmds.polyListComponentConversion(selObj_uv,tf=1)
    selObj_face_hasUV = cmds.ls(selObj_face_hasUV, fl=1)
    selObj_face_noUV = list(set(selObj_face).difference(set(selObj_face_hasUV)))
    if selObj_face_noUV:
        cmds.delete(selObj_face_noUV)
    return selObj
    
def splitIfOnUVBorder():
    sel = cmds.ls(sl=1,o=1)
    sel = sel[0]
    selList = om2.MGlobal.getActiveSelectionList()
    selListPath = selList.getDagPath(0)
    vertIt = om2.MItMeshVertex(selListPath)
    selMesh = om2.MFnMesh(selListPath)
    vertIdToSplit = []
    vertToSplit = []
    while not vertIt.isDone():
        uvIndices = vertIt.getUVIndices()
        uvIndices = list(set(uvIndices))
        if len(uvIndices)>=2:
            vertIdToSplit.append(vertIt.index())
        elif vertIt.onBoundary():
            vertIdToSplit.append(vertIt.index())
        vertIt.next()
    for i in range(len(vertIdToSplit)):
        vertToSplit.append(sel+'.vtx['+str(vertIdToSplit[i])+']')
    cmds.polySplitVertex(vertToSplit,cch=0)
    
def morph2UV():
    sel = cmds.ls(sl=1,o=1)
    sel = sel[0]
    selList = om2.MSelectionList()
    selList.add(sel)
    path = selList.getDagPath(0)
    myMesh = om2.MFnMesh(path)
    newPointArray = om2.MPointArray()
    space = om2.MSpace.kWorld
    myMesh_UVs = myMesh.getUVs()
    myMesh_points = myMesh.getPoints()
    # for i in range(myMesh.numVertices):
    myMesh_itVertex = om2.MItMeshVertex(path)
    points = om2.MPointArray()
    while not myMesh_itVertex.isDone():
        vertIndex = myMesh_itVertex.index()
        gotUV = myMesh_itVertex.getUV()
        point = om2.MPoint(gotUV[0],gotUV[1],0)
        points.append(point)
        myMesh_itVertex.next()
    myMesh.setPoints(points,space)
    
def runMorph2UV():
    baseObj = cmds.ls(sl=1,o=1)   #1. inputmesh
    baseObjDup = cmds.duplicate() #2. duplicate
    mel.eval("FreezeTransformations")
    mel.eval("ResetTransformations")
    baseObj = baseObjDup[0]
    deleteNoUV()
    splitIfOnUVBorder()
    morph2UV()
    currentSelection = cmds.ls(sl=1)
    currentUV  = cmds.polyListComponentConversion(currentSelection,tuv=1)
    cmds.polyMergeVertex(currentSelection,d=0.0001,cch=0)
    cmds.polyMergeUV(currentUV,d=0.001,cch=0)   # fix split
    cmds.select(baseObj,r=1)
if __name__ == "__main__":
    runMorph2UV()