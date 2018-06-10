'''
Auther: Liu Dian 
Email: xgits@outlook.com
Website: www.xgits.com
License: MIT
'''
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import math
def checkUVBleed_ui():
    if cmds.window("checkUVBleed",ex=1):
        cmds.deleteUI("checkUVBleed")
    cmds.window("checkUVBleed",sizeable=1,h=100,w=200)
    cmds.frameLayout("checkUV",l="Check UV Bleed",collapsable=0)
    cmds.gridLayout(numberOfColumns = 2, cellHeight = 22, cellWidth=100)
    cmds.text(al="center",l="Min Shell Pixel")
    cmds.intField("minShell",v=32,min=1)
    cmds.text(al="center",l="Min Border Pixel")
    cmds.intField("minBorder",v=16,min=1)
    cmds.text(al="center",l="UV size")
    cmds.optionMenu("uvSize",ann="Set texture size.",changeCommand="print #1")
    cmds.menuItem(l=4096)
    cmds.menuItem(l=2048)
    cmds.menuItem(l=1024)
    cmds.menuItem(l=512)
    cmds.radioCollection()
    cmds.text(al="center",l="Has Overlap UV?")
    cmds.optionMenu("overlapUV",ann="If this model have overlaping UVs. Will be slower.",changeCommand="print #1")
    cmds.menuItem(l="No")
    cmds.menuItem(l="Yes")
    cmds.setParent('..')
    cmds.button(l="Check", c= 'checkUVBleed()') 
    cmds.setParent('..')
    cmds.showWindow()
    
def checkUVBleed():
    uvResolution = int(cmds.optionMenu("uvSize",q=1,v=1))
    pixDistance = cmds.intField("minShell",q=1,v=1)
    borderDistance = cmds.intField("minBorder",q=1,v=1)
    sel = cmds.ls(sl=1,o=1)
    sel = sel[0]
    selDup = prepare_morphToUV(sel)
    positions = returnShortDistancePos(selDup,pixDistance,borderDistance,uvResolution) #select target mesh first
    if positions==0:
        return "Just One Shell!"
    UVNotPass = selectUVNotPass(sel,positions)
    cmds.delete(selDup)
    cmds.select(UVNotPass,r=1)
            
def prepare_morphToUV(sel):  #1. inputmesh
    selDup = cmds.duplicate(sel) #2. duplicate
    selDup = selDup[0]
    hasOverlapUV = cmds.optionMenu("overlapUV",q=1,v=1)
    if hasOverlapUV == "Yes":
        moveOutStackUV(selDup,"delete")
    morph2UV(selDup)
    if hasOverlapUV == "Yes":
        moveOutOverlapUV(selDup,"delete")
    return selDup
       
def moveOutStackUV(sel,ifDelete="move"):
    uvDic = getUVDic(sel)
    usi_uvname     = uvDic[2]      
    usi_bb         = uvDic[11]
    usiSkipList    = []
    usiMoveOutList = []
    uvMoveOutList  = []
    for usiA in usi_bb:
        if not usiA in usiSkipList:
            usiSkipList.append(usiA)
            usiA_Umin = usi_bb[usiA][0][0]
            usiA_Umax = usi_bb[usiA][0][1]
            usiA_Vmin = usi_bb[usiA][1][0]
            usiA_Vmax = usi_bb[usiA][1][1]
            for usiB in usi_bb:
                if not usiB in usiSkipList:
                    usiB_Umin = usi_bb[usiB][0][0]
                    usiB_Umax = usi_bb[usiB][0][1]
                    usiB_Vmin = usi_bb[usiB][1][0]
                    usiB_Vmax = usi_bb[usiB][1][1]
                    Umin_diff = abs(usiB_Umin-usiA_Umin)
                    Umax_diff = abs(usiB_Umax-usiA_Umax)
                    Vmin_diff = abs(usiB_Vmin-usiA_Vmin)
                    Vmax_diff = abs(usiB_Vmax-usiA_Vmax)
                    if(Umin_diff<0.0001 and Umax_diff<0.0001 and Vmin_diff<0.0001 and Vmax_diff<0.0001):
                        usiMoveOutList.append(usiB)
                        usiSkipList.append(usiB)
    for usi in usiMoveOutList:
        uvMoveOutList += usi_uvname[usi]
    if ifDelete == "delete" and uvMoveOutList:
        toDelete= cmds.polyListComponentConversion(uvMoveOutList,fuv=1,tf=1,internal=1)
        cmds.delete(toDelete)
    else:
        cmds.polyEditUV(uvMoveOutList,u=1,r=1)

def morph2UV(sel):
    #delete face with no uv
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
    if faceWithNoUV:
        cmds.delete(faceWithNoUV)
        
    #split if on uv border
    vertIt = om2.MItMeshVertex(selPath)
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
    uvid_usi = selMesh.getUvShellsIds() # [usi1,usi2,...]
    uvid_usi = uvid_usi[1]
    uvArray = selMesh.getUVs()
    for i in xrange(len(uvArray[0])):
        uvid_uv.append([uvArray[0][i],uvArray[1][i]])
        
    while not selVtxIter.isDone():   #get {[[uvid1,uvid2],...]}
        vtxid_uvid.append(list(set(selVtxIter.getUVIndices())))
        selVtxIter.next()
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
    
    #morph to UV
    myMesh = om2.MFnMesh(selPath)
    newPointArray = om2.MPointArray()
    space = om2.MSpace.kWorld
    myMesh_UVs = myMesh.getUVs()
    myMesh_points = myMesh.getPoints()
    myMesh_itVertex = om2.MItMeshVertex(selPath)
    points = om2.MPointArray()
    while not myMesh_itVertex.isDone():
        vertIndex = myMesh_itVertex.index()
        gotUV = myMesh_itVertex.getUV()
        points.append((gotUV[0],gotUV[1],0))
        myMesh_itVertex.next()
    myMesh.setPoints(points,space)
    selUVs  = sel+'.map[*]'
    cmds.polyMergeVertex(sel,d=0.00001,cch=0)
    cmds.polyMergeUV(selUVs,d=0.00001,cch=0)   # fix split
    
def moveOutOverlapUV(sel,ifDelete="move"):  # add two method to detect!!!!!!!!!!!!!!!!!!
    uvDic = getUVDic(sel)
    usi_uvname =        uvDic[2]
    uvid_uv =           uvDic[3]
    vtxOnBordId_uvid =  uvDic[4]
    edgeOnBordId_uvid = uvDic[6]
    edgeOnBordId_uv =   uvDic[7]
    usi_edgeOnBordId =  uvDic[9]
    usi_vtxOnBordId =   uvDic[10]
    usi_bb =            uvDic[11]
    usi_bbarea = {}
    bbarea_usi_zip = []
    usi_overlapUsi = {}
    intersectUVsName =  []
    usiSkipList = []

    for i in range(len(usi_uvname)): #get {usi:area,} from usi_bb
        usi_bbarea[i] = abs(usi_bb[i][0][0]-usi_bb[i][0][1])*abs(usi_bb[i][1][0]-usi_bb[i][1][1])
    bbarea_usi_zip = sorted(zip(usi_bbarea.values(), usi_bbarea.keys())) # get [(minarea, usi0),...,( maxarea, usi99)]
    bbarea_usi_zip.reverse()

    # intersect method
    for area_usiA_tuple in range(len(bbarea_usi_zip)):
        intersects=0
        usiA = bbarea_usi_zip[area_usiA_tuple][1]
        if usiA in usiSkipList:
            continue
        for area_usiB_tuple in range(len(bbarea_usi_zip)):
            usiB = bbarea_usi_zip[area_usiB_tuple][1]
            if usiB != usiA and not (usiB in usiSkipList):
                if (usi_bb[usiB][0][0]>usi_bb[usiA][0][1] or\
                    usi_bb[usiA][0][0]>usi_bb[usiB][0][1] or\
                    usi_bb[usiB][1][0]>usi_bb[usiA][1][1] or\
                    usi_bb[usiA][1][0]>usi_bb[usiB][1][1]):
                    continue
                else:
                    for edgeA in usi_edgeOnBordId[usiA]:
                        ax = edgeOnBordId_uv[edgeA][0][0]
                        ay = edgeOnBordId_uv[edgeA][0][1]
                        bx = edgeOnBordId_uv[edgeA][1][0]
                        by = edgeOnBordId_uv[edgeA][1][1]
                        
                        if bx>ax:
                            edgeA_bb = [[ax,bx],[ay,by]]
                        else:
                            edgeA_bb = [[bx,ax],[ay,by]]
                          
                        for edgeB in usi_edgeOnBordId[usiB]:
                            if intersects == 1:
                                intersects = 0
                                break
                            elif usiB in usiSkipList:
                                break
                            cx = edgeOnBordId_uv[edgeB][0][0]
                            cy = edgeOnBordId_uv[edgeB][0][1]
                            dx = edgeOnBordId_uv[edgeB][1][0]
                            dy = edgeOnBordId_uv[edgeB][1][1]   
                            if dx > cx:
                                edgeB_bb = [[cx,dx],[cy,dy]]
                            else:
                                edgeB_bb = [[dx,cx],[cy,dy]]
                            # now let's see if they intersect!
                            if edgeA_bb[0][0]>edgeB_bb[0][1] or\
                               edgeB_bb[0][0]>edgeA_bb[0][1] or\
                               edgeA_bb[1][0]>edgeB_bb[1][1] or\
                               edgeB_bb[1][0]>edgeA_bb[1][1]:
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
                                intersects = 1
                                if usiA not in usi_overlapUsi:
                                    usi_overlapUsi[usiA] = [usiB]
                                else:
                                    usi_overlapUsi[usiA].append(usiB)
                                usiSkipList.append(usiA)
                                usiSkipList.append(usiB)
                    
                    #ray method
                    for vtxid in usi_vtxOnBordId[usiA]:
                        if usiB in usiSkipList:
                            break
                        intersects = 0
                        uvid = vtxOnBordId_uvid[vtxid]
                        ray_u = uvid_uv[uvid][0]
                        ray_v = uvid_uv[uvid][1]
                        for edge in usi_edgeOnBordId[usiB]:
                            u0 = edgeOnBordId_uv[edge][0][0]
                            u1 = edgeOnBordId_uv[edge][1][0]
                            v0 = edgeOnBordId_uv[edge][0][1]
                            v1 = edgeOnBordId_uv[edge][1][1]
                            if (v1 >= ray_v and v0 < ray_v):
                                if ((u0-ray_u)*(v1-ray_v)-(v0-ray_v)*(u1-ray_u)) < 0:
                                    intersects += 1
                        if intersects%2 == 1:
                            if usiB in usi_overlapUsi:
                                usi_overlapUsi[usiB].append(usiA)
                            else:
                                usi_overlapUsi[usiB] = [usiA]
                            usiSkipList.append(usiA)
                            usiSkipList.append(usiB)
                            continue

    for usiA in usi_overlapUsi:
        for usiB in usi_overlapUsi[usiA]:
            intersectUVsName += usi_uvname[usiB]
        
    if ifDelete=="delete" and intersectUVsName:
        intersectFaces = cmds.polyListComponentConversion(intersectUVsName,fuv=1,tf=1)
        cmds.delete(intersectFaces)
    elif ifDelete=="move":
        cmds.polyEditUV(intersectUVsName,u=1,r=1)
    return intersectUVsName
    
def returnShortDistancePos(sel,pixelDistance=16,borderDistance=8,uvScale=2048):
# sel=cmds.ls(sl=1,o=1)
# sel = sel[0]
    # uvDistance = float(25)/512
    # borderDistance =   float(25)/512
    uvDistance = float(pixelDistance)/uvScale
    borderDistance =  float(borderDistance)/uvScale
    TOLERANCE = 5
    p = 10**TOLERANCE
    uvDic = getUVDic(sel)
    uvid_uv =          uvDic[3]
    vtxOnBordId_uvid = uvDic[4]
    edgeOnBordId_uv =  uvDic[7]
    usi_edgeOnBordId = uvDic[9]
    usi_vtxOnBordId =  uvDic[10]
    bbList =           uvDic[11]

    uvNotPass = []  # len(uvNotPass)
    vtxSkipList = []
    for usiA in usi_vtxOnBordId:
        if bbList[usiA][0][0] - borderDistance < 0 or\
           bbList[usiA][0][1] + borderDistance > 1 or\
           bbList[usiA][1][0] - borderDistance < 0 or\
           bbList[usiA][1][1] + borderDistance > 1:
            for vtx in usi_vtxOnBordId[usiA]:
                vtx_uvid = vtxOnBordId_uvid[vtx]  
                x = uvid_uv[vtx_uvid][0]
                y = uvid_uv[vtx_uvid][1]
                if  x - borderDistance < 0 or\
                    x + borderDistance > 1 or\
                    y - borderDistance < 0 or\
                    y + borderDistance > 1:
                    uvNotPass.append([float(int(x*p))/p,float(int(y*p))/p])
                    vtxSkipList.append(vtx)

        for usiB in usi_edgeOnBordId:
            if usiB == usiA or\
            bbList[usiA][0][0] - uvDistance > bbList[usiB][0][1] or\
            bbList[usiA][0][1] + uvDistance < bbList[usiB][0][0] or\
            bbList[usiA][1][0] - uvDistance > bbList[usiB][1][1] or\
            bbList[usiA][1][1] + uvDistance < bbList[usiB][1][0]:
                continue
            for vtx in usi_vtxOnBordId[usiA]:
                if vtx in vtxSkipList:
                    continue
                    
                vtx_uvid = vtxOnBordId_uvid[vtx]  
                x = uvid_uv[vtx_uvid][0]
                y = uvid_uv[vtx_uvid][1]
                
                if x - uvDistance > bbList[usiB][0][1] or\
                x + uvDistance < bbList[usiB][0][0] or\
                y - uvDistance > bbList[usiB][1][1] or\
                y + uvDistance < bbList[usiB][1][0]:
                    continue
                for edge in usi_edgeOnBordId[usiB]:
                    x1 = edgeOnBordId_uv[edge][0][0]
                    y1 = edgeOnBordId_uv[edge][0][1]                    
                    x2 = edgeOnBordId_uv[edge][1][0]
                    y2 = edgeOnBordId_uv[edge][1][1]
                    cross = (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1)
                    toAppend = [float(int(x*p))/p,float(int(y*p))/p] 
                    if cross <= 0:
                        closest = math.sqrt((x - x1)**2 + (y - y1)**2)
                        if closest < uvDistance:
                            uvNotPass.append(toAppend)
                        continue
                    d2 = (x2 - x1)**2 + (y2 - y1)**2
                    if cross >= d2:
                        closest = math.sqrt((x - x2)**2 + (y - y2)**2)
                        if closest < uvDistance:
                            uvNotPass.append(toAppend)
                        continue
                    r = cross / d2
                    px = x1 + (x2 - x1) * r
                    py = y1 + (y2 - y1) * r
                    closest = math.sqrt((x - px)**2 + (py - y)**2)
                    if closest < uvDistance:
                            uvNotPass.append(toAppend)
    return uvNotPass

def selectUVNotPass(sel,positions):  #### FINAL STAGE
    TOLERANCE = 5
    p = 10**TOLERANCE
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    selMesh = om2.MFnMesh(selPath)
    uvArray = selMesh.getUVs() #get uvid_uv
    uvid_uv = {} # get {uvid:[u,v],}
    for i in range(len(uvArray[0])):
        uvid_uv[i] = [uvArray[0][i],uvArray[1][i]]
    uvidNotPass = []
    for i in uvid_uv:
        uvpos = uvid_uv[i]
        u= float(int(uvpos[0] * p))/p  #rounding faster than round()
        v= float(int(uvpos[1] * p))/p
        for uvpo_pos in positions:
            if u > uvpo_pos[0]-0.001 and v > uvpo_pos[1]-0.001 and u < uvpo_pos[0]+0.001 and v < uvpo_pos[1]+0.001:
                uvidNotPass.append(i)
    uvNameNotPass = []
    if uvidNotPass:
        for uv in uvidNotPass:
            uvNameNotPass.append(sel+'.map['+str(uv)+']')
    return uvNameNotPass
####### MY EVALUATE FUNCTION #########
def getUVDic(sel):
    # UVDics are connected, keep the codes in order, shit codes
    selList = om2.MSelectionList()
    selList.add(sel)
    selPath = selList.getDagPath(0)
    selMesh = om2.MFnMesh(selPath)
    uvArray = selMesh.getUVs()

    uvid_usi = selMesh.getUvShellsIds() # [usi1,usi2,...]
    uvid_usi = uvid_usi[1]
    usi_uvids = {}  # generate {usi:uvid,} from [usi]
    usi_uvname = {} # generate {usi:uvname,} from [usi]
    uvid_uv = {}  # generate {uvid:[u,v],} from MFnMesh.getUVs()

    for uvid in range(len(uvid_usi)):
        usi = uvid_usi[uvid]
        if usi in usi_uvids:
            usi_uvids[usi].append(uvid)
            usi_uvname[usi].append(sel+'.map['+str(uvid)+']')
        else:
            usi_uvids[usi] = [uvid]
            usi_uvname[usi] = [sel+'.map['+str(uvid)+']']
            
    
    for i in range(len(uvArray[0])):
        uvid_uv[i] = [uvArray[0][i],uvArray[1][i]]

    vtxOnBordId_uvid = {} # generate {vtxid:uvid} for edgeOnBordId_uv list
    uvid_vtxOnBordId = {}
    vtxIter = om2.MItMeshVertex(selPath)
    while not vtxIter.isDone():
        if vtxIter.onBoundary():
            vtxid = vtxIter.index()
            uvid = vtxIter.getUVIndices()[0]
            vtxOnBordId_uvid[vtxid] = uvid
            uvid_vtxOnBordId[uvid] = vtxid
        vtxIter.next()
        
    edgeOnBordId_uvid = {}  # generate {edge:[[u0,v0],[u1,v1]],}
    edgeOnBordId_vtx = {}  # generate {edge:[vtxA,vtxB],}
    edgeOnBordId_uv = {} # genreate {edge:[[u0,v0],[u1,v1]],}
    edgeIter = om2.MItMeshEdge(selPath)
    while not edgeIter.isDone():
        if edgeIter.onBoundary():
            edgeid = edgeIter.index()
            vertA = edgeIter.vertexId(0)
            vertB = edgeIter.vertexId(1)
            vertA_uvid = vtxOnBordId_uvid[vertA]
            vertB_uvid = vtxOnBordId_uvid[vertB]
            vertA_u = uvid_uv[vertA_uvid][0]
            vertA_v = uvid_uv[vertA_uvid][1]
            vertB_u = uvid_uv[vertB_uvid][0]
            vertB_v = uvid_uv[vertB_uvid][1]
            edgeOnBordId_uvid[edgeid] = [vertA_uvid,vertB_uvid]
            edgeOnBordId_vtx[edgeid] = [vertA,vertB]
            if vertA_v <= vertB_v:
                edgeOnBordId_uv[edgeid] = [[vertA_u,vertA_v],[vertB_u,vertB_v]]
            else:
                edgeOnBordId_uv[edgeid] = [[vertB_u,vertB_v],[vertA_u,vertA_v]]
        edgeIter.next()

    usi_edgeOnBordId = {} # generate {usi:[edgeOnBordId,],} from edgeOnBordId_uvid and from uvid_usi
    for edge in edgeOnBordId_uvid:
        uvid = edgeOnBordId_uvid[edge][0]
        usi = uvid_usi[uvid]
        if usi in usi_edgeOnBordId:
            usi_edgeOnBordId[usi].append(edge)
        else:
            usi_edgeOnBordId[usi] = [edge]
            
    usi_vtxOnBordId = {} # generate {usi0:[vtx0,vtx1,],usi1:[...]} from usi_edgeOnBordId and edgeOnBordId_uvid
    for usi in usi_edgeOnBordId:
        vtxPerUsi = []
        for edgeid in usi_edgeOnBordId[usi]:
            vtxPerUsi += edgeOnBordId_vtx[edgeid]
        usi_vtxOnBordId[usi] = list(set(vtxPerUsi))
        
    usi_bb = {} # generate {usi:[[Umin,Umax],[Vmin,Vmax]],} from usi_uvids,uvid_uv
    for usi in usi_uvids:
        bb_Umin = 1
        bb_Umax = 0
        bb_Vmin = 1
        bb_Vmax = 0
        for uvid in usi_uvids[usi]:
            if uvid_uv[uvid][0] < bb_Umin:
                bb_Umin = uvid_uv[uvid][0]
            if uvid_uv[uvid][0] > bb_Umax:
                bb_Umax = uvid_uv[uvid][0]
            if uvid_uv[uvid][1] < bb_Vmin:
                bb_Vmin = uvid_uv[uvid][1]
            if uvid_uv[uvid][1] > bb_Vmax:
                bb_Vmax = uvid_uv[uvid][1]
        usi_bb[usi] = [[bb_Umin,bb_Umax],[bb_Vmin,bb_Vmax]]

    ### return
    return uvid_usi,\
           usi_uvids,\
           usi_uvname,\
           uvid_uv,\
           vtxOnBordId_uvid,\
           uvid_vtxOnBordId,\
           edgeOnBordId_uvid,\
           edgeOnBordId_uv,\
           edgeOnBordId_vtx,\
           usi_edgeOnBordId,\
           usi_vtxOnBordId,\
           usi_bb
  # return uvid_usi,\         # 0  uvid_usi
  #        usi_uvids,\        # 1  usi_uvids
  #        usi_uvname,\       # 2  usi_uvname
  #        uvid_uv,\          # 3  uvid_uv
  #        vtxOnBordId_uvid,\ # 4  vtxOnBordId_uvid
  #        uvid_vtxOnBordId,\ # 5  uvid_vtxOnBordId
  #        edgeOnBordId_uvid,\# 6  edgeOnBordId_uvid
  #        edgeOnBordId_uv,\  # 7  edgeOnBordId_uv
  #        edgeOnBordId_vtx,\ # 8  edgeOnBordId_vtx
  #        usi_edgeOnBordId,\ # 9  usi_edgeOnBordId
  #        usi_vtxOnBordId,\  # 10 usi_vtxOnBordId
  #        usi_bb             # 11 usi_bb

    
# newUVDic =  getUVDic()

# sel = cmds.ls(sl=1,o=1)
# sel = sel[0]
# cmds.select(abc,r=1)