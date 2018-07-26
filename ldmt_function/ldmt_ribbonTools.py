import os
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
import random
import math
try:
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance 
except ImportError:
    from PySide.QtCore import * 
    from PySide.QtGui import * 
    from PySide.QtUiTools import *
    from PySide import __version__
    from shiboken import wrapInstance 
    
from functools import partial

from ldmt_loadUIFile import get_maya_window, load_ui_type
from ldmt_core import ldmt_cmds as ld

LDMTPATH = ld.getPath('LDMT')
LDRibbonToolsUI_file = LDMTPATH + '/ldmt_ui/ldmt_ribbonTools.ui'
LDRibbonToolsUI_list_form, LDRibbonToolsUI_list_base = load_ui_type(LDRibbonToolsUI_file)

ldmt_window_name = 'ldmt_ribbonTools'
ldmt_button_name = 'btn_'+ldmt_window_name.split('_')[1]

'''
#Functions
'''
def LDRibbonTools_getSliderList():
    curveAttrName  = {'flip'           :'flipAxis',\
                      'rotation'       :'rotation',\
                      'widthScale'     :'maxScale',\
                      'lengthScale'    :'lengthScale',\
                      'offset'         :'offset',\
                      'subdivLength'   :'subdivLength',\
                      'subdivWidth'    :'subdivWidth',\
                      'scaleRoot'      :'scaleCurve[0].scaleCurve_Value',\
                      'scaleTip'       :'scaleCurve[3].scaleCurve_Value',\
                      'twistRotation'  :'twistRotation',\
                      'twistStartPos'  :'twistCurve[1].twistCurve_Position',\
                      'twistStartValue':'twistCurve[1].twistCurve_Value'\
                      }

    attrName       = ['flip','rotation','widthScale' ,'lengthScale' ,'offset','subdivLength' ,'subdivWidth' ,'scaleRoot' ,'scaleTip' ,'twistRotation' ,   'twistStartPos'    ,'twistStartValue'  ]
    label          = ['Flip','Rotation','Width Scale','Length Scale','Offset','Subdiv Length','Subdiv Width','Scale Root','Scale Tip','Twist Rotation','Twist Start Position','Twist Start Value']
    minValue       = [  0   ,   -36000 ,    0.001    ,    0.001     ,   0    ,       1       ,       1      ,     0      ,     0     ,  -3600000      ,          0           ,      -100         ]
    softMinValue   = [  0   ,   -360   ,    0.01     ,    0.01      ,   0    ,       1       ,       1      ,     0      ,     0     ,    -3600       ,          0           ,      -100         ]
    maxValue       = [  1   ,    36000 ,    1000     ,     300      ,  100   ,      300      ,       50     ,    100     ,    100    ,   3600000      ,         100          ,       100         ]
    softMaxValue   = [  1   ,    360   ,    100      ,     150      ,  100   ,      100      ,       12     ,    100     ,    100    ,     3600       ,         100          ,       100         ]
    value          = [  0   ,     0    ,     1       ,     150      ,   0    ,       10      ,       3      ,     50     ,     50    ,      0         ,          50          ,        50         ]
    precision      = [  0   ,     0    ,     3       ,      0       ,   0    ,       0       ,       0      ,     0      ,     0     ,      0         ,          0           ,        0          ]
    #create Unique name for ui 
    toolName       = 'ldCurveWarp'
    ldCurveWarpSliderNameList =  []
    for eachAttr in attrName:
        ldCurveWarpSliderNameList.append(toolName + '_'+ eachAttr)
    sliderList = {}
    sliderList['curveAttrName'] = curveAttrName
    sliderList['sliderName']    = ldCurveWarpSliderNameList
    sliderList['attrName']      = attrName
    sliderList['label']         = label
    sliderList['minValue']      = minValue
    sliderList['softMinValue'] = softMinValue
    sliderList['maxValue']      = maxValue
    sliderList['softMaxValue'] = softMaxValue
    sliderList['value']         = value
    sliderList['precision']     = precision
    return sliderList
    
def LDRibbonTools_selectBaseMesh():
    sel = cmds.ls(o=1,os=1)
    if len(sel) == 1:
        currentIndex = cmds.optionMenu('LDRibbonTools_meshOption',q=1,sl=1)
        currentItem = 'LDRibbonTools_mesh'+str(currentIndex-1)
        cmds.menuItem(currentItem, e=1, l=sel[0])
    elif len(sel) > 1:
        for i in range(len(sel)):
            currentIndex = cmds.optionMenu('LDRibbonTools_meshOption',q=1,sl=1)
            currentItem = 'LDRibbonTools_mesh'+str(i+currentIndex-1)
            cmds.menuItem(currentItem, e=1, l=sel[i])

def LDRibbonTools_movePivotToCurve0():
    sel = cmds.ls(sl=1,o=1)
    for i in sel:
        if cmds.nodeType(sel) != 'transform':
            i = cmds.listRelatives(i,p=1)
            i = i[0]
        shapeNode = cmds.listRelatives(i,s=1)
        nodeType = cmds.nodeType(shapeNode)
        if nodeType == 'nurbsCurve':
            curveName = i
            curve0Pos = cmds.pointPosition(curveName+'.cv[0]', w=1)
            cmds.move(curve0Pos[0], curve0Pos[1], curve0Pos[2], i+".scalePivot", i+".rotatePivot", absolute=True)
        else:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            if curveWarpName != None:
                curveName = cmds.listConnections(curveWarpName, t='curveShape')
                curveName = curveName[0]
                curve0Pos = cmds.pointPosition(curveName+'.cv[0]', w=1)
                cmds.move(curve0Pos[0], curve0Pos[1], curve0Pos[2], i+".scalePivot", i+".rotatePivot", absolute=True)
                cmds.move(curve0Pos[0], curve0Pos[1], curve0Pos[2], curveName+".scalePivot", curveName+".rotatePivot", absolute=True)
                
def LDRibbonTools_getMaterial(sel):
    shape = cmds.listRelatives ( sel, shapes=True )
    shadingEngine = cmds.listConnections (shape, source=False, destination=True)
    material = cmds.listConnections (shadingEngine, source=True, destination=False)
    return material[0]
    
def LDRibbonTools_reverseCurve():
    sel = cmds.ls(sl=1,o=1) 
    for i in sel:
        shapeNode = cmds.listRelatives(i,s=1)
        nodeType = cmds.nodeType(shapeNode)
        if nodeType == 'nurbsCurve':
            curveName = i
            cmds.reverseCurve(curveName,ch=1,rpo=1)
        else:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            if curveWarpName != None:
                curveName = cmds.listConnections(curveWarpName, t='curveShape')
                curveName = curveName[0]
                cmds.reverseCurve(curveName,rpo=1)
    cmds.select(sel,r=1)
                
def LDRibbonTools_densifyCV():
    sel = cmds.ls(sl=1,o=1) 
    for i in sel:
        shapeNode = cmds.listRelatives(i,s=1)
        nodeType = cmds.nodeType(shapeNode)
        if nodeType == 'nurbsCurve':
            curveName = i
            spans = cmds.getAttr(curveName+'.spans')
            targetSpans = spans*2
            cmds.rebuildCurve(curveName,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=0,kt=0,s=targetSpans,d=3,tol=0.01)
        else:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            if curveWarpName != None:
                curveName = cmds.listConnections(curveWarpName, t='curveShape')
                curveName = curveName[0]
                spans = cmds.getAttr(curveName+'.spans')
                targetSpans = spans*2
                cmds.rebuildCurve(curveName,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=0,kt=0,s=targetSpans,d=3,tol=0.01)
    cmds.select(sel,r=1)  
    
def LDRibbonTools_smoothCV():
    sel = cmds.ls(sl=1,o=1) 
    for i in sel:
        shapeNode = cmds.listRelatives(i,s=1)
        nodeType = cmds.nodeType(shapeNode)
        if nodeType == 'nurbsCurve':
            curveName = i
            spans = cmds.getAttr(curveName+'.spans')
            targetSpans = spans/2+1
            cmds.rebuildCurve(curveName,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=0,kt=0,s=targetSpans,d=3,tol=0.01)
        else:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            if curveWarpName != None:
                curveName = cmds.listConnections(curveWarpName, t='curveShape')
                curveName = curveName[0]
                spans = cmds.getAttr(curveName+'.spans')
                targetSpans = spans/2+1
                cmds.rebuildCurve(curveName,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=0,kt=0,s=targetSpans,d=3,tol=0.01)
    cmds.select(sel,r=1)

def LDRibbonTools_ribbonCreate():
    sel = ld.ls("curve")
    if sel == None:
        ld.msg("Select Curve Please!")
        return
    bendGroupName = cmds.group(n="bendHandle#",em=1)
    groupName = cmds.group(n="ribbonMeshGroup#",em=1)
    cmds.hide(bendGroupName)
    createdMesh = []
    for i in sel:
        polyCreateName = cmds.polyPlane(sx=3,sy=10)
        polyName = polyCreateName[0]
        cmds.setAttr(polyName+'.rz',-90)
        ld.freeze(polyName)
        bendCreateName = cmds.nonLinear(polyName, type='bend',lowBound=-1,highBound=1,curvature=0)
        bendName = bendCreateName[0] 
        bendHandleName = bendCreateName[1]
        polyPlaneName = polyCreateName[1]
        curveLength = cmds.arclen(i)
        curveWarpName = cmds.createCurveWarp(polyName,i)
        
        # default value for polyPlane
        cmds.setAttr(curveWarpName+'.alignmentMode',4) #align z
        cmds.setAttr(polyPlaneName+'.height',curveLength) #max length
        
        sliderList = LDRibbonTools_getSliderList()
        attrAddList = sliderList['attrName'] 
        minValue = sliderList['minValue']
        maxValue = sliderList['maxValue']
        softMinValue = sliderList['softMinValue']
        softMaxValue = sliderList['softMaxValue']
        precision     = sliderList['precision']
        defaultValue  = sliderList['value']
         
        for index in range(len(sliderList['attrName'])):
            attributeType = 'long' if precision[index] == 0 else 'double'
            cmds.addAttr(polyName,ln = attrAddList[index], min = minValue[index], smn = softMinValue[index], max = maxValue[index], smx = softMaxValue[index], at = attributeType, dv = defaultValue[index], k=1)
        cmds.addAttr(polyName,ln="twistReverse", min=0, max=1,at="long",dv=0,k=1)
        cmds.addAttr(polyName,ln="curvature", min = -180 ,max =180, at="long", dv=0,k=1)
        
        polyTwistReverse = polyName+'.twistReverse' 
        cmds.scriptJob(ro=0, ac=[polyTwistReverse, 'LDRibbonTools_ribbon_updateTwistReverse("'+ polyName +'","' + curveWarpName +'")'])
        LDRibbonTools_scriptJob_twistReverse = 'cmds.scriptJob(ro=0, ac=["'+polyTwistReverse+'", \'LDRibbonTools_ribbon_updateTwistReverse("' + polyName +'","' + curveWarpName +'")\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistReverse , n="ldCurveWarpScriptNode#", stp="python")    
        
        cmds.connectAttr(polyName+'.flip',curveWarpName+'.flipAxis')
        cmds.expression(s = curveWarpName+".maxScale"+'='+polyName+".widthScale*2")
        cmds.expression(s = curveWarpName+".lengthScale"+'='+polyName+".lengthScale/100")
        cmds.expression(s = curveWarpName+".offset"+'='+polyName+".offset/100")
        cmds.connectAttr(polyName+'.rotation',curveWarpName+'.rotation')

        cmds.connectAttr(polyName+'.curvature',bendName+'.curvature')
        
        polyTwistRotation = polyName + '.twistRotation'
        cmds.scriptJob(ro=0, ac=[polyTwistRotation, 'LDRibbonTools_ribbon_updateTwistRotation("'+ polyName +'","' + curveWarpName +'")'])
        LDRibbonTools_scriptJob_twistRotation = 'cmds.scriptJob(ro=0, ac=["'+polyTwistRotation+'", \'LDRibbonTools_ribbon_updateTwistRotation("' + polyName +'","' + curveWarpName +'")\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistRotation , n="ldCurveWarpScriptNode#", stp="python")
        
        cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',0.001)
        cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',0.999)

        polySubdivLength = polyName+'.subdivLength'
        polySubdivWidth = polyName+'.subdivWidth'
        polyPlaneSubdivLength = polyPlaneName+'.subdivisionsHeight'
        polyPlaneSubdivWidth = polyPlaneName+'.subdivisionsWidth'
        cmds.scriptJob(ro=0, ac=[polySubdivLength, 'LDRibbonTools_ribbon_updateSubdiv("'+ polyName +'","' + polyPlaneName +'")'])
        cmds.scriptJob(ro=0, ac=[polySubdivWidth , 'LDRibbonTools_ribbon_updateSubdiv("'+ polyName +'","' + polyPlaneName  +'")'])
        LDRibbonTools_scriptJob_subdivLength = 'cmds.scriptJob(ro=0, ac=["'+polySubdivLength+'", \'LDRibbonTools_ribbon_updateSubdiv("' + polyName +'","' + polyPlaneName +'")\'])'
        LDRibbonTools_scriptJob_subdivWidth  = 'cmds.scriptJob(ro=0, ac=["'+polySubdivWidth+'",  \'LDRibbonTools_ribbon_updateSubdiv("' + polyName +'","' + polyPlaneName + '")\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_subdivLength , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_subdivWidth , n="ldCurveWarpScriptNode#", stp="python")
        
        polyTwistStartPos = polyName + '.twistStartPos'
        polyTwistStartValue = polyName + '.twistStartValue'
        curveTwistStartPos1 = curveWarpName + '.twistCurve[1].twistCurve_Position'
        curveTwistStartPos2 = curveWarpName + '.twistCurve[2].twistCurve_Position'
        curveTwistStartValue1 = curveWarpName + '.twistCurve[1].twistCurve_Value'
        curveTwistStartValue2 = curveWarpName + '.twistCurve[2].twistCurve_Value'
        cmds.scriptJob(ro=0, ac=[polyTwistStartPos , 'LDRibbonTools_setAttr("'+ curveTwistStartPos1 +'","' + polyTwistStartPos  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartPos , 'LDRibbonTools_setAttr("'+ curveTwistStartPos2 +'","' + polyTwistStartPos  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartValue , 'LDRibbonTools_setAttr("'+ curveTwistStartValue1 +'","' + polyTwistStartValue  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartValue , 'LDRibbonTools_setAttr("'+ curveTwistStartValue2 +'","' + polyTwistStartValue  +'",0.01)'])
        LDRibbonTools_scriptJob_twistStartPos1   = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartPos+'", \'LDRibbonTools_setAttr("' + curveTwistStartPos1 +'","'+ polyTwistStartPos +'",0.01)\'])'
        LDRibbonTools_scriptJob_twistStartPos2   = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartPos+'", \'LDRibbonTools_setAttr("' + curveTwistStartPos2 +'","'+ polyTwistStartPos +'",0.01)\'])'
        LDRibbonTools_scriptJob_twistStartValue1 = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartValue+'", \'LDRibbonTools_setAttr("' + curveTwistStartValue1 +'","'+ polyTwistStartValue +'",0.01)\'])'
        LDRibbonTools_scriptJob_twistStartValue2 = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartValue+'", \'LDRibbonTools_setAttr("' + curveTwistStartValue2 +'","'+ polyTwistStartValue +'",0.01)\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistStartPos1 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistStartPos2 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistStartValue1 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistStartValue2 , n="ldCurveWarpScriptNode#", stp="python")
            
        polyScaleRoot = polyName + '.scaleRoot'
        polyScaleTip = polyName + '.scaleTip'
        curveScaleRoot = curveWarpName + '.scaleCurve[0].scaleCurve_Value'
        curveScaleTip = curveWarpName + '.scaleCurve[3].scaleCurve_Value'
        cmds.scriptJob(ro=0, ac=[polyScaleRoot, 'LDRibbonTools_setAttr("'+ curveScaleRoot+'","' + polyScaleRoot +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyScaleTip , 'LDRibbonTools_setAttr("'+ curveScaleTip +'","' + polyScaleTip  +'",0.01)'])
        LDRibbonTools_scriptJob_scaleRoot   = 'cmds.scriptJob(ro=0, ac=["'+polyScaleRoot+'", \'LDRibbonTools_setAttr("' + curveScaleRoot +'","'+ polyScaleRoot +'",0.01)\'])'
        LDRibbonTools_scriptJob_scaleTip    = 'cmds.scriptJob(ro=0, ac=["'+polyScaleTip +'", \'LDRibbonTools_setAttr("' + curveScaleTip +'","'+ polyScaleTip  +'",0.01)\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_scaleRoot , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_scaleTip , n="ldCurveWarpScriptNode#", stp="python")

        LDRibbonTools_movePivotToCurve0()
        cmds.parent(polyName,groupName)
        cmds.parent(bendHandleName,bendGroupName)
        createdMesh.append(polyName)
    cmds.select(createdMesh,r=1)

# get corner uv [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
def LDRibbonTools_getRibbonUV(sel):
    selVtxIter = ld.MItMeshVertex(sel)
    cornerVtx_uv = {}
    while not selVtxIter.isDone():
        index   = selVtxIter.index()
        faceNum = selVtxIter.numConnectedFaces()
        uv      = selVtxIter.getUV()
        if faceNum == 1:
            cornerVtx_uv[index]=uv
        selVtxIter.next()
    if len(cornerVtx_uv) == 4:
        return cornerVtx_uv
    else:
        return None
        
def LDRibbonTools_getRibbonSubdiv(sel):
    mesh = ld.MFnMesh(sel)
    vtxNum = mesh.numVertices

    edgeIter = ld.MItMeshEdge(sel)
    edge0 = mesh.getEdgeVertices(0)
    edge1 = mesh.getEdgeVertices(1)
    biggerIndex = max(max(edge0[0],edge0[1]),max(edge1[0],edge1[1]))

    subdivWidth = biggerIndex - 1
    subdivLength = (vtxNum - subdivWidth)/ biggerIndex
    return [subdivLength,subdivWidth]

def ldCurveWarp_findCurve():
    sel = cmds.ls(sl=1,o=1)
    cmds.select(cl=1)
    curves = cmds.filterExpand(sel,sm=9)
    if curves == None:
        for i in sel:  
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            if curveWarpName != None:
                curveName = cmds.listConnections(curveWarpName, t='curveShape')
                curveName = curveName[0]
            cmds.select(curveName,add=1)
    else:
        cmds.select(curves,r=1)

def ldCurveWarp_findRibbon():
    sel = cmds.ls(sl=1,o=1)
    cmds.select(cl=1)
    curves = cmds.filterExpand(sel,sm=9)
    meshes = cmds.filterExpand(sel,sm=12)
    if curves != None:
        meshToSelect = []
        for i in curves:
            curveShape = cmds.listRelatives(i)
            curveWarp =cmds.listConnections(curveShape[0])
            mesh = cmds.listConnections(curveWarp[0],t='transform')
            mesh = mesh[0] 
            meshToSelect.append(mesh)
        cmds.select(meshToSelect,r=1)
    else:
        cmds.select(meshes,r=1) 
    
def LDRibbonTools_ribbonFromMesh(sel):
    #prepare inputs
    curves = ld.ls('curve')
    material = LDRibbonTools_getMaterial(sel)
    cornerVtx_uv = LDRibbonTools_getRibbonUV(sel)
    ribbonCurrentSubdiv = LDRibbonTools_getRibbonSubdiv(sel)
    currentSubdiv_width = ribbonCurrentSubdiv[1]
    currentSubdiv_length = ribbonCurrentSubdiv[0]

    #if no inputs
    if curves == None:
        ld.msg("Select some curves first!")
        return
    elif sel == None:
        ld.msg("Select some mesh first!")
        return
    elif cornerVtx_uv == None or len(cornerVtx_uv) != 4:
        ld.msg("Select ribbon mesh first!")
        return
    #prepare groups
    bendGroupName = cmds.group(n="bendHandle#",em=1)
    groupName = cmds.group(n="ribbonMeshGroup#",em=1)
    cmds.hide(bendGroupName)
    createdMesh = []
        
    for i in curves:
        polyCreateName = cmds.polyPlane( sx = currentSubdiv_width, sy = currentSubdiv_length )
        cmds.hyperShade(assign=material)
        polyName = polyCreateName[0]
        polyPlaneName = polyCreateName[1]
        cmds.setAttr(polyName+'.rz',-90)
        ld.freeze(polyName)
        bendCreateName = cmds.nonLinear(polyName, type='bend',lowBound=-1,highBound=1,curvature=0)
        bendName = bendCreateName[0] 
        bendHandleName = bendCreateName[1]
        curveLength = cmds.arclen(i)
        curveWarpName = cmds.createCurveWarp(polyName,i)
        # default value for polyPlane
        cmds.setAttr(curveWarpName+'.alignmentMode',4) #align z
        cmds.setAttr(polyPlaneName+'.height',curveLength) #max length   

        sliderList = LDRibbonTools_getSliderList()
        attrAddList = sliderList['attrName'] 
        minValue = sliderList['minValue']
        maxValue = sliderList['maxValue']
        softMinValue = sliderList['softMinValue']
        softMaxValue = sliderList['softMaxValue']
        precision     = sliderList['precision']
        defaultValue  = sliderList['value']
        
        for index in range(len(sliderList['attrName'])):
            attributeType = 'long' if precision[index] == 0 else 'double'
            cmds.addAttr(polyName,ln = attrAddList[index], min = minValue[index], smn = softMinValue[index], max = maxValue[index], smx = softMaxValue[index], at = attributeType, dv = defaultValue[index], k=1)
            
        cmds.addAttr(polyName,ln="twistReverse", min=0, max=1,at="long",dv=0,k=1)
        cmds.addAttr(polyName,ln="curvature", min = -180 ,max =180, at="long", dv=0,k=1)
        
        polyTwistReverse = polyName+'.twistReverse' 
        cmds.scriptJob(ro=0, ac=[polyTwistReverse, 'LDRibbonTools_ribbon_updateTwistReverse("'+ polyName +'","' + curveWarpName +'")'])
        LDRibbonTools_scriptJob_twistReverse = 'cmds.scriptJob(ro=0, ac=["'+polyTwistReverse+'", \'LDRibbonTools_ribbon_updateTwistReverse("' + polyName +'","' + curveWarpName +'")\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistReverse , n="ldCurveWarpScriptNode#", stp="python")        
        
        cmds.connectAttr(polyName+'.flip',curveWarpName+'.flipAxis')
        cmds.expression(s = curveWarpName+".maxScale"+'='+polyName+".widthScale*2")
        cmds.expression(s = curveWarpName+".lengthScale"+'='+polyName+".lengthScale/100")
        cmds.expression(s = curveWarpName+".offset"+'='+polyName+".offset/100")
        cmds.connectAttr(polyName+'.rotation',curveWarpName+'.rotation')
        cmds.connectAttr(polyName+'.curvature',bendName+'.curvature')
        
        polyTwistRotation = polyName + '.twistRotation'
        cmds.scriptJob(ro=0, ac=[polyTwistRotation, 'LDRibbonTools_ribbon_updateTwistRotation("'+ polyName +'","' + curveWarpName +'")'])
        LDRibbonTools_scriptJob_twistRotation = 'cmds.scriptJob(ro=0, ac=["'+polyTwistRotation+'", \'LDRibbonTools_ribbon_updateTwistRotation("' + polyName +'","' + curveWarpName +'")\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistRotation , n="ldCurveWarpScriptNode#", stp="python")
        
        cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',0.001)
        cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',0.999)

        polySubdivLength = polyName+'.subdivLength'
        polySubdivWidth = polyName+'.subdivWidth'
        polyPlaneSubdivLength = polyPlaneName+'.subdivisionsHeight'
        polyPlaneSubdivWidth = polyPlaneName+'.subdivisionsWidth'
        cmds.scriptJob(ro=0, ac=[polySubdivLength, 'LDRibbonTools_ribbon_updateSubdiv("'+ polyName +'","' + polyPlaneName +'")'])
        cmds.scriptJob(ro=0, ac=[polySubdivWidth , 'LDRibbonTools_ribbon_updateSubdiv("'+ polyName +'","' + polyPlaneName  +'")'])
        LDRibbonTools_scriptJob_subdivLength = 'cmds.scriptJob(ro=0, ac=["'+polySubdivLength+'", \'LDRibbonTools_ribbon_updateSubdiv("' + polyName +'","' + polyPlaneName +'")\'])'
        LDRibbonTools_scriptJob_subdivWidth  = 'cmds.scriptJob(ro=0, ac=["'+polySubdivWidth+'",  \'LDRibbonTools_ribbon_updateSubdiv("' + polyName +'","' + polyPlaneName + '")\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_subdivLength , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_subdivWidth , n="ldCurveWarpScriptNode#", stp="python")
        
        polyTwistStartPos = polyName + '.twistStartPos'
        polyTwistStartValue = polyName + '.twistStartValue'
        curveTwistStartPos1 = curveWarpName + '.twistCurve[1].twistCurve_Position'
        curveTwistStartPos2 = curveWarpName + '.twistCurve[2].twistCurve_Position'
        curveTwistStartValue1 = curveWarpName + '.twistCurve[1].twistCurve_Value'
        curveTwistStartValue2 = curveWarpName + '.twistCurve[2].twistCurve_Value'
        cmds.scriptJob(ro=0, ac=[polyTwistStartPos , 'LDRibbonTools_setAttr("'+ curveTwistStartPos1 +'","' + polyTwistStartPos  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartPos , 'LDRibbonTools_setAttr("'+ curveTwistStartPos2 +'","' + polyTwistStartPos  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartValue , 'LDRibbonTools_setAttr("'+ curveTwistStartValue1 +'","' + polyTwistStartValue  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartValue , 'LDRibbonTools_setAttr("'+ curveTwistStartValue2 +'","' + polyTwistStartValue  +'",0.01)'])
        LDRibbonTools_scriptJob_twistStartPos1   = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartPos+'", \'LDRibbonTools_setAttr("' + curveTwistStartPos1 +'","'+ polyTwistStartPos +'",0.01)\'])'
        LDRibbonTools_scriptJob_twistStartPos2   = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartPos+'", \'LDRibbonTools_setAttr("' + curveTwistStartPos2 +'","'+ polyTwistStartPos +'",0.01)\'])'
        LDRibbonTools_scriptJob_twistStartValue1 = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartValue+'", \'LDRibbonTools_setAttr("' + curveTwistStartValue1 +'","'+ polyTwistStartValue +'",0.01)\'])'
        LDRibbonTools_scriptJob_twistStartValue2 = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartValue+'", \'LDRibbonTools_setAttr("' + curveTwistStartValue2 +'","'+ polyTwistStartValue +'",0.01)\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistStartPos1 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistStartPos2 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistStartValue1 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_twistStartValue2 , n="ldCurveWarpScriptNode#", stp="python")
            
        polyScaleRoot = polyName + '.scaleRoot'
        polyScaleTip = polyName + '.scaleTip'
        curveScaleRoot = curveWarpName + '.scaleCurve[0].scaleCurve_Value'
        curveScaleTip = curveWarpName + '.scaleCurve[3].scaleCurve_Value'
        cmds.scriptJob(ro=0, ac=[polyScaleRoot, 'LDRibbonTools_setAttr("'+ curveScaleRoot+'","' + polyScaleRoot +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyScaleTip , 'LDRibbonTools_setAttr("'+ curveScaleTip +'","' + polyScaleTip  +'",0.01)'])
        LDRibbonTools_scriptJob_scaleRoot   = 'cmds.scriptJob(ro=0, ac=["'+polyScaleRoot+'", \'LDRibbonTools_setAttr("' + curveScaleRoot +'","'+ polyScaleRoot +'",0.01)\'])'
        LDRibbonTools_scriptJob_scaleTip    = 'cmds.scriptJob(ro=0, ac=["'+polyScaleTip +'", \'LDRibbonTools_setAttr("' + curveScaleTip +'","'+ polyScaleTip  +'",0.01)\'])'
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_scaleRoot , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=LDRibbonTools_scriptJob_scaleTip , n="ldCurveWarpScriptNode#", stp="python")
        
        # edit uv
        LDRibbonTools_ribbon_recoverUV(polyName,cornerVtx_uv,currentSubdiv_width,currentSubdiv_length)
        # group closure
        LDRibbonTools_movePivotToCurve0()
        cmds.parent(polyName,groupName)
        cmds.parent(bendHandleName,bendGroupName)
        createdMesh.append(polyName)
    cmds.select(createdMesh,r=1)
    
def LDRibbonTools_ribbon_recoverUV(polyName,cornerVtx_uv,currentSubdiv_width,currentSubdiv_length):
    polyMesh = ld.MFnMesh(polyName)
    polyVtxNum = polyMesh.numVertices
    cornerVtx = cornerVtx_uv.keys()
    cornerVtx.sort()
    leftBottomUV  = cornerVtx_uv[cornerVtx[0]]
    rightBottomUV = cornerVtx_uv[cornerVtx[1]]
    leftTopUV     = cornerVtx_uv[cornerVtx[2]]
    rightTopUV    = cornerVtx_uv[cornerVtx[3]]
    vecX = [ (rightBottomUV[0] - leftBottomUV[0]) / currentSubdiv_width , (rightBottomUV[1] - leftBottomUV[1])/currentSubdiv_width]
    vecY = [ (leftTopUV[0]     - leftBottomUV[0]) / currentSubdiv_length ,(leftTopUV[1]     - leftBottomUV[1])/currentSubdiv_length]

    for i in range(polyVtxNum): 
        newU = leftBottomUV[0] + ( i % (currentSubdiv_width+1) ) * vecX[0] + ( i / (currentSubdiv_width +1) ) * vecY[0]
        newV = leftBottomUV[1] + ( i % (currentSubdiv_width+1) ) * vecX[1] + ( i / (currentSubdiv_width +1) ) * vecY[1]
        cmds.polyEditUV( polyName +'.map['+str(i)+']',u=newU,v=newV,r=0)
        
def LDRibbonTools_ribbon_updateSubdiv(sel,polyPlaneName):
    cornerVtx_uv = LDRibbonTools_getRibbonUV(sel)
    # first update subdiv then deal with uv
    targetSubdivLength = cmds.getAttr(sel+'.subdivLength')
    cmds.setAttr(polyPlaneName+'.subdivisionsHeight',targetSubdivLength)
    targetSubdivWidth = cmds.getAttr(sel+'.subdivWidth')
    cmds.setAttr(polyPlaneName+'.subdivisionsWidth',targetSubdivWidth)
    # fix bugs
    # cmds.polyMapSewMove(sel+'.e[*]')
    # get new info
    ribbonCurrentSubdiv = LDRibbonTools_getRibbonSubdiv(sel)
    currentSubdiv_width = ribbonCurrentSubdiv[1]
    currentSubdiv_length = ribbonCurrentSubdiv[0]
    # assign new uv to every uvid
    LDRibbonTools_ribbon_recoverUV(sel,cornerVtx_uv,currentSubdiv_width,currentSubdiv_length)

def LDRibbonTools_ribbon_updateTwistRotation(sel,curveWarpName):
    targetTwistRotation = cmds.getAttr(sel + '.twistRotation')
    currentTwistRotation = cmds.getAttr(curveWarpName + '.twistRotation')
    currentTwistMiddleValue = cmds.getAttr(sel + '.twistStartValue')

    currentTwistRotation0 = cmds.getAttr(curveWarpName + '.twistCurve[0].twistCurve_Value')
    currentTwistRotation3 = cmds.getAttr(curveWarpName + '.twistCurve[3].twistCurve_Value')
    
    if currentTwistRotation3 * targetTwistRotation < 0 :
        cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',-1*currentTwistRotation0)
        cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',-1*currentTwistRotation3)
        cmds.setAttr(sel+'.twistStartValue',-1*currentTwistMiddleValue)
    cmds.setAttr(curveWarpName + '.twistRotation', abs(targetTwistRotation))
    
def LDRibbonTools_ribbon_updateTwistReverse(sel,curveWarpName):
    currentTwistRotation0 = cmds.getAttr(curveWarpName + '.twistCurve[0].twistCurve_Value')
    currentTwistRotation3 = cmds.getAttr(curveWarpName + '.twistCurve[3].twistCurve_Value')
    cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',currentTwistRotation3)
    cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',currentTwistRotation0)
    
def LDRibbonTools_setAttr(attr,channel,multiplier=1):
    cmds.setAttr(attr,cmds.getAttr(channel)*multiplier)

#Edit
        
def fixCurvatureDirection():
    mods = cmds.getModifiers()
    if (mods==8):
        sel = cmds.ls(sl=1,o=1)
        kWorld = om2.MSpace.kWorld
        for each in sel:
            eachList = om2.MSelectionList()
            eachList.add(each)
            eachPath = eachList.getDagPath(0)
            eachMesh = om2.MFnMesh(eachPath)
            point0 = eachMesh.getPoint(0,space=kWorld)
            point1 = eachMesh.getPoint(1,space=kWorld)
            point0_MVec = om2.MVector(point0[0],point0[1],point0[2])
            point1_MVec = om2.MVector(point1[0],point1[1],point1[2])
            normal0 = eachMesh.getClosestNormal(point0,space=kWorld)
            normal1 = eachMesh.getClosestNormal(point1,space=kWorld)
            point0N = point0_MVec + normal0[0]
            point1N = point1_MVec + normal1[0]
            vec0_1 = point1_MVec - point0_MVec
            vec0_1_length = vec0_1.length()
            point0N_MVec = om2.MVector(point0N[0],point0N[1],point0N[2])
            point1N_MVec = om2.MVector(point1N[0],point1N[1],point1N[2])
            vec0N_1N =  point1N_MVec - point0N_MVec
            ifSameDirection = vec0_1*vec0N_1N
            attrCurvature = each+'.curvature'
            if ifSameDirection>0 or vec0N_1N.length()>vec0_1.length():
                curvatureValue = cmds.getAttr(attrCurvature)
                cmds.setAttr(attrCurvature, curvatureValue*(-1))
    else:
        sel = cmds.ls(sl=1,o=1)
        kWorld = om2.MSpace.kWorld
        for each in sel:
            eachList = om2.MSelectionList()
            eachList.add(each)
            eachPath = eachList.getDagPath(0)
            eachMesh = om2.MFnMesh(eachPath)
            point0 = eachMesh.getPoint(0,space=kWorld)
            point1 = eachMesh.getPoint(1,space=kWorld)
            point0_MVec = om2.MVector(point0[0],point0[1],point0[2])
            point1_MVec = om2.MVector(point1[0],point1[1],point1[2])
            normal0 = eachMesh.getClosestNormal(point0,space=kWorld)
            normal1 = eachMesh.getClosestNormal(point1,space=kWorld)
            point0N = point0_MVec + normal0[0]
            point1N = point1_MVec + normal1[0]
            vec0_1 = point1_MVec - point0_MVec
            vec0_1_length = vec0_1.length()
            point0N_MVec = om2.MVector(point0N[0],point0N[1],point0N[2])
            point1N_MVec = om2.MVector(point1N[0],point1N[1],point1N[2])
            vec0N_1N =  point1N_MVec - point0N_MVec
            ifSameDirection = vec0_1*vec0N_1N
            attrCurvature = each+'.curvature'
            if ifSameDirection<0 or vec0N_1N.length()<vec0_1.length():
                curvatureValue = cmds.getAttr(attrCurvature)
                cmds.setAttr(attrCurvature, curvatureValue*(-1))
                
def rotateRibbonToNormal():
    sel = cmds.ls(sl=1,o=1)
    target = sel[-1]
    targetList = om2.MSelectionList()
    targetList.add(target)
    targetPath = targetList.getDagPath(0)
    targetMesh = om2.MFnMesh(targetPath)
    for i in sel[:-1]:
        try:
            cmds.getAttr(i+'.rotation')
            rotateRibbonToNormal_curveWarp(i,targetMesh)
        except:
            rotateRibbonToNormal_ribbon(i,targetMesh)
        
def rotateRibbonToNormal_ribbon(eachRibbon,targetMesh):
    kWorld = om2.MSpace.kWorld
    eachRibbonList = om2.MSelectionList()
    eachRibbonList.add(eachRibbon)
    eachRibbonPath = eachRibbonList.getDagPath(0)
    eachMesh = om2.MFnMesh(eachRibbonPath)
    point8 = eachMesh.getPoint(8, space=kWorld)
    point0 = eachMesh.getPoint(0, space=kWorld)
    point9 = eachMesh.getPoint(9, space=kWorld)
    splineVec = (point9[0] - point8[0], point9[1] - point8[1], point9[2] - point8[2])
    sideVec = (point0[0] - point8[0], point0[1] - point8[1], point0[2] - point8[2])
    splineMVector = om2.MVector(splineVec)    
    sideMVector = om2.MVector(sideVec)
    normal8 = sideMVector^splineMVector
    normal8.normalize()
    targetMesh_MVector = targetMesh.getClosestNormal(point8 , space = kWorld)
    dotProduct = targetMesh_MVector[0]*normal8
    normal = targetMesh_MVector[0]^splineMVector # got normal of vertical plane
    normal.normalize()
    normalA = normal[0]
    normalB = normal[1]
    normalC = normal[2]
    x0 = point8[0]
    y0 = point8[1]
    z0 = point8[2]
    distance = normalA*normal8[0] + normalB*normal8[1]+ normalC*normal8[2]/((normalA**2+normalB**2+normalC**2)**(0.5))
    arc = math.asin(distance)
    angle = arc*180/3.14
    orientation = cmds.getAttr(eachRibbon+'.orientation')
    if dotProduct>0:
        orientValue = orientation+180-angle
    else:
        orientValue = orientation+angle
    cmds.setAttr(eachRibbon+'.orientation',orientValue)

def rotateRibbonToNormal_curveWarp(eachRibbon,targetMesh):
    kWorld = om2.MSpace.kWorld
    eachRibbonList = om2.MSelectionList()
    eachRibbonList.add(eachRibbon)
    eachRibbonPath = eachRibbonList.getDagPath(0)
    eachMesh = om2.MFnMesh(eachRibbonPath)
    point8 = eachMesh.getPoint(8, space=kWorld)
    point0 = eachMesh.getPoint(0, space=kWorld)
    point9 = eachMesh.getPoint(9, space=kWorld)
    splineVec = (point9[0] - point8[0], point9[1] - point8[1], point9[2] - point8[2])
    sideVec = (point0[0] - point8[0], point0[1] - point8[1], point0[2] - point8[2])
    splineMVector = om2.MVector(splineVec)    
    sideMVector = om2.MVector(sideVec)
    normal8 = sideMVector^splineMVector
    normal8.normalize()
    targetMesh_MVector = targetMesh.getClosestNormal(point8 , space = kWorld)
    dotProduct = targetMesh_MVector[0]*normal8
    normal = targetMesh_MVector[0]^splineMVector # got normal of vertical plane
    normal.normalize()
    normalA = normal[0]
    normalB = normal[1]
    normalC = normal[2]
    x0 = point8[0]
    y0 = point8[1]
    z0 = point8[2]
    distance = normalA*normal8[0] + normalB*normal8[1]+ normalC*normal8[2]/((normalA**2+normalB**2+normalC**2)**(0.5))
    arc = math.asin(distance)
    angle = arc*180/3.14
    rotation = cmds.getAttr(eachRibbon+'.rotation')
    if dotProduct>0:
        orientValue = rotation+180-angle
    else:
        orientValue = rotation+angle
    cmds.setAttr(eachRibbon+'.rotation',orientValue)
'''
#UI
'''

class LDRibbonToolsUI_cls(LDRibbonToolsUI_list_form, LDRibbonToolsUI_list_base):
    def __init__(self, parent = get_maya_window()):
        super(LDRibbonToolsUI_cls, self).__init__(parent)
        self.window_name = ldmt_window_name
        self.setupUi(self)
        self.setupBtn()
        self.statusBar.showMessage(" Procedure Ribbon Tools by Liu Dian Email: xgits@outlook.com")
        
        # update status bar so it's not only show in help line window.
        self.installStartBar()
    def setupBtn(self):
        #generate
        self.btn_add.clicked.connect(self.add)
        self.btn_remove.clicked.connect(self.remove)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_generateRibbon.clicked.connect(LDRibbonTools_ribbonCreate)
        self.btn_generateFromMesh.clicked.connect(self.generateFromMesh)
        self.btn_pivotToCV0.clicked.connect(LDRibbonTools_movePivotToCurve0)
        self.btn_reverseCV.clicked.connect(LDRibbonTools_reverseCurve)
        self.btn_densifyCV.clicked.connect(LDRibbonTools_densifyCV)
        self.btn_smoothCV.clicked.connect(LDRibbonTools_smoothCV)
        self.btn_smoothCV.clicked.connect(LDRibbonTools_smoothCV)
        self.btn_smoothCV.clicked.connect(LDRibbonTools_smoothCV)

        self.btn_getCurveFromMesh.clicked.connect(ldCurveWarp_findCurve)
        self.btn_getMeshFromCurve.clicked.connect(ldCurveWarp_findRibbon)

        #edit
        self.text_randomIntensity.setText("20")
        self.btn_random_width.clicked.connect(partial(self.ribbonMaster_random,"width"))
        self.btn_random_curvature.clicked.connect(partial(self.ribbonMaster_random,"curvature"))
        self.btn_random_rotation.clicked.connect(partial(self.ribbonMaster_random,"rotation"))
        self.btn_random_taper.clicked.connect(partial(self.ribbonMaster_random,"taper"))
        self.btn_random_twist.clicked.connect(partial(self.ribbonMaster_random,"twist"))
        self.btn_fixCurvature.clicked.connect(fixCurvatureDirection)
        self.btn_alignRibbonToTangent.clicked.connect(rotateRibbonToNormal)

    def installStartBar(self):
        QPushButtons = self.findChildren(QPushButton)
        for i in QPushButtons:
            i.installEventFilter(self)

    def eventFilter(self, obj, event ):
        '''Connect signals on mouse over''' 
        if event.type() == QEvent.Enter:
            self.oldMessage = self.statusBar.currentMessage()
            self.statusBar.showMessage(obj.statusTip(),0) 
        elif event.type() == QEvent.Leave:
            self.statusBar.showMessage(self.oldMessage, 0)
            pass 
            event.accept()
        return False 

    def closeEvent(self,event):
        ld.turnToolBtnOff(self,ldmt_button_name)
        cmds.deleteUI(ldmt_window_name)

    def add(self):
        sel = ld.ls()
        for each in sel:
            self.list_selection.addItem(QListWidgetItem(each))
        
    def remove(self):
        currentRow = self.list_selection.currentRow()
        selectedItem = self.list_selection.takeItem(currentRow)
        self.list_selection.removeItemWidget(selectedItem)
            
    def clear(self):
        self.list_selection.clear()
        
    def generateFromMesh(self):
        sel = self.LDRibbonTools_getMesh()
        LDRibbonTools_ribbonFromMesh(sel)
        
    def LDRibbonTools_getMesh(self):
        sel = ld.ls(0,'mesh')
        if sel == None:
            sel = self.LDRibbonTools_getBaseMesh()
            if sel == None:
                ld.msg("Please Select Something!")
                return
            return sel
        else:
            return sel
            
    def LDRibbonTools_getBaseMesh(self):
        try:
            currentItem = self.list_selection.currentItem().text()
            return currentItem
        except:
            return 
    def ribbonMaster_random(self,ribbonAttr_msg):
        sel = cmds.ls(sl=1,o=1)
        randomPercentage = self.text_randomIntensity.text()
        try:
            randomPercentage = int(randomPercentage)
        except:
            ld.msg("Input is not valid!")
        for each in sel:
            if cmds.attributeQuery("twistRotation",node=each,ex=1):
                if ribbonAttr_msg == "width":
                    ribbonAttr = "widthScale"
                elif ribbonAttr_msg == "taper":
                    ribbonAttr = "scaleTip"
                elif ribbonAttr_msg == "curvature":
                    ribbonAttr = "curvature" 
                elif ribbonAttr_msg == "rotation":
                    ribbonAttr = "rotation" 
                elif ribbonAttr_msg == "twist":
                    ribbonAttr = "twistRotation"
            if not cmds.attributeQuery("twistRotation",node=each,ex=1):
                if ribbonAttr_msg == "width":
                    ribbonAttr = "width"
                elif ribbonAttr_msg == "taper":
                    ribbonAttr = "taper"
                elif ribbonAttr_msg == "curvature":
                    ribbonAttr = "curvature" 
                elif ribbonAttr_msg == "rotation":
                    ribbonAttr = "orientation" 
                elif ribbonAttr_msg == "twist":
                    ribbonAttr = "twist"
            ribbonAttrName = each+'.'+ribbonAttr
            ribbonAttrCurrentValue = cmds.getAttr(ribbonAttrName)
            baseValue = ribbonAttrCurrentValue
            if ribbonAttr == "rotation":
                constValue = 180
                if random.random()>0.5:
                    targetValue = baseValue+constValue*randomPercentage/100.0*random.random()
                else:    
                    targetValue = baseValue-constValue*randomPercentage/100.0*random.random()
            else:    
                if random.random()>0.5:
                    targetValue = baseValue*(1-randomPercentage/100.0*random.random())
                else:
                    targetValue = baseValue*(1+2*randomPercentage/100.0*random.random())
            ribbonAttrCurrentValue = cmds.getAttr(ribbonAttrName)
            cmds.setAttr(ribbonAttrName, targetValue)

def LDRibbonToolsUI_init():
    if not ld.existsCmd('createCurveWarp'):
        try:
            cmds.loadPlugin('curveWarp')
        except:
            ld.msg("Please Update to 2017!")
    if cmds.window(ldmt_window_name,ex=1):
        if cmds.window(ldmt_window_name,q=1,vis=1):
            cmds.window(ldmt_window_name,e=1,vis=0)
        else:
            cmds.window(ldmt_window_name,e=1,vis=1)

def LDRibbonToolsUI_show():
    LDRibbonToolsUI_init()
    ui = LDRibbonToolsUI_cls()
    ui.show()

if __name__ == '__main__':
    LDRibbonToolsUI_show()



    