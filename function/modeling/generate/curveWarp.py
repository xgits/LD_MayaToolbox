import maya.cmds as cmds
import maya.mel as mel
from ldmaya import ldmaya as ld
reload(ld)

def ldCurveWarp_getSliderList():

    curveAttrName  = {'flip'           :'flipAxis',\
                      'widthScale'     :'maxScale',\
                      'lengthScale'    :'lengthScale',\
                      'offset'         :'offset',\
                      'rotation'       :'rotation',\
                      'scaleRoot'      :'scaleCurve[0].scaleCurve_Value',\
                      'scaleTip'       :'scaleCurve[3].scaleCurve_Value',\
                      'twistStartPos'  :'twistCurve[1].twistCurve_Position',\
                      'twistStartValue':'twistCurve[1].twistCurve_Value'\
                      }

    attrName       = ['flip','widthScale' ,'lengthScale' ,'offset','rotation','subdivLength' ,'subdivWidth' , 'twistRotation' , 'scaleRoot' , 'scaleTip' ,    'twistStartPos'    , 'twistStartValue'  ]
    label          = ['Flip','Width Scale','Length Scale','Offset','Rotation','Subdiv Length','Subdiv Width', 'Twist Rotation', 'Scale Root', 'Scale Tip', 'Twist Start Position', 'Twist Start Value']
    minValue       = [  0   ,    0.01     ,    0.01      ,   0    ,   -360   ,       1       ,       1      ,       0         ,      0      ,      0     ,           0           ,         0          ]
    fieldMinValue  = [  0   ,    0.001    ,    0.001     ,   0    ,   -360   ,       1       ,       1      ,       0         ,      0      ,      0     ,           0           ,         0          ]
    maxValue       = [  1   ,     10      ,     10       ,   1    ,    360   ,       50      ,       24     ,      3600       ,      1      ,      1     ,           1           ,         1          ]
    fieldMaxValue  = [  1   ,    1000     ,    1000      ,   1    ,    360   ,      300      ,       50     ,    3600000      ,      1      ,      1     ,           1           ,         1          ]
    value          = [  0   ,     1       ,     1        ,   0    ,     0    ,       10      ,       6      ,       0         ,      0.5    ,      0.5   ,           0.5         ,         0.5        ]
    precision      = [  0   ,     3       ,     3        ,   3    ,     0    ,       0       ,       0      ,       0         ,      3      ,      3     ,           3           ,         3          ]
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
    
def ldCurveWarp_ui():
    if cmds.window("ldCurveWarp_ui",ex=1):
        cmds.deleteUI("ldCurveWarp_ui")
    cmds.window("ldCurveWarp_ui",sizeable=1,h=240)
    cmds.frameLayout("curveWarpUI_layout",l="ldCurveWarp_ui",collapsable=0,mh=8)
    cmds.gridLayout(numberOfColumns = 4, cellHeight = 22, cellWidth=114)
    cmds.button(l='Select Base Mesh',c='ldCurveWarp_selectObj()')
    cmds.text('ldCurveWarp_meshName',al="center",l="Base Mesh Name")
    cmds.button(al="center",l="Value From Select",c='ldCurveWarp_getValueFromSelect()')
    cmds.button(al="center",l="Reset All",c='ldCurveWarp_resetSlider()')
    cmds.setParent('..')
    
    # create sliderbutton using loop
    sliderList = ldCurveWarp_getSliderList()
    for i in range(len(sliderList['sliderName'])):
        cmds.floatSliderButtonGrp ( sliderList['sliderName'][i],\
                                    cc = 'ldCurveWarp_updateAttr("'+ sliderList['attrName'][i]+ '")',\
                                    buttonLabel = 'Apply',\
                                    bc = 'ldCurveWarp_updateAttr("'+ sliderList['attrName'][i]+ '")',\
                                    label = sliderList['label'][i],\
                                    cal   = (1, 'center'),\
                                    field = True,\
                                    minValue = sliderList['minValue'][i],\
                                    maxValue = sliderList['maxValue'][i],\
                                    fieldMinValue = sliderList['fieldMinValue'][i],\
                                    fieldMaxValue = sliderList['fieldMaxValue'][i],\
                                    value         = sliderList['value'][i],\
                                    pre           = sliderList['precision'][i])
                                    
    cmds.gridLayout(numberOfColumns = 1, cellHeight = 22, cellWidth=456)
    cmds.gridLayout(numberOfColumns = 3, cellHeight = 22, cellWidth=152)
    cmds.button(l='Generate From Select',c='ldCurveWarpFromSelect()')
    cmds.button(l='Generate Ribbon',c='ldCurveWarp_ribbonGen()')
    cmds.button(l='Generate Tube',c='ldCurveWarp_tubeGen()')
    cmds.setParent('..')

    cmds.gridLayout(numberOfColumns = 3, cellHeight = 22, cellWidth=152)
    cmds.button(l='Move Pivot To Curve0',c='ldCurveWarpMovePivotToCurve0()')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = 22, cellWidth=76)
    cmds.button(l='Reverse CV',c='ldCurveWarpReverseCurve()')
    cmds.button(l='Rebuild CV',c='ldCurveWarpRebuildCurve()')
    cmds.setParent('..')
    cmds.button(l='Reverse Twist Direction',c='reverseCurveWarpTwistDirection()')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.showWindow()

def ldCurveWarp_selectObj():
    sel = ld.ls(0)
    ld.freeze(sel)
    cmds.text('ldCurveWarp_meshName',e=1, l=sel)

def ldCurveWarp_getValueFromSelect():
    sel = ld.ls(0,"mesh")
    if sel == None:
        ld.msg("Select Mesh First!")
        return
    curveWarpName = cmds.listConnections(sel,t='curveWarp')
    curveWarpName = curveWarpName[0]
    selList = ldCurveWarp_getSliderList()
    
    selCurveAttrName = selList['curveAttrName']
    selAttrList      = selList['attrName']
    selSliderList    = selList["label"]
    
    selAttrToSlider = {}
    for index in range(len(selAttrList)):
        selAttrToSlider[selAttrList[index]] = selSliderList[index]
    for attrName in selAttrList:
        if attrName in ['width','rotation','subdivLength','subdivWidth','twistRotation']:
            attrValue = cmds.getAttr(sel+'.'+attrName)
            cmds.floatSliderButtonGrp(selAttrToSlider[attrName], e=1,value = attrValue)
        elif attrName in ['scaleCurve[0].scaleCurve_Value','scaleCurve[3].scaleCurve_Value','twistCurve[1].twistCurve_Position','twistCurve[1].twistCurve_Value']:
            attrValue = cmds.getAttr(curveWarpName+'.'+attrName)
            attrValue = abs(attrValue)
            cmds.floatSliderButtonGrp(selAttrToSlider[attrName], e=1,value = attrValue*100)
            
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
                
def ldCurveWarpReverseCurve():
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
                cmds.reverseCurve(curveName,ch=1,rpo=1)
                
                
def ldCurveWarpRebuildCurve():
    sel = cmds.ls(sl=1,o=1) 
    for i in sel:
        shapeNode = cmds.listRelatives(i,s=1)
        nodeType = cmds.nodeType(shapeNode)
        if nodeType == 'nurbsCurve':
            curveName = i
            cmds.rebuildCurve(curveName,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=0,kt=0,s=0,d=3,tol=0.01)
        else:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            if curveWarpName != None:
                curveName = cmds.listConnections(curveWarpName, t='curveShape')
                curveName = curveName[0]
                cmds.rebuildCurve(curveName,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=0,kt=0,s=0,d=3,tol=0.01)

def ldCurveWarpResetSlider():
    slidersList = ['curveWarpWidth','curveWarpRotation','curveWarpSubdivLength','curveWarpSubdivWidth','curveWarpTwistRotation','curveWarpScaleRoot','curveWarpScaleTip','curveWarpTwistStartPos','curveWarpTwistStartValue']
    defaultValueList = {'curveWarpWidth':5,'curveWarpRotation':0,'curveWarpSubdivLength':10,'curveWarpSubdivWidth':3,'curveWarpTwistRotation':0,'curveWarpScaleRoot':50,'curveWarpScaleTip':50,'curveWarpTwistStartPos':50,'curveWarpTwistStartValue':50}
    for sliderName in slidersList:
        defaultValue = defaultValueList[sliderName]
        cmds.floatSliderButtonGrp(sliderName,e=1,value = defaultValue)

def updateCurveWarpAttr(curveWarpAttr):
    sel = cmds.ls(sl=1,o=1)
    sel = cmds.filterExpand(sel,sm=12)
    if sel == None:
        print("Select Mesh First!")
        return
    currentAttr = "None"
    currentAttr1 = "None"
    currentAttr2 = "None"
    currentAttr3 = "None"
    currentSlider = "None"
    
    if curveWarpAttr == "width":
        currentAttr = "width"
        currentSlider = "curveWarpWidth"
    elif curveWarpAttr == "rotation":
        currentAttr = "rotation"
        currentSlider = "curveWarpRotation"
    elif curveWarpAttr == "subdivLength":
        currentAttr = "subdivLength"
        currentSlider = "curveWarpSubdivLength"
    elif curveWarpAttr == "subdivWidth":
        currentAttr = "subdivWidth"
        currentSlider = "curveWarpSubdivWidth"
    elif curveWarpAttr == "twistRotation":
        currentAttr = "twistRotation"
        currentSlider = "curveWarpTwistRotation"    
            
    elif curveWarpAttr == "scaleRoot":
        currentAttr = "scaleCurve[0].scaleCurve_Value"
        currentSlider = "curveWarpScaleRoot"
    elif curveWarpAttr == "scaleTip":
        currentAttr = "scaleCurve[3].scaleCurve_Value"
        currentSlider = "curveWarpScaleTip"
    elif curveWarpAttr == "twistCurvePos":
        currentAttr1 = "twistCurve[1].twistCurve_Position"
        currentAttr2 = "twistCurve[2].twistCurve_Position"
        currentSlider = "curveWarpTwistStartPos"
    elif curveWarpAttr == "twistCurveValue":
        currentAttr1 = "twistCurve[1].twistCurve_Value"
        currentAttr2 = "twistCurve[2].twistCurve_Value"
        currentAttr3 = "twistCurve[3].twistCurve_Value"
        currentSlider = "curveWarpTwistStartValue"
    
    if curveWarpAttr == "width" or curveWarpAttr == "rotation" or curveWarpAttr=="subdivLength" or curveWarpAttr=="subdivWidth" or curveWarpAttr == "twistRotation":
        for i in sel:
            setValue = cmds.floatSliderButtonGrp(currentSlider,q=1,v=1)
            cmds.setAttr(i+'.'+currentAttr,setValue)
            
    elif curveWarpAttr == "scaleRoot" or curveWarpAttr == "scaleTip":
        for i in sel:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            curveWarpName = curveWarpName[0]
            setValue = cmds.floatSliderButtonGrp(currentSlider,q=1,v=1)
            cmds.setAttr(curveWarpName+'.'+currentAttr,setValue/100)
    elif curveWarpAttr == "twistCurvePos":
        for i in sel:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            curveWarpName = curveWarpName[0]
            setValue = cmds.floatSliderButtonGrp(currentSlider,q=1,v=1)
            cmds.setAttr(curveWarpName+'.'+currentAttr1,setValue/100)
            cmds.setAttr(curveWarpName+'.'+currentAttr2,setValue/100)
    elif curveWarpAttr == "twistCurveValue":
        for i in sel:
            curveWarpName = cmds.listConnections(i,t='curveWarp')
            curveWarpName = curveWarpName[0]
            setValue = cmds.floatSliderButtonGrp(currentSlider,q=1,v=1)
            currentAttr3Value = cmds.getAttr(curveWarpName+'.'+currentAttr3)
            cmds.setAttr(curveWarpName+'.'+currentAttr1,currentAttr3Value*setValue/100)
            cmds.setAttr(curveWarpName+'.'+currentAttr2,currentAttr3Value*setValue/100)
            
def reverseCurveWarpTwistDirection():
    sel = cmds.ls(sl=1,o=1)
    sel = cmds.filterExpand(sel,sm=12)
    if sel == None:
        print("Select Curve Please!")
        return
    for i in sel:
        curveWarpName = cmds.listConnections(i,t='curveWarp')
        curveWarpName = curveWarpName[0]
        currentAttr1 = "twistCurve[1].twistCurve_Value"
        currentAttr2 = "twistCurve[2].twistCurve_Value"
        currentAttr3 = "twistCurve[3].twistCurve_Value"
        currentAttr1Value = cmds.getAttr(curveWarpName+'.'+currentAttr1)
        currentAttr2Value = cmds.getAttr(curveWarpName+'.'+currentAttr2)
        currentAttr3Value = cmds.getAttr(curveWarpName+'.'+currentAttr3)
        
        cmds.setAttr(curveWarpName+'.'+currentAttr1,currentAttr1Value*(-1))
        cmds.setAttr(curveWarpName+'.'+currentAttr2,currentAttr2Value*(-1))
        cmds.setAttr(curveWarpName+'.'+currentAttr3,currentAttr3Value*(-1))
        
def ldCurveWarpFromSelect():
    curves = ld.ls('curve')
    if curves == None:
        print("Select some curves first!")
        return
    sel = cmds.filterExpand(sel,sm=12)
    if sel == None:
        sel = cmds.text('ldCurveWarpMeshName',q=1,l=1)
        sel = cmds.duplicate(sel,rr=1,un=1)
        sel = sel[0]
    else:
        sel = cmds.duplicate(sel,rr=1,un=1)
        sel = sel[0]
        
    cmds.move(0,0,0,sel,rpr=1)
    #prepareMesh
    cmds.makeIdentity(sel,apply=True, t=1, r=1, s=1, n=0)
    selBB = cmds.polyEvaluate(sel,b=1)
    selBB_diff_x = selBB[0][1]-selBB[0][0]
    selBB_diff_y = selBB[1][1]-selBB[1][0]
    selBB_diff_z = selBB[2][1]-selBB[2][0]
    alignMode = 3
    if (selBB_diff_y>selBB_diff_x*0.9 and selBB_diff_y> selBB_diff_z*0.9) or selBB_diff_x<0.001 or selBB_diff_z<0.001 :
        pass 
    elif (selBB_diff_z > selBB_diff_x and selBB_diff_z> selBB_diff_y) or selBB_diff_y<0.001:
        alignMode = 4
    else:
        alignMode = 2
    
    for curve in curves:
        instance = sel
        curveWarpName = cmds.createCurveWarp(instance,curve)
        cmds.setAttr(curveWarpName+'.alignmentMode',alignMode) #align y
        
        cmds.addAttr(instance,ln = 'width',min=0.00001,at='double',dv=2,k=1)  
        cmds.connectAttr(instance+'.width',curveWarpName+'.maxScale')

        cmds.addAttr(instance,ln = 'length',min=0.00001,at='double',dv=99999,k=1)  
        cmds.connectAttr(instance+'.length',curveWarpName+'.lengthScale')
      
        cmds.addAttr(instance,ln = 'rotation',at = 'long', dv=180,k=1)
        cmds.connectAttr(instance+'.rotation',curveWarpName+'.rotation')

        cmds.addAttr(instance,ln = 'subdivLength',min=1,at='long',dv=10,k=1)  #placeholder 
        cmds.addAttr(instance,ln = 'subdivWidth', min=1,at='long',dv=6,k=1)  #placeholder
        
        historyNodes = cmds.listHistory(sel)
        for historyNode in historyNodes:
            if cmds.nodeType(historyNode) == 'polyPlane':
                cmds.connectAttr(sel+'.subdivLength',historyNode+'.subdivisionsHeight') 
                cmds.connectAttr(sel+'.subdivWidth',historyNode+'.subdivisionsWidth')
                
        historyNodes = cmds.listHistory(sel)
        for historyNode in historyNodes:
            if cmds.nodeType(historyNode) == 'polyCylinder':
                cmds.connectAttr(sel+'.subdivLength',historyNode+'.subdivisionsHeight') 
                cmds.connectAttr(sel+'.subdivWidth',historyNode+'.subdivisionsAxis') 
                       
        cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',0)
        cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',1)

        cmds.addAttr(instance,ln = 'twistRotation',at='long',dv=0,k=1)
        cmds.connectAttr(instance+'.twistRotation',curveWarpName+'.twistRotation')
        ldCurveWarpMovePivotToCurve0()
        
def ldCurveWarp_tubeGen():
    sel = cmds.ls(sl=1,o=1)
    sel = cmds.filterExpand(sel,sm=9)
    if sel == None:
        print("Select Curve Please!")
        return
    polyNames=[]
    groupName = cmds.group(n="tubeMeshGroup#",em=1)

    for i in sel:
        polyCreateName = cmds.polyCylinder(sx=6,sy=10,sc=1)
        polyName = polyCreateName[0]
        polyPlaneName = polyCreateName[1]
        # polyShapeName = cmds.listRelatives(polyName, shapes=True)
        # polyShapeName = polyShapeName[0]
    
        curveWarpName = cmds.createCurveWarp(polyName,i)
        
        cmds.setAttr(curveWarpName+'.alignmentMode',3) #align y
        cmds.setAttr(polyPlaneName+'.height',9999) #max length
        
        cmds.addAttr(polyName,ln = 'width',min=0.00001,at='double',dv=2,k=1)
        cmds.connectAttr(polyName+'.width',polyPlaneName+'.radius')
        
        cmds.addAttr(polyName,ln = 'rotation',at = 'long', dv=-90,k=1)
        cmds.connectAttr(polyName+'.rotation',curveWarpName+'.rotation')

        cmds.addAttr(polyName,ln = 'subdivLength',min=1,at='long',dv=10,k=1)
        cmds.connectAttr(polyName+'.subdivLength',polyPlaneName+'.subdivisionsHeight')
        
        cmds.addAttr(polyName,ln = 'subdivWidth', min=1,at='long',dv=6,k=1)
        cmds.connectAttr(polyName+'.subdivWidth',polyPlaneName+'.subdivisionsAxis')
        
        cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',0)
        cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',1)

        cmds.addAttr(polyName,ln = 'twistRotation',at='long',dv=0,k=1)
        cmds.connectAttr(polyName+'.twistRotation',curveWarpName+'.twistRotation')
        
        # cmds.setAttr(curveWarpName+'.twistCurve[2].twistCurve_Position',l=0,cb=1,k=1)
        # cmds.addAttr(polyName,ln = 'twistPositionY', min=0,max=100,at='long',dv=50,k=1)
        # cmds.expression( s= curveWarpName+'.twistCurve[1].twistCurve_Value ='+ polyName +'.twistPositionY*0.01' )
        # cmds.expression( s= curveWarpName+'.twistCurve[2].twistCurve_Value ='+ polyName +'.twistPositionY*0.01' )
        ldCurveWarpMovePivotToCurve0()
        cmds.parent(polyName,groupName)

def ldCurveWarp_ribbonGen():
    sel = ld.ls("curve")
    # if sel == None:
    #     ld.msg("Select Curve Please!")
    #     return
        
    groupName = cmds.group(n="ribbonMeshGroup#",em=1)
    for i in sel:
        polyCreateName = cmds.polyPlane(sx=2,sy=10)
        polyName = polyCreateName[0]
        polyPlaneName = polyCreateName[1]
        curveLength = cmds.arclen(i)
        curveWarpName = cmds.createCurveWarp(polyName,i)
        
        # default value for polyPlane
        cmds.setAttr(curveWarpName+'.alignmentMode',4) #align z
        cmds.setAttr(polyPlaneName+'.height',curveLength) #max length
        
        sliderList = ldCurveWarp_getSliderList()
        attrAddList = sliderList['attrName'] 
        fieldMinValue = sliderList['fieldMinValue']
        fieldMaxValue = sliderList['fieldMaxValue']
        precision     = sliderList['precision']
        defaultValue  = sliderList['value']
         
        for index in range(8):
            attributeType = 'long' if precision[index] == 0 else 'double'
            cmds.addAttr(polyName,ln = attrAddList[index], min = fieldMinValue[index], max = fieldMaxValue[index], at =attributeType, dv = defaultValue[index], k=1)

        cmds.connectAttr(polyName+'.flip',curveWarpName+'.flipAxis')
        cmds.connectAttr(polyName+'.widthScale',curveWarpName+'.maxScale')
        cmds.connectAttr(polyName+'.lengthScale',curveWarpName+'.lengthScale')  
        cmds.connectAttr(polyName+'.offset',curveWarpName+'.offset')      
        cmds.connectAttr(polyName+'.rotation',curveWarpName+'.rotation')
        cmds.connectAttr(polyName+'.twistRotation',curveWarpName+'.twistRotation')
        
        cmds.setAttr(curveWarpName+'.twistCurve[0].twistCurve_Value',0)
        cmds.setAttr(curveWarpName+'.twistCurve[3].twistCurve_Value',1)
        
        polyPlaneSubdivLength = polyPlaneName+'.subdivisionsHeight'
        polyPlaneSubdivWidth = polyPlaneName+'.subdivisionsWidth'
        polySubdivLength = polyName+'.subdivLength'
        polySubdivWidth = polyName+'.subdivWidth'
        
        cmds.scriptJob(ro=0, ac=[polySubdivLength, 'ldCurveWarp_setAttr("'+ polyPlaneSubdivLength+'","' + polySubdivLength +'")'])
        cmds.scriptJob(ro=0, ac=[polySubdivWidth , 'ldCurveWarp_setAttr("'+ polyPlaneSubdivWidth +'","' + polySubdivWidth  +'")'])
        
        ldCurveWarp_scriptJob_subdivLength = 'cmds.scriptJob(ro=0, ac=["'+polySubdivLength+'", \'ldCurveWarp_setAttr("' + polyPlaneSubdivLength +'","'+ polySubdivLength +'")\'])'
        ldCurveWarp_scriptJob_subdivWidth  = 'cmds.scriptJob(ro=0, ac=["'+polySubdivWidth+'",  \'ldCurveWarp_setAttr("' + polyPlaneSubdivWidth +'","' + polySubdivWidth + '")\'])'

        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_subdivLength , n="ldCurveWarpScriptNode#", stp="python")
        cmds.scriptNode(st=2, bs=ldCurveWarp_scriptJob_subdivWidth , n="ldCurveWarpScriptNode#", stp="python")

        ldCurveWarp_movePivotToCurve0()
        cmds.parent(polyName,groupName)
    
def ldCurveWarp_setAttr(attr,channel):
    cmds.setAttr(attr,cmds.getAttr(channel))