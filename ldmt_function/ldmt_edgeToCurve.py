import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

def edgeToCurve():
    edgeSel = cmds.ls(sl=1,fl=1)
    objSel = edgeSel[0].split('.')[0]
    edgeSelId = []
    for edge in edgeSel:
        edgeSelId.append(int(edge.split('[')[1][:-1]))
        
    objSelList = om2.MSelectionList()
    objSelList.add(objSel)
    objSelPath = objSelList.getDagPath(0)
    objSelEdgeIter = om2.MItMeshEdge(objSelPath)

    edgeToVtx = {}
    vtxToEdge = {}
    vtxIndexAll = []
    while not objSelEdgeIter.isDone():
        edgeIndex = objSelEdgeIter.index()
        vtxIndex = [objSelEdgeIter.vertexId(0),objSelEdgeIter.vertexId(1)]
        if edgeIndex in edgeSelId:
            edgeToVtx[edgeIndex] = vtxIndex
            vtxIndexAll += vtxIndex
        objSelEdgeIter.next()

    #reverse dic to vtxToEdge
    for edge in edgeToVtx:
        vtxes = edgeToVtx[edge]
        for vtx in vtxes:
            if vtx in vtxToEdge:
                vtxToEdge[vtx].append(edge)
            else:
                vtxToEdge[vtx] = [edge]

    #get endpoint vtx
    rootVtx = []
    for vtx in vtxIndexAll:
        if vtxIndexAll.count(vtx)==1:
            rootVtx.append(vtx)
    skipVtx = []
    lineToEdges = {}
    for vtx in rootVtx:
        if not vtx in skipVtx:
            lineToEdges[vtx]=[]
            progressVtx = vtx
            vtxRoot = -1
            lastEdge = -1
            while not vtxRoot in rootVtx:
                edges = vtxToEdge[progressVtx]
                if lastEdge==-1:
                    edge = edges[0]
                    lineToEdges[vtx].append(edge)
                    lastEdge = edge
                else:
                    if lastEdge in edges:
                        if lastEdge == edges[0]:    
                            edge = edges[1]
                        else:
                            edge = edges[0]
                    lineToEdges[vtx].append(edge)
                    lastEdge = edge
                newVtxes = edgeToVtx[edge]
                newVtxes.remove(progressVtx)
                
                if len(vtxToEdge[newVtxes[0]])>1:
                    progressVtx = newVtxes[0]
                else:
                    vtxRoot = newVtxes[0]
                    skipVtx.append(newVtxes[0])

    lineEdges = []
    for line in lineToEdges:
        lineEdges+=lineToEdges[line]


    if not len(lineEdges) == len(edgeSelId):
        circleEdges = []
        circleVtx = set()
        for edge in edgeSelId:
            if not edge in lineEdges:
                circleEdges += [edge]
                circleVtx.add(edgeToVtx[edge][0])
                circleVtx.add(edgeToVtx[edge][1])
        
        ifFirst = 1
        currentEdge = -1
        currentVtx = -1
        vtxSkip = []
        circleToEdges = {}
        for vtx in circleVtx:
            if vtx in vtxSkip:
                continue
            circleToEdges[vtx] = []
            currentEdge = vtxToEdge[vtx][1]
            currentPoints = edgeToVtx[currentEdge]
            if currentPoints[0] == vtx:
                currentPoint = currentPoints[1]
            else:
                currentPoint = currentPoints[0]
            vtxSkip.append(currentPoint)
            circleToEdges[vtx].append(currentEdge)
            
            while currentPoint != vtx:
                currentEdges = vtxToEdge[currentPoint]
                if currentEdges[0] == currentEdge:
                    currentEdge = currentEdges[1]
                else:
                    currentEdge = currentEdges[0]
                currentPoints = edgeToVtx[currentEdge]
                if currentPoints[0] == currentPoint:
                    currentPoint = currentPoints[1]
                else:
                    currentPoint = currentPoints[0]
                circleToEdges[vtx].append(currentEdge)
                vtxSkip.append(currentPoint)
                
        for circle in circleToEdges:
            edgeNames = []
            for edge in circleToEdges[circle]:
                edgeNames.append(objSel+'.e['+str(edge)+']')
            cmds.select(edgeNames,r=1)
            cmds.CreateCurveFromPoly()
    #perform
    for line in lineToEdges:
        edgeNames = []
        for edge in lineToEdges[line]:
            edgeNames.append(objSel+'.e['+str(edge)+']')
        cmds.select(edgeNames,r=1)
        cmds.CreateCurveFromPoly()
    
