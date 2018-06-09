# About ####################
# Auther:  Liu Dian
# Email:   xgits@outlook.com
# Website: www.xgits.com
# Version: Pro 
# License: GPL
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

def getUVEdgeDic(sel):
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    selMesh = om2.MFnMesh(selPath)
    selVtxIter = om2.MItMeshVertex(selPath)
    selEdgeIter = om2.MItMeshEdge(selPath)
    selFaceIter = om2.MItMeshPolygon(selPath)

    uvid_uv = []  # generate {uvid:[u,v],} from MFnMesh.getUVs()
    vtxid_uvid = []
    edgeid_vtxid = []
    edgeid_uvid = []   #edgeid_vtxid + vtxid_uvid
    faceid_edgeid = []
    faceid_uvid = []
    edgeid_faceid = [] #faceid_edgeid reverse
    uvedgeid_uvid = [] # get { uvedgeid: [uvid1, uvid2]} On border

    uvid_usi = selMesh.getUvShellsIds()
    uvid_usi = uvid_usi[1]
    uvArray = selMesh.getUVs()
    for i in xrange(len(uvArray[0])):
        uvid_uv.append([uvArray[0][i],uvArray[1][i]])
        
    while not selVtxIter.isDone():   #get {[[uvid1,uvid2],...]}
        vtxid_uvid.append(list(set(selVtxIter.getUVIndices())))
        selVtxIter.next()

    while not selEdgeIter.isDone():  #get edge to vtx
        edgeid_vtxid.append([selEdgeIter.vertexId(0),selEdgeIter.vertexId(1)])
        edgeid_faceid.append(selEdgeIter.getConnectedFaces())
        selEdgeIter.next()
        
    for edgeid in xrange(len(edgeid_vtxid)):  # get {[[uvid1,uvid2,uvid3],...]}
        vtx0 = edgeid_vtxid[edgeid][0]
        vtx1 = edgeid_vtxid[edgeid][1]
        edgeid_uvid.append(vtxid_uvid[vtx0] + vtxid_uvid[vtx1])
            
    while not selFaceIter.isDone():  # get {[[uvid1,uvid2,uvid3,uvid4], ...] }
        verts = selFaceIter.getVertices()
        faceid_edgeid.append(selFaceIter.getEdges())
        uvids=[]
        for index in xrange(len(verts)):        
            uvids.append(selFaceIter.getUVIndex(index)) #necessary for uvedgeid
        faceid_uvid.append(uvids)
        selFaceIter.next(None)
                    
    for edgeid in xrange(len(edgeid_faceid)):
        faceids = edgeid_faceid[edgeid]
        edgeuvids = set(edgeid_uvid[edgeid])
        numface = len(faceids)
        if numface == 1:                        #OnBorder
            uvids =  faceid_uvid[faceids[0]]
            uvedgeid_uvid.append(list(edgeuvids.intersection(uvids)))
            continue
        elif numface == 2:
            uvidsA =  faceid_uvid[faceids[0]]
            uvidsB =  faceid_uvid[faceids[1]]
            intersectUV = list(set(uvidsA).intersection(uvidsB))
            intersectUV_len = len(intersectUV)
            if intersectUV_len<2:
                if intersectUV_len == 1:
                    for uv in edgeuvids:
                        if uv == intersectUV[0]:
                            continue
                        elif uv in uvidsA or uv in uvidsB:
                            uvedgeid_uvid.append([intersectUV[0],uv])
                else:
                    uvedgeid_uvid.append(list(edgeuvids.intersection(uvidsA)))
                    uvedgeid_uvid.append(list(edgeuvids.intersection(uvidsB)))
        else:
            print("Cleanup mesh first!!!!")
            
    usi_uvid = {}
    usi_uvidOnBord = {}
    usi_uvedgeidOnBord = {}
    usi_bb = {}

    for uvid in xrange(len(uvid_usi)):
        usi = uvid_usi[uvid]
        if usi in usi_uvid:
            usi_uvid[usi].append(uvid)
        else:
            usi_uvid[usi] = [uvid]

    for uvedgeid in xrange(len(uvedgeid_uvid)):
        usi = uvid_usi[uvedgeid_uvid[uvedgeid][0]]
        if usi in usi_uvedgeidOnBord:
            usi_uvedgeidOnBord[usi].append(uvedgeid)
        else:
            usi_uvedgeidOnBord[usi] = [uvedgeid]

    for usi in usi_uvedgeidOnBord:
        edgeids = usi_uvedgeidOnBord[usi]
        uvsOnBord = []
        for edgeid in edgeids:
            uvsOnBord = uvsOnBord + uvedgeid_uvid[edgeid]
        usi_uvidOnBord[usi] = list(set(uvsOnBord))

    for usi in usi_uvidOnBord:
        umin = 1
        umax = 0
        vmin = 1
        vmax = 0
        for uvid in usi_uvidOnBord[usi]:
            u = uvid_uv[uvid][0]
            v = uvid_uv[uvid][1]
            if u < umin:
                umin = u
            if u > umax:
                umax = u
            if v < vmin:
                vmin = v
            if v > vmax:
                vmax = v
        usi_bb[usi] = [[umin,umax],[vmin,vmax]]

    usi_bbarea = {}
    for i in xrange(len(usi_uvid)): #get {usi:area,} from usi_bb
        usi_bbarea[i] = abs(usi_bb[i][0][1]-usi_bb[i][0][0])*abs(usi_bb[i][1][1]-usi_bb[i][1][0])
    bbarea_usi = sorted(zip(usi_bbarea.values(), usi_bbarea.keys())) # get [(minarea, usi0),...,( maxarea, usi99)]
    bbarea_usi.reverse()

    uvedgeid_uv = []
    for uvedgeid in xrange(len(uvedgeid_uvid)):
        uvidA = uvedgeid_uvid[uvedgeid][0]
        uvidB = uvedgeid_uvid[uvedgeid][1]
        uA = uvid_uv[uvidA][0] 
        vA = uvid_uv[uvidA][1]
        uB = uvid_uv[uvidB][0]
        vB = uvid_uv[uvidB][1]
        if vB >= vA:
            uvedgeid_uv.append([[uA,vA],[uB,vB]])
        else:
            uvedgeid_uv.append([[uB,vB],[uA,vA]])
                
    return usi_uvid, uvid_uv, uvedgeid_uvid, usi_uvidOnBord, usi_uvedgeidOnBord, usi_bb, bbarea_usi, uvedgeid_uv

def getFacesHaveNoUV(sel):
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    selVtxIter= om2.MItMeshVertex(selPath)
    faceidWithNoUV = []
    faceWithNoUV = []
    while not selVtxIter.isDone():
        if selVtxIter.numUVs()==0:
            faceidWithNoUV += selVtxIter.getConnectedFaces()
        selVtxIter.next()
    faceidWithNoUV = list(set(faceidWithNoUV))
    for faceid in faceidWithNoUV:
        faceWithNoUV+=[sel+'.f['+str(faceid)+']']
    return faceWithNoUV
    
def LD_moveOverlapUVOut():
    TOLERANCE = 4
    p = 10**TOLERANCE
    selForSkip = cmds.ls(sl=1)
    sel = cmds.ls(sl=1,o=1)
    if selForSkip != sel:
        selUVidForSkip = cmds.polyListComponentConversion(selForSkip,tuv=1)
        selUVidForSkip = cmds.ls(selUVidForSkip,fl=1)
    else:
        selUVidForSkip = []
    sel = sel[0]
    faceWithNoUV = getFacesHaveNoUV(sel)
    if faceWithNoUV !=[]:
        cmds.select(faceWithNoUV,r=1)
        f_printMessage("Some Faces have no UVs!")
        return
    uvDic = getUVEdgeDic(sel)  #uvDic[6]
    usi_uvid =           uvDic[0]
    uvid_uv =            uvDic[1]
    uvedgeid_uvid =      uvDic[2]
    usi_uvidOnBord =     uvDic[3]
    usi_uvedgeidOnBord = uvDic[4]
    usi_bb =             uvDic[5]
    bbarea_usi =         uvDic[6]
    uvedgeid_uv =        uvDic[7]

    uvNotPass = set()  # len(uvNotPass) Filter out stacking uvs 
    skipList = set() 
    skipListTemp = set()
    intersectList = {}
    usi_uvidOnBord_final = {}
    usi_uvedgeidOnBord_final = {}

    # prepare
    for tupleA in xrange(len(bbarea_usi)):
        usiA = bbarea_usi[tupleA][1]
        skipListTemp.add(usiA)
        
        # fast detect
        bb_uminA = usi_bb[usiA][0][0]
        bb_umaxA = usi_bb[usiA][0][1]
        bb_vminA = usi_bb[usiA][1][0]
        bb_vmaxA = usi_bb[usiA][1][1]  
              
        for tupleB in xrange(len(bbarea_usi)):
            usiB = bbarea_usi[tupleB][1]
            
            #faset detect
            bb_uminB = usi_bb[usiB][0][0]
            bb_umaxB = usi_bb[usiB][0][1]
            bb_vminB = usi_bb[usiB][1][0]
            bb_vmaxB = usi_bb[usiB][1][1]
            if bb_uminA > bb_umaxB or\
               bb_umaxA < bb_uminB or\
               bb_vminA > bb_vmaxB or\
               bb_vmaxA < bb_vminB :
                continue
                
            if usiB in skipListTemp:
                continue
            if ifUVShellStack(usiA,usiB,usi_bb, p):
                skipList.add(usiB)
                skipListTemp.add(usiB)
            elif ifUVShellIntersect(usiA,usiB,usi_uvedgeidOnBord, uvedgeid_uv, usi_bb):
                skipListTemp.add(usiB)
                skipList.add(usiB)
            elif ifUVShellContain(usiA,usiB,usi_uvedgeidOnBord,usi_uvidOnBord,uvedgeid_uv,uvid_uv):
                skipList.add(usiB)
                skipListTemp.add(usiB)
                
    uvidsToMove = []
    uvNamesToMove = set()
    # calculate final list
    for usi in skipList:
        uvidsToMove += usi_uvid[usi]
        
    for uvid in uvidsToMove:
        uvNamesToMove.add(sel+'.map['+str(uvid)+']')
        
    for index in xrange(len(selUVidForSkip)):
        selUVidForSkip[index] = selUVidForSkip[index].split('.')[1]
        
    selToSkip = []
    for uvName in uvNamesToMove:
        uvName = uvName.split('.')[1]
        if uvName in selUVidForSkip:
            selToSkip.append(sel+'.'+uvName)
    for i in selToSkip:
        uvNamesToMove.remove(i)

    uvNamesToMove = list(uvNamesToMove)
    cmds.polyEditUV(uvNamesToMove,u=1)
    
def ifUVShellStack(usiA, usiB, usi_bb, p):
    # fast filter
    usiA_umin = float(int(usi_bb[usiA][0][0] * p))/p
    usiB_umin = float(int(usi_bb[usiB][0][0] * p))/p
    if not usiA_umin == usiB_umin:
        return 0
        
    usiA_umax = float(int(usi_bb[usiA][0][1] * p))/p
    usiA_vmin = float(int(usi_bb[usiA][1][0] * p))/p
    usiA_vmax = float(int(usi_bb[usiA][1][1] * p))/p
    usiB_umax = float(int(usi_bb[usiB][0][1] * p))/p
    usiB_vmin = float(int(usi_bb[usiB][1][0] * p))/p
    usiB_vmax = float(int(usi_bb[usiB][1][1] * p))/p
    if usiA_umax == usiB_umax and usiA_vmin == usiB_vmin and usiA_vmax == usiB_vmax:
        return 1
    return 0

def ifUVShellIntersect(usiA, usiB, usi_uvedgeidOnBord, uvedgeid_uv, usi_bb):
    for edgeA in usi_uvedgeidOnBord[usiA]:
        ax = uvedgeid_uv[edgeA][0][0]
        ay = uvedgeid_uv[edgeA][0][1]
        bx = uvedgeid_uv[edgeA][1][0]
        by = uvedgeid_uv[edgeA][1][1]

        # fast filter
        abx = [ax,bx]
        aby = [ay,by]
        if bx<ax:
            abx = [bx,ax]
        if by<ay:
            aby = [by,ay]

        # bound filter
        bb_usiB = usi_bb[usiB]
        bb_uminB = bb_usiB[0][0]
        bb_umaxB = bb_usiB[0][1]
        bb_vminB = bb_usiB[1][0]
        bb_vmaxB = bb_usiB[1][1]
        
        if  abx[0] > bb_umaxB or\
            abx[1] < bb_uminB or\
            aby[0] > bb_vmaxB or\
            aby[1] < bb_vminB:
            continue
            
        for edgeB in usi_uvedgeidOnBord[usiB]:
            cx = uvedgeid_uv[edgeB][0][0]
            cy = uvedgeid_uv[edgeB][0][1]
            dx = uvedgeid_uv[edgeB][1][0]
            dy = uvedgeid_uv[edgeB][1][1]
            
            # fast filter
            cdx = [cx,dx]
            cdy = [cy,dy]
            if dx<cx:
                cdx = [dx,cx]
            if dy<cy:
                cdy = [dy,cy]
            if abx[0] > cdx[1] or\
               abx[1] < cdx[0] or\
               aby[0] > cdy[1] or\
               aby[1] < cdy[0]:
                continue
            
            x1 = bx - ax
            y1 = by - ay
            x2 = cx - ax
            y2 = cy - ay
            cross1 = x1*y2-x2*y1
            x2 = dx - ax
            y2 = dy - ay
            cross2 = x1*y2-x2*y1
            x1 = dx - cx
            y1 = dy - cy
            x2 = ax - cx
            y2 = ay - cy
            cross3 = x1*y2-x2*y1
            x2 = bx - cx
            y2 = by - cy
            cross4 = x1*y2-x2*y1
            if (cross1*cross2 <= 0 and cross3*cross4<=0):
                return 1
    return 0

def ifUVShellContain(usiA,usiB,usi_uvedgeidOnBord,usi_uvidOnBord,uvedgeid_uv,uvid_uv):
    uvid = usi_uvidOnBord[usiB][0]
    intersects = 0
    ray_u = uvid_uv[uvid][0]
    ray_v = uvid_uv[uvid][1]

    for edge in usi_uvedgeidOnBord[usiA]:
        u0 = uvedgeid_uv[edge][0][0]
        v0 = uvedgeid_uv[edge][0][1]
        u1 = uvedgeid_uv[edge][1][0]
        v1 = uvedgeid_uv[edge][1][1]
        if (v1 >= ray_v and v0 < ray_v):
            if ((u0-ray_u)*(v1-ray_v)-(v0-ray_v)*(u1-ray_u)) < 0:
                intersects += 1
    if intersects%2 == 1:
        return 1
    return 0
    
# checkUVBleed_0()
# cProfile.run('checkUVBleed_0()')