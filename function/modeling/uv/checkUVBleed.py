'''
Auther: Liu Dian 
Email: xgits@outlook.com
Website: www.xgits.com
License: MIT
'''
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import math

def selectUVBorder():
    try:
        finalborder = []
        sel = cmds.ls(sl=1,o=1)
        sel = sel[0]+".map[*]"
        cmds.select(sel)
        mel.eval("polySelectBorderShell 1;")
        uvborder = cmds.ls(sl=1)
        uvborder = cmds.polyListComponentConversion(uvborder,te=1,internal=1)
        uvborder = cmds.ls(uvborder,fl=1)
        for border in uvborder:
            borderuv = cmds.polyListComponentConversion(border,tuv=1)
            borderuv = cmds.ls(borderuv,fl=1)
            if len(borderuv) > 2:
                finalborder.append(border)
        return finalborder
    except:
        print("TIP: There is no selection, select something first!")
    
def morphToUV(baseobj):
    cmds.select(baseobj,r=1)
    uvborder = selectUVBorder()
    bordervertices = cmds.polyListComponentConversion(uvborder,tv=1)
    cmds.polySplitVertex(bordervertices)

    baseobj = cmds.ls(sl=1,o=1)
    basevertices = cmds.polyListComponentConversion(baseobj,tv=1)
    basevertices = cmds.ls(basevertices,fl=1)
    for i in basevertices:
        baseuv = cmds.polyListComponentConversion(i,tuv=1)
        uvpos = cmds.polyEditUV(baseuv,q=1)
        cmds.xform(i, t=(uvpos[0], uvpos[1],0 ),ws=1 )

def returnShortDistancePos(pixelDistance=50,uvScale=2048):
    uvDistance = float(pixelDistance)/uvScale

    baseobj = cmds.ls(sl=1,o=1)   #1. inputmesh
    baseobj = cmds.duplicate() #2. duplicate
    baseobj = baseobj[0]
    morphToUV(baseobj) #3.disassemble

    vertexes = cmds.polyListComponentConversion(baseobj,tv=1)
    uvs = cmds.polyListComponentConversion(baseobj,tuv=1)
    cmds.polyMergeVertex(vertexes,d=0.0001)
    cmds.polyMergeUV(uvs,d=0.001)   # fix split

    cmds.polySoftEdge(baseobj,a=180,ch=1) #4-5.dictionary
    selectHardEdges() #select

    borderEdges = cmds.ls(sl=1)
    baseobj= cmds.ls(sl=1,o=1)
    vertspos = vertexPosFromSel()  #### get vertspos in advance
    borderVerts = cmds.polyListComponentConversion(borderEdges,fe=1,tv=1) 
    borderVerts = cmds.ls(borderVerts,fl=1)

    borderUVs = cmds.polyListComponentConversion(borderEdges,fe=1,tuv=1) 
    uvShellId = list(set(cmds.polyEvaluate(borderUVs,usi=1)))
    u2vList = {}   # uvshell : borderVertex
    u2bList = {}   # uvshell : boundingbox 2d

    for i in uvShellId:
        uvShellId_i = uvShellId[i]
        uvFromShell = cmds.polyEvaluate(baseobj,uis=uvShellId_i)
        vertFromShell = cmds.polyListComponentConversion(uvFromShell,fuv=1,tv=1)
        vertFromShell = cmds.ls(vertFromShell,fl=1)
        shellB2 = cmds.polyEvaluate(uvFromShell,bc2=True)
        u2vList[i]= list(set(vertFromShell).intersection(set(borderVerts))) # uvshell : borderVertex
        u2bList[i]= shellB2   # uvshell : boundingbox 2d

    separatedOperation = cmds.polySeparate(baseobj)
    separatedObj = separatedOperation[:-1]
    separatedObj_ShellId = {}  # separatedObj : shellid

    for eachObj in separatedObj:
        eachObjUV = cmds.polyListComponentConversion(eachObj,tuv=1) 
        eachObjB2 = cmds.polyEvaluate(eachObjUV,bc2=True)
        for i in u2bList:
            if eachObjB2 == u2bList[i]:
                separatedObj_ShellId[eachObj] = i
                break
                
    CPOM = cmds.createNode('closestPointOnMesh',n="CPOM#")
    CPOM_inMesh = CPOM + ".inMesh"
    CPOM_inPosition = CPOM+".inPosition"
    CPOM_inputMatrix = CPOM+".inputMatrix"

    CPOM_outPosition = CPOM+".position"

    vertPosList = []
    for eachObj in separatedObj:
        # get pos
        usi = separatedObj_ShellId[eachObj]
        verts = u2vList[usi]
        for vert in verts:
            vertid = int(vert.split('[')[1][:-1])
            vertpos = vertspos[vertid]

            for eachOtherObj in separatedObj:
                if not eachOtherObj == eachObj:
                    CPOM_obj = eachOtherObj 
                    CPOM_shape = cmds.listRelatives(CPOM_obj,shapes=1)
                    CPOM_shape_worldMesh = CPOM_shape[0] + ".worldMesh[0]"
                    CPOM_shape_worldMatrix = CPOM_shape[0] + ".worldMatrix[0]"
                    cmds.connectAttr(CPOM_shape_worldMesh,CPOM_inMesh,f=1)
                    cmds.connectAttr(CPOM_shape_worldMatrix,CPOM_inputMatrix,f=1)
                    cmds.setAttr(CPOM_inPosition,vertpos[0], vertpos[1], vertpos[2])
                    CPOM_outPos = cmds.getAttr(CPOM_outPosition)
                    CPOM_distance = math.sqrt( ((vertpos[0]- CPOM_outPos[0][0])**2)+((vertpos[1]- CPOM_outPos[0][1])**2))
                    if CPOM_distance < uvDistance:
                        vertPosList.append([round(vertpos[0],4),round(vertpos[1],4)])
    cmds.delete(CPOM)
    cmds.delete(separatedOperation)
    return vertPosList
#For Example
def vertexPosFromSel():
    """
    Using Maya Python API 1.0
    """
    #___________Selection___________
    # 1 # initialize a selectionList holder
    selectionLs = om.MSelectionList()
    # 2 # get the selected object in the viewport and put it in the selection list
    om.MGlobal.getActiveSelectionList(selectionLs)
    # 3 # initialize a dagpath object
    dagPath = om.MDagPath()
    # 4 # populate the dag path object with the first object in the selection list
    selectionLs.getDagPath(0,dagPath)
    #___________Query vertex position ___________
    # initialize a Point array holder
    vertPoints = om.MPointArray()
    # create a Mesh functionset from our dag object
    mfnObject = om.MFnMesh(dagPath)
    # call the function "getPoints" and feed the data into our pointArray
    mfnObject.getPoints(vertPoints)
    return vertPoints
   
def uvtestmain():
    sel = cmds.ls(sl=1,o=1)
    selectUVEdgeBorder()
    originBorders = cmds.ls(sl=1)
    originVerts = cmds.polyListComponentConversion(originBorders,fe=1,tuv=1)
    originVerts = cmds.ls(originVerts,fl=1)
    return originVerts

def checkUVBleed():
    uvResolution = int(cmds.optionMenu("uvSize",q=1,v=1))
    pixDistance = cmds.intField("minPixel",q=1,v=1)
    originObj = cmds.ls(sl=1,o=1)
    originUV = uvtestmain()
    cmds.select(originObj,r=1)
    positions = returnShortDistancePos(pixDistance,uvResolution) #select target mesh first
    UVList_notpass = []
    for i in originUV:
        uvpos = cmds.polyEditUV(i,q=1,u=1,v=1)
        uvpos[0]=round(uvpos[0],4)
        uvpos[1]=round(uvpos[1],4)
        if uvpos in positions:
            UVList_notpass.append(i)
    cmds.select(UVList_notpass)

def selectHardEdges():
    selList = cmds.ls(sl=1)
    if selList!=[]:
        edges = cmds.polyListComponentConversion(selList,te=1)
        cmds.select(edges,r=1)
        cmds.polySelectConstraint(m=2,t=0x8000,sm=1)
        cmds.polySelectConstraint(dis=1)

def selectUVEdgeBorder():
    try:
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
    except:
        print("TIP: There is no selection, select something first!")
        
def checkUVBleed_ui():
    if cmds.window("checkUVBleed",ex=1):
        cmds.deleteUI("checkUVBleed")
    cmds.window("checkUVBleed",sizeable=1,h=100,w=200)
    cmds.frameLayout("checkUV",l="Check UV Bleed",collapsable=0)
    cmds.gridLayout(numberOfColumns = 2, cellHeight = 22, cellWidth=100)
    cmds.text(al="center",l="Minimum Pixel")
    cmds.intField("minPixel",v=1000,min=1,max=1024)
    cmds.text(al="center",l="UV size")
    cmds.optionMenu("uvSize",ann="Choose format to output.",changeCommand="print #1")
    cmds.menuItem(l=512)
    cmds.menuItem(l=1024)
    cmds.menuItem(l=2048)
    cmds.menuItem(l=4196)
    cmds.setParent('..')
    cmds.button(l="Check", c= 'checkUVBleed()') 
    cmds.setParent('..')
    cmds.showWindow()