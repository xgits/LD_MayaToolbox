import os
from ldmt_ui.loadUIFile import get_maya_window, load_ui_type
import maya.OpenMayaUI as omui
from ldmt_core import ldmt_cmds as ld
import maya.cmds as cmds
import maya.mel as mel
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
LDMTPATH = ld.getPath('LDMT')
LDRibbonToolsUI_file = LDMTPATH + '/ldmt_ui/tools/LDRibbonTools.ui'
LDRibbonToolsUI_list_form, LDRibbonToolsUI_list_base = load_ui_type(LDRibbonToolsUI_file)
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

'''
#UI
'''

class LDRibbonToolsUI_cls(LDRibbonToolsUI_list_form, LDRibbonToolsUI_list_base):
    def __init__(self, parent = get_maya_window()):
        super(LDRibbonToolsUI_cls, self).__init__(parent)
        self.window_name = 'LDRibbonToolsUI'
        self.setupUi(self)
        self.setupBtn()
        self.statusBar.showMessage(" Procedure Ribbon Tools by Liu Dian Email: xgits@outlook.com")
        
        # update status bar so it's not only show in help line window.
        self.installStartBar()
    def setupBtn(self):
        self.btn_add.clicked.connect(self.add)
        self.btn_remove.clicked.connect(self.remove)
        self.btn_clear.clicked.connect(self.clear)
        self.btn_generateRibbon.clicked.connect(LDRibbonTools_ribbonCreate)
        self.btn_generateFromMesh.clicked.connect(self.generateFromMesh)
        self.btn_pivotToCV0.clicked.connect(LDRibbonTools_movePivotToCurve0)
        self.btn_reverseCV.clicked.connect(LDRibbonTools_reverseCurve)
        self.btn_densifyCV.clicked.connect(LDRibbonTools_densifyCV)
        self.btn_smoothCV.clicked.connect(LDRibbonTools_smoothCV)
        
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
        
def LDRibbonToolsUI_init():
    if not ld.existsCmd('createCurveWarp'):
        try:
            cmds.loadPlugin('curveWarp')
        except:
            ld.msg("Please Update to 2017!")
    if cmds.window('LDRibbonToolsUI',ex=1):
        cmds.deleteUI('LDRibbonToolsUI')
        
def LDRibbonToolsUI_show():
    LDRibbonToolsUI_init()
    ui = LDRibbonToolsUI_cls()
    ui.show()

if __name__ == '__main__':
    LDRibbonToolsUI_show()



    