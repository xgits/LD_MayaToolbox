'''
Auther: Liu Dian 
Email: xgits@outlook.com
Website: www.xgits.com
License: MIT
'''

import maya.cmds as cmds
import maya.api.OpenMaya as om2
def selectUVEdgeBorders():
    sel = cmds.ls(sl=1,o=1)
    sel = sel[0]
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    selVtxIter = om2.MItMeshVertex(selPath)
    selEdgeIter = om2.MItMeshEdge(selPath)
    selFaceIter = om2.MItMeshPolygon(selPath)

    vtxid_uvid = {}
    edgeid_vtxid = {}
    edgeid_uvid = {}   #edgeid_vtxid + vtxid_uvid

    faceid_edgeid = {}
    edgeid_faceid = {} #faceid_edgeid reverse

    faceid_uviduv = {}

    while not selVtxIter.isDone():   #get {vertid:[uvid1,uvid2],}
        vertid = selVtxIter.index()
        vtxid_uvid[vertid] = selVtxIter.getUVIndices()
        selVtxIter.next()

    for vtxid in vtxid_uvid:  # delete rundant
        vtxid_uvid[vtxid] = list(set(vtxid_uvid[vtxid]))

    while not selEdgeIter.isDone():
        edgeid = selEdgeIter.index()
        edgeid_vtxid[edgeid] = [selEdgeIter.vertexId(0),selEdgeIter.vertexId(1)]
        selEdgeIter.next()
        
    while not selFaceIter.isDone():
        faceid = selFaceIter.index()
        verts = selFaceIter.getVertices()
        faceid_edgeid[faceid] = selFaceIter.getEdges()
        uvidanduv=[]
        for index in range(len(verts)):
            uvidanduv.append((selFaceIter.getUVIndexAndValue(index))[0])
        faceid_uviduv[faceid] = uvidanduv
        selFaceIter.next(None)
        
    for faceid in faceid_edgeid:
        for edgeid in faceid_edgeid[faceid]:
            if edgeid in edgeid_faceid:
                edgeid_faceid[edgeid].append(faceid)
            else:
                edgeid_faceid[edgeid] = [faceid]
                
    for edgeid in edgeid_vtxid:
        for vtx in edgeid_vtxid[edgeid]:
            if edgeid in edgeid_uvid:
                edgeid_uvid[edgeid].append(vtxid_uvid[vtx])
            else:
                edgeid_uvid[edgeid] = [vtxid_uvid[vtx]]
                    
    edgeidOnBorder= []
    edgeidOnUVBorder = [] 
    for edgeid in edgeid_faceid:
        faceids = edgeid_faceid[edgeid]
        numface = len(faceids)
        if numface == 1:
            edgeidOnBorder.append(edgeid)
            continue
        elif numface ==2:
            uvidsA =  faceid_uviduv[faceids[0]]
            uvidsB =  faceid_uviduv[faceids[1]]
            intersectUV = list(set(uvidsA).intersection(uvidsB))
            if len(intersectUV)<2:
                edgeidOnUVBorder.append(edgeid)
        else:
            print("Cleanup mesh first!!!!")
            
    edgeName = []
    for edgeid in edgeidOnUVBorder+edgeidOnBorder:
        edgeName.append(sel+'.e['+str(edgeid)+']')
    cmds.select(edgeName,r=1)