"""
    Snippet testing Vertex Tangent Space in Maya (Python API)
    
    @author: Roy Nieterau
    @website: www.colorbleed.nl
    @email: roy@colorbleed.nl
    
    ==================================
        Averaging the Face Tangents
    ==================================
    Currently I am getting the vertex-tangents by averaging
    the vertex-face-tangents per vertex.
    
    Note:
        That this is not a good solution working with L-shapes:
            - i.e. the 90 degree corners of a Cube
   
    Note2:      
        Without the normalization the pinching on a sphere (top/bottom) can
        result in a matrix with 0, 0, 0 scale because the normals of the
        different faces summed up together will become zero (thus zero average) 

    Edited by Liu Dian, added to specified vertex and random spread.
"""
import maya.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel
import random

def getPosNormalTangents(mesh, normalize=True):
    """ Prototype/Snippet to get vertex tangents from a mesh """
    selList = om.MSelectionList()
    selList.add(mesh)
    path = om.MDagPath()
    selList.getDagPath(0, path)
    path.extendToShape()
    fnMesh = om.MFnMesh(path)
    tangents = om.MFloatVectorArray()
    binormals = om.MFloatVectorArray()
    
    fnMesh.getTangents(tangents)
    fnMesh.getBinormals(binormals)
    itMeshVertex = om.MItMeshVertex(path)
    
    vertBinormals = om.MFloatVectorArray()
    vertBinormals.setLength(fnMesh.numVertices())
    
    vertTangents = om.MFloatVectorArray()
    vertTangents.setLength(fnMesh.numVertices())
    
    vertNormals = om.MFloatVectorArray()
    vertNormals.setLength(fnMesh.numVertices())
    
    vertId = 0
    connectedFaceIds = om.MIntArray()
    
    # For each vertex get the connected faces
    # For each of those faces get the 'tangentId' to get the tangent and binormal stored above
    # Use that to calculate the normal
    while(not itMeshVertex.isDone()):
        
        itMeshVertex.getConnectedFaces(connectedFaceIds)
        tangent = om.MFloatVector()
        binormal = om.MFloatVector()
        for x in xrange(connectedFaceIds.length()):
            faceId = connectedFaceIds[x]
            tangentId = fnMesh.getTangentId(faceId, vertId)
            binormal += binormals[tangentId]
            tangent += tangents[tangentId]
            
        binormal /= connectedFaceIds.length()
        tangent /= connectedFaceIds.length()
        
        if normalize:
            binormal.normalize()
            tangent.normalize()
        
        normal = tangent ^ binormal
        if normalize:
            normal.normalize()
        
        # Put the data in the vertArrays
        vertTangents.set(tangent, vertId)
        vertBinormals.set(binormal, vertId)
        vertNormals.set(normal, vertId)
          
        vertId += 1
        itMeshVertex.next()
        
    vertPoints = om.MPointArray()
    fnMesh.getPoints(vertPoints)
        
    return vertBinormals, vertTangents, vertNormals, vertPoints


def vectorsToMatrix(binormal=(1, 0, 0), tangent=(0, 1, 0), normal=(0, 0, 1), pos=(0, 0, 0), asApi=False):
    """ Function to convert an orthogonal basis defined from seperate vectors + position to a matrix """
    def _parseAPI(vec):
        if isinstance(vec, (om.MVector, om.MFloatVector, om.MPoint, om.MFloatPoint)):
            vec = [vec(x) for x in xrange(3)]
        return vec
    
    binormal = _parseAPI(binormal)    
    tangent = _parseAPI(tangent)    
    normal = _parseAPI(normal)    
    pos = _parseAPI(pos)
    
    if asApi:
        matrix = om.MMatrix()
        for x in xrange(3):
            om.MScriptUtil.setDoubleArray(matrix[0], x, binormal[x])
            om.MScriptUtil.setDoubleArray(matrix[1], x, tangent[x])
            om.MScriptUtil.setDoubleArray(matrix[2], x, normal[x])
            om.MScriptUtil.setDoubleArray(matrix[3], x, pos[x])
        return matrix

    else:
        return [binormal[0], binormal[1], binormal[2], 0,
                tangent[0],  tangent[1],  tangent[2],  0,
                normal[0],   normal[1],   normal[2],   0,
                pos[0],      pos[1],      pos[2],      1]


#
# Test it on two objects (select two objects)
# 1. Used for calculating the tangent spaces
# 2. Duplicated to every vertex with the matrix of the tangent space
#
def copy2VertexPy():
    sel = cmds.ls(os=1,fl=1)
    points = cmds.filterExpand(sel,selectionMask=31,expand=1)

    if not len(sel) > 1:
        raise RuntimeError("Select at least one object and one vertex in order, if multiple objects, it will randomly spread.")
    
    selectedObjs = cmds.ls(sl=1,o=1,fl=1) 
    sizeOfTobeInstanced = len(selectedObjs)-1

    for objIndex in range(sizeOfTobeInstanced):
        eachObj = selectedObjs[objIndex]
        cmds.select(eachObj,r=1)
        pivotWSPos = cmds.xform(ws=1,q=1,piv=1)
        cmds.move(0,0,0,eachObj,rpr=1)
        mel.eval("FreezeTransformations")
        cmds.move(pivotWSPos[0],pivotWSPos[1],pivotWSPos[2],eachObj,rpr=1)
    
    vertBinormals, vertTangents, vertNormals, vertPoints = getPosNormalTangents(selectedObjs[-1])

    for i in points:
        vertid = int(str(i).split('[')[1][:-1])
        objToInstance = random.randrange(0,sizeOfTobeInstanced)
        
        newInstance = cmds.instance(selectedObjs[objToInstance]);

        mat = vectorsToMatrix(vertBinormals[vertid], vertTangents[vertid], vertNormals[vertid], vertPoints[vertid])
        cmds.xform(newInstance, m=mat)
