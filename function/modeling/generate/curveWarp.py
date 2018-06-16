import maya.cmds as cmds
import maya.mel as mel
from ldmaya import ldmaya as ld
orange       = [ 0.86 , 0.58 , 0.34 ]
green        = [ 0.37 , 0.68 , 0.53 ]
blue         = [ 0.35 , 0.65 , 0.80 ]

def ldCurveWarp_ui():
    if cmds.window("ldCurveWarp_ui",ex=1):
        cmds.deleteUI("ldCurveWarp_ui")
    cmds.window("ldCurveWarp_ui",sizeable=1,h=80)
    cmds.frameLayout("curveWarpUI_layout",l="ldCurveWarp_ui",collapsable=0,mh=8)
    cmds.gridLayout(numberOfColumns = 1, cellHeight = 32, cellWidth=280)
    
    cmds.gridLayout(numberOfColumns = 2, cellHeight = 32, cellWidth=140)
    cmds.button(l='Select Base Mesh',bgc=orange,c='ldCurveWarp_selectBaseMesh()')
    cmds.optionMenu('ldCurveWarp_meshOption')
    cmds.menuItem('ldCurveWarp_mesh0',l="...")
    cmds.menuItem('ldCurveWarp_mesh1',l="...")
    cmds.menuItem('ldCurveWarp_mesh2',l="...")
    cmds.menuItem('ldCurveWarp_mesh3',l="...")
    cmds.menuItem('ldCurveWarp_mesh4',l="...")
    cmds.menuItem('ldCurveWarp_mesh5',l="...")
    cmds.menuItem('ldCurveWarp_mesh6',l="...")
    cmds.menuItem('ldCurveWarp_mesh7',l="...")
    cmds.menuItem('ldCurveWarp_mesh8',l="...")
    cmds.menuItem('ldCurveWarp_mesh9',l="...")
    cmds.menuItem('ldCurveWarp_mesh10',l="...")
    cmds.menuItem('ldCurveWarp_mesh11',l="...")
    cmds.menuItem('ldCurveWarp_mesh12',l="...")
    cmds.menuItem('ldCurveWarp_mesh13',l="...")
    cmds.menuItem('ldCurveWarp_mesh14',l="...")
    cmds.menuItem('ldCurveWarp_mesh15',l="...")

    cmds.setParent('..')
    
    # create sliderbutton using loop
    cmds.gridLayout(numberOfColumns = 2, cellHeight = 32, cellWidth=140)
    cmds.button(l='Ribbon From Mesh',bgc= green,c='ldCurveWarp_ribbonFromMesh()')
    cmds.button(l='Create Ribbon', bgc= blue,c='ldCurveWarp_ribbonCreate()')
    cmds.setParent('..')
    
    cmds.gridLayout(numberOfColumns = 2, cellHeight = 32, cellWidth=140)
    cmds.button(l='Move Pivot To Curve0',c='ldCurveWarp_movePivotToCurve0()')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = 32, cellWidth=70)
    cmds.button(l='Reverse CV',c='ldCurveWarp_reverseCurve()')
    cmds.button(l='Rebuild CV',c='ldCurveWarp_rebuildCurve()')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.showWindow()
    
def ldCurveWarp_getSliderList():
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
    minValue       = [  0   ,   -360   ,    0.01     ,    0.01      ,   0    ,       1       ,       1      ,     0      ,     0     ,      0         ,          0           ,        0          ]
    fieldMinValue  = [  0   ,   -360   ,    0.001    ,    0.001     ,   0    ,       1       ,       1      ,     0      ,     0     ,      0         ,          0           ,        0          ]
    maxValue       = [  1   ,    360   ,    100      ,     100      ,  100   ,      100      ,       12     ,    100     ,    100    ,     3600       ,         100          ,       100         ]
    fieldMaxValue  = [  1   ,    360   ,    1000     ,     100      ,  100   ,      300      ,       50     ,    100     ,    100    ,   3600000      ,         100          ,       100         ]
    value          = [  0   ,     0    ,     1       ,     100      ,   0    ,       10      ,       2      ,     50     ,     50    ,      0         ,          50          ,        50         ]
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
    sliderList['fieldMinValue'] = fieldMinValue
    sliderList['maxValue']      = maxValue
    sliderList['fieldMaxValue'] = fieldMaxValue
    sliderList['value']         = value
    sliderList['precision']     = precision
    return sliderList
    
def ldCurveWarp_selectBaseMesh():
    sel = cmds.ls(o=1,os=1)
    if len(sel) == 1:
        currentIndex = cmds.optionMenu('ldCurveWarp_meshOption',q=1,sl=1)
        currentItem = 'ldCurveWarp_mesh'+str(currentIndex-1)
        cmds.menuItem(currentItem, e=1, l=sel[0])
    elif len(sel) > 1:
        for i in range(len(sel)):
            currentIndex = cmds.optionMenu('ldCurveWarp_meshOption',q=1,sl=1)
            currentItem = 'ldCurveWarp_mesh'+str(i+currentIndex-1)
            cmds.menuItem(currentItem, e=1, l=sel[i])

def ldCurveWarp_getBaseMesh():
    currentIndex = cmds.optionMenu('ldCurveWarp_meshOption',q=1,sl=1)
    currentItem = 'ldCurveWarp_mesh'+str(currentIndex-1)
    return cmds.menuItem(currentItem, q=1, l=1)
    
def ldCurveWarp_movePivotToCurve0():
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

def ldCurveWarp_reverseCurve():
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
                
def ldCurveWarp_rebuildCurve():
    sel = cmds.ls(sl=1,o=1) 
    for i in sel:
        shapeNode = cmds.listRelatives(i,s=1)
        nodeType = cmds.nodeType(shapeNode)
        if nodeType == 'nurbsCurve':
            curveName = i
            cmds.rebuildCurve(curveName,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=0,kt=0,s=0,d=3,tol=0.01)
        else:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            if curveWarpName != None:
                curveName = cmds.listConnections(curveWarpName, t='curveShape')
                curveName = curveName[0]
                cmds.rebuildCurve(curveName,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=0,kt=0,s=0,d=3,tol=0.01)
    cmds.select(sel,r=1)  
              
def ldCurveWarp_ribbonCreate():
    sel = ld.ls("curve")
    if sel == None:
        ld.msg("Select Curve Please!")
        return
    bendGroupName = cmds.group(n="bendHandle#",em=1)
    groupName = cmds.group(n="ribbonMeshGroup#",em=1)
    cmds.hide(bendGroupName)
    createdMesh = []
    for i in sel:
        polyCreateName = cmds.polyPlane(sx=2,sy=10)
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
        
        sliderList = ldCurveWarp_getSliderList()
        attrAddList = sliderList['attrName'] 
        minValue = sliderList['minValue']
        maxValue = sliderList['maxValue']
        precision     = sliderList['precision']
        defaultValue  = sliderList['value']
         
        for index in range(len(sliderList['attrName'])):
            attributeType = 'long' if precision[index] == 0 else 'double'
            cmds.addAttr(polyName,ln = attrAddList[index], min = minValue[index], max = maxValue[index], at =attributeType, dv = defaultValue[index], k=1)
        cmds.addAttr(polyName,ln="twistReverse", min=0, max=1,at="long",dv=0,k=1)
        cmds.addAttr(polyName,ln="curvature", min = -180 ,max =180, at="long", dv=0,k=1)
        
        polyTwistReverse = polyName+'twistReverse' 
        cmds.expression(s = polyName+'.scaleY'+'=(-1)*('+polyName+'.twistReverse*2-1)')
        
        cmds.connectAttr(polyName+'.flip',curveWarpName+'.flipAxis')
        cmds.expression(s = curveWarpName+".maxScale"+'='+polyName+".widthScale*2")
        cmds.expression(s = curveWarpName+".lengthScale"+'='+polyName+".lengthScale/100")
        cmds.expression(s = curveWarpName+".offset"+'='+polyName+".offset/100")
        cmds.connectAttr(polyName+'.rotation',curveWarpName+'.rotation')
        cmds.connectAttr(polyName+'.twistRotation',curveWarpName+'.twistRotation')
        cmds.connectAttr(polyName+'.curvature',bendName+'.curvature')
        
        cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',0.001)
        cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',0.999)

        polySubdivLength = polyName+'.subdivLength'
        polySubdivWidth = polyName+'.subdivWidth'
        polyPlaneSubdivLength = polyPlaneName+'.subdivisionsHeight'
        polyPlaneSubdivWidth = polyPlaneName+'.subdivisionsWidth'
        cmds.scriptJob(ro=0, ac=[polySubdivLength, 'ldCurveWarp_ribbon_updateSubdiv("'+ polyName +'","' + polyPlaneName +'")'])
        cmds.scriptJob(ro=0, ac=[polySubdivWidth , 'ldCurveWarp_ribbon_updateSubdiv("'+ polyName +'","' + polyPlaneName  +'")'])
        ldCurveWarp_scriptJob_subdivLength = 'cmds.scriptJob(ro=0, ac=["'+polySubdivLength+'", \'ldCurveWarp_ribbon_updateSubdiv("' + polyName +'","' + polyPlaneName +'")\'])'
        ldCurveWarp_scriptJob_subdivWidth  = 'cmds.scriptJob(ro=0, ac=["'+polySubdivWidth+'",  \'ldCurveWarp_ribbon_updateSubdiv("' + polyName +'","' + polyPlaneName + '")\'])'
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_subdivLength , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_subdivWidth , n="ldCurveWarpScriptNode#", stp="python")
        
        polyTwistStartPos = polyName + '.twistStartPos'
        polyTwistStartValue = polyName + '.twistStartValue'
        curveTwistStartPos1 = curveWarpName + '.twistCurve[1].twistCurve_Position'
        curveTwistStartPos2 = curveWarpName + '.twistCurve[2].twistCurve_Position'
        curveTwistStartValue1 = curveWarpName + '.twistCurve[1].twistCurve_Value'
        curveTwistStartValue2 = curveWarpName + '.twistCurve[2].twistCurve_Value'
        cmds.scriptJob(ro=0, ac=[polyTwistStartPos , 'ldCurveWarp_setAttr("'+ curveTwistStartPos1 +'","' + polyTwistStartPos  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartPos , 'ldCurveWarp_setAttr("'+ curveTwistStartPos2 +'","' + polyTwistStartPos  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartValue , 'ldCurveWarp_setAttr("'+ curveTwistStartValue1 +'","' + polyTwistStartValue  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartValue , 'ldCurveWarp_setAttr("'+ curveTwistStartValue2 +'","' + polyTwistStartValue  +'",0.01)'])
        ldCurveWarp_scriptJob_twistStartPos1   = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartPos+'", \'ldCurveWarp_setAttr("' + curveTwistStartPos1 +'","'+ polyTwistStartPos +'",0.01)\'])'
        ldCurveWarp_scriptJob_twistStartPos2   = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartPos+'", \'ldCurveWarp_setAttr("' + curveTwistStartPos2 +'","'+ polyTwistStartPos +'",0.01)\'])'
        ldCurveWarp_scriptJob_twistStartValue1 = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartValue+'", \'ldCurveWarp_setAttr("' + curveTwistStartValue1 +'","'+ polyTwistStartValue +'",0.01)\'])'
        ldCurveWarp_scriptJob_twistStartValue2 = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartValue+'", \'ldCurveWarp_setAttr("' + curveTwistStartValue2 +'","'+ polyTwistStartValue +'",0.01)\'])'
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_twistStartPos1 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_twistStartPos2 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_twistStartValue1 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_twistStartValue2 , n="ldCurveWarpScriptNode#", stp="python")
            
        polyScaleRoot = polyName + '.scaleRoot'
        polyScaleTip = polyName + '.scaleTip'
        curveScaleRoot = curveWarpName + '.scaleCurve[0].scaleCurve_Value'
        curveScaleTip = curveWarpName + '.scaleCurve[3].scaleCurve_Value'
        cmds.scriptJob(ro=0, ac=[polyScaleRoot, 'ldCurveWarp_setAttr("'+ curveScaleRoot+'","' + polyScaleRoot +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyScaleTip , 'ldCurveWarp_setAttr("'+ curveScaleTip +'","' + polyScaleTip  +'",0.01)'])
        ldCurveWarp_scriptJob_scaleRoot   = 'cmds.scriptJob(ro=0, ac=["'+polyScaleRoot+'", \'ldCurveWarp_setAttr("' + curveScaleRoot +'","'+ polyScaleRoot +'",0.01)\'])'
        ldCurveWarp_scriptJob_scaleTip    = 'cmds.scriptJob(ro=0, ac=["'+polyScaleTip +'", \'ldCurveWarp_setAttr("' + curveScaleTip +'","'+ polyScaleTip  +'",0.01)\'])'
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_scaleRoot , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_scaleTip , n="ldCurveWarpScriptNode#", stp="python")

        ldCurveWarp_movePivotToCurve0()
        cmds.parent(polyName,groupName)
        cmds.parent(bendHandleName,bendGroupName)
        createdMesh.append(polyName)
    cmds.select(createdMesh,r=1)

def ldCurveWarp_getMesh():
    sel = ld.ls(0,'mesh')
    if sel == None:
        sel = ldCurveWarp_getBaseMesh()
        if sel.startswith('mesh'):
            return None
        else:
            return sel
    else:
        return sel

# get corner uv [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
def ldCurveWarp_getRibbonUV(sel):
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
        
def ldCurveWarp_getRibbonSubdiv(sel):
    mesh = ld.MFnMesh(sel)
    vtxNum = mesh.numVertices
    edgeRing = cmds.polySelect(sel,edgeRing=0,ns=1)
    length = len(edgeRing)-1
    width = vtxNum/len(edgeRing)-1
    return [length,width]
    
def ldCurveWarp_ribbonFromMesh():
    #prepare inputs
    curves = ld.ls('curve')
    sel = ldCurveWarp_getMesh()
    cornerVtx_uv = ldCurveWarp_getRibbonUV(sel)
    ribbonCurrentSubdiv = ldCurveWarp_getRibbonSubdiv(sel)
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
        sliderList = ldCurveWarp_getSliderList()
        attrAddList = sliderList['attrName'] 
        minValue = sliderList['minValue']
        maxValue = sliderList['maxValue']
        precision     = sliderList['precision']
        defaultValue  = sliderList['value']
         
        for index in range(len(sliderList['attrName'])):
            attributeType = 'long' if precision[index] == 0 else 'double'
            cmds.addAttr(polyName,ln = attrAddList[index], min = minValue[index], max = maxValue[index], at =attributeType, dv = defaultValue[index], k=1)
        cmds.addAttr(polyName,ln="twistReverse", min=0, max=1,at="long",dv=0,k=1)
        cmds.addAttr(polyName,ln="curvature", min = -180 ,max =180, at="long", dv=0,k=1)
        
        polyTwistReverse = polyName+'twistReverse' 
        cmds.expression(s = polyName+'.scaleY'+'=(-1)*('+polyName+'.twistReverse*2-1)')
        
        cmds.connectAttr(polyName+'.flip',curveWarpName+'.flipAxis')
        cmds.expression(s = curveWarpName+".maxScale"+'='+polyName+".widthScale*2")
        cmds.expression(s = curveWarpName+".lengthScale"+'='+polyName+".lengthScale/100")
        cmds.expression(s = curveWarpName+".offset"+'='+polyName+".offset/100")
        cmds.connectAttr(polyName+'.rotation',curveWarpName+'.rotation')
        cmds.connectAttr(polyName+'.twistRotation',curveWarpName+'.twistRotation')
        cmds.connectAttr(polyName+'.curvature',bendName+'.curvature')
        
        cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',0.001)
        cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',0.999)

        polySubdivLength = polyName+'.subdivLength'
        polySubdivWidth = polyName+'.subdivWidth'
        polyPlaneSubdivLength = polyPlaneName+'.subdivisionsHeight'
        polyPlaneSubdivWidth = polyPlaneName+'.subdivisionsWidth'
        cmds.scriptJob(ro=0, ac=[polySubdivLength, 'ldCurveWarp_ribbon_updateSubdiv("'+ polyName +'","' + polyPlaneName +'")'])
        cmds.scriptJob(ro=0, ac=[polySubdivWidth , 'ldCurveWarp_ribbon_updateSubdiv("'+ polyName +'","' + polyPlaneName  +'")'])
        ldCurveWarp_scriptJob_subdivLength = 'cmds.scriptJob(ro=0, ac=["'+polySubdivLength+'", \'ldCurveWarp_ribbon_updateSubdiv("' + polyName +'","' + polyPlaneName +'")\'])'
        ldCurveWarp_scriptJob_subdivWidth  = 'cmds.scriptJob(ro=0, ac=["'+polySubdivWidth+'",  \'ldCurveWarp_ribbon_updateSubdiv("' + polyName +'","' + polyPlaneName + '")\'])'
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_subdivLength , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_subdivWidth , n="ldCurveWarpScriptNode#", stp="python")
        
        polyTwistStartPos = polyName + '.twistStartPos'
        polyTwistStartValue = polyName + '.twistStartValue'
        curveTwistStartPos1 = curveWarpName + '.twistCurve[1].twistCurve_Position'
        curveTwistStartPos2 = curveWarpName + '.twistCurve[2].twistCurve_Position'
        curveTwistStartValue1 = curveWarpName + '.twistCurve[1].twistCurve_Value'
        curveTwistStartValue2 = curveWarpName + '.twistCurve[2].twistCurve_Value'
        cmds.scriptJob(ro=0, ac=[polyTwistStartPos , 'ldCurveWarp_setAttr("'+ curveTwistStartPos1 +'","' + polyTwistStartPos  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartPos , 'ldCurveWarp_setAttr("'+ curveTwistStartPos2 +'","' + polyTwistStartPos  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartValue , 'ldCurveWarp_setAttr("'+ curveTwistStartValue1 +'","' + polyTwistStartValue  +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyTwistStartValue , 'ldCurveWarp_setAttr("'+ curveTwistStartValue2 +'","' + polyTwistStartValue  +'",0.01)'])
        ldCurveWarp_scriptJob_twistStartPos1   = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartPos+'", \'ldCurveWarp_setAttr("' + curveTwistStartPos1 +'","'+ polyTwistStartPos +'",0.01)\'])'
        ldCurveWarp_scriptJob_twistStartPos2   = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartPos+'", \'ldCurveWarp_setAttr("' + curveTwistStartPos2 +'","'+ polyTwistStartPos +'",0.01)\'])'
        ldCurveWarp_scriptJob_twistStartValue1 = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartValue+'", \'ldCurveWarp_setAttr("' + curveTwistStartValue1 +'","'+ polyTwistStartValue +'",0.01)\'])'
        ldCurveWarp_scriptJob_twistStartValue2 = 'cmds.scriptJob(ro=0, ac=["'+polyTwistStartValue+'", \'ldCurveWarp_setAttr("' + curveTwistStartValue2 +'","'+ polyTwistStartValue +'",0.01)\'])'
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_twistStartPos1 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_twistStartPos2 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_twistStartValue1 , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_twistStartValue2 , n="ldCurveWarpScriptNode#", stp="python")
            
        polyScaleRoot = polyName + '.scaleRoot'
        polyScaleTip = polyName + '.scaleTip'
        curveScaleRoot = curveWarpName + '.scaleCurve[0].scaleCurve_Value'
        curveScaleTip = curveWarpName + '.scaleCurve[3].scaleCurve_Value'
        cmds.scriptJob(ro=0, ac=[polyScaleRoot, 'ldCurveWarp_setAttr("'+ curveScaleRoot+'","' + polyScaleRoot +'",0.01)'])
        cmds.scriptJob(ro=0, ac=[polyScaleTip , 'ldCurveWarp_setAttr("'+ curveScaleTip +'","' + polyScaleTip  +'",0.01)'])
        ldCurveWarp_scriptJob_scaleRoot   = 'cmds.scriptJob(ro=0, ac=["'+polyScaleRoot+'", \'ldCurveWarp_setAttr("' + curveScaleRoot +'","'+ polyScaleRoot +'",0.01)\'])'
        ldCurveWarp_scriptJob_scaleTip    = 'cmds.scriptJob(ro=0, ac=["'+polyScaleTip +'", \'ldCurveWarp_setAttr("' + curveScaleTip +'","'+ polyScaleTip  +'",0.01)\'])'
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_scaleRoot , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_scaleTip , n="ldCurveWarpScriptNode#", stp="python")
        
        # edit uv
        ldCurveWarp_ribbon_recoverUV(polyName,cornerVtx_uv,currentSubdiv_width,currentSubdiv_length)
        # group closure
        ldCurveWarp_movePivotToCurve0()
        cmds.parent(polyName,groupName)
        cmds.parent(bendHandleName,bendGroupName)
        createdMesh.append(polyName)
    cmds.select(createdMesh,r=1)
    
def ldCurveWarp_ribbon_recoverUV(polyName,cornerVtx_uv,currentSubdiv_width,currentSubdiv_length):
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
        
def ldCurveWarp_ribbon_updateSubdiv(sel,polyPlaneName):
    cornerVtx_uv = ldCurveWarp_getRibbonUV(sel)
    # first update subdiv then deal with uv
    targetSubdivLength = cmds.getAttr(sel+'.subdivLength')
    cmds.setAttr(polyPlaneName+'.subdivisionsHeight',targetSubdivLength)
    targetSubdivWidth = cmds.getAttr(sel+'.subdivWidth')
    cmds.setAttr(polyPlaneName+'.subdivisionsWidth',targetSubdivWidth)
    # fix bugs
    cmds.polyMapSewMove(sel+'.e[*]')
    
    # get new info
    ribbonCurrentSubdiv = ldCurveWarp_getRibbonSubdiv(sel)
    currentSubdiv_width = ribbonCurrentSubdiv[1]
    currentSubdiv_length = ribbonCurrentSubdiv[0]
    # assign new uv to every uvid
    ldCurveWarp_ribbon_recoverUV(sel,cornerVtx_uv,currentSubdiv_width,currentSubdiv_length)

def ldCurveWarp_setAttr(attr,channel,multiplier=1):
    cmds.setAttr(attr,cmds.getAttr(channel)*multiplier)
    