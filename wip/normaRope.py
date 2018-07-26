def generateNormalRope(self,count):
    ldmt_plugin_path = ld.getPath('LDMT') + '/ldmt_plugin'
    pluginPath = ldmt_plugin_path + "/curve2spiral.py"
    
    if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
        cmds.loadPlugin (pluginPath)
    selectedCurve=cmds.ls(sl=1)

    for i in range(len(selectedCurve)):
        # if used delete attributes
        if cmds.attributeQuery("ropeWidth", node = selectedCurve[i],ex=1):
            cmds.deleteAttr(ropeWidthControl)
            cmds.deleteAttr(densityControl)
            cmds.deleteAttr(lengthDivisionsControl)
            cmds.deleteAttr(widthDivisionsControl)
            cmds.deleteAttr(widthControl)
            cmds.deleteAttr(taperControl)
            cmds.deleteAttr(reverseControl)
        # get main curve shape
        shapes=cmds.listRelatives(selectedCurve[i], children=1)
        shape=shapes[0]
        # set main curve attirubtes
        cmds.addAttr(selectedCurve[i], ln="ropeWidth", h=0, k=1, dv=1, at='double')
        cmds.addAttr(selectedCurve[i], min=0, ln="ropeDensity", h=0, k=1, at='double', dv=50)
        cmds.addAttr(selectedCurve[i], min=3, ln="lengthDivisions", h=0, k=1, at='long', dv=100)
        cmds.addAttr(selectedCurve[i], min=3, ln="widthDivisions", h=0, k=1, at='long', dv=9)
        cmds.addAttr(selectedCurve[i], min=0.01, ln="width", h=0, k=1, at='double', dv=1)
        cmds.addAttr(selectedCurve[i], min=0, ln="taper", h=0, k=1, at='double', dv=1)
        cmds.addAttr(selectedCurve[i], min=0, ln="reverse", h=0, k=1, at='bool', dv=0)
        ropeWidthControl       = selectedCurve[i] + ".ropeWidth"
        densityControl         = selectedCurve[i] + ".ropeDensity"
        lengthDivisionsControl = selectedCurve[i] + ".lengthDivisions"
        widthDivisionsControl  = selectedCurve[i] + ".widthDivisions"
        widthControl           = selectedCurve[i] + ".width"
        taperControl           = selectedCurve[i] + ".taper"
        reverseControl         = selectedCurve[i] + ".reverse"
        
        # loop for each count
        for countIndex in range(count):
            # create spiral first
            node=str(cmds.createNode("curveSpiral"))
            cmds.connectAttr(shape + ".worldSpace", node + ".ic")
            outputNode=str(cmds.createNode("nurbsCurve"))
            cmds.connectAttr(node + ".oc", outputNode + ".create")
            cmds.select(outputNode, node)
            node_Rotation=node + ".rotation"
            cmds.setAttr(node_Rotation, countIndex*360/count) # !important each count's rotation is arraged.
            nodeParent=cmds.listRelatives(outputNode, p=1)
            #Fix Orient Point Issue. You will konw trying without it when you edit the width. :P :P :P
            node_useRadMap=node + ".useRadiusMap"
            node_usePointCount=node + ".usePointCount"
            node_pointCount=node + ".pointCount"
            node_sweep=node + ".sweep"
            cmds.setAttr(node_useRadMap, 1)
            cmds.setAttr(node_usePointCount, 1)
            cmds.setAttr(node_pointCount, 200)
            RadMap_1_Pos=node + ".radiusMap[0].radiusMap_Position"
            RadMap_1_Val=node + ".radiusMap[0].radiusMap_FloatValue"
            RadMap_2_Pos=node + ".radiusMap[1].radiusMap_Position"
            RadMap_2_Val=node + ".radiusMap[1].radiusMap_FloatValue"
            RadMap_3_Pos=node + ".radiusMap[2].radiusMap_Position"
            RadMap_3_Val=node + ".radiusMap[2].radiusMap_FloatValue"
            RadMap_4_Pos=node + ".radiusMap[3].radiusMap_Position"
            RadMap_4_Val=node + ".radiusMap[3].radiusMap_FloatValue"
            cmds.setAttr(RadMap_1_Pos, 0)
            cmds.setAttr(RadMap_1_Val, 0)
            cmds.setAttr(RadMap_2_Pos, 0.01)
            cmds.setAttr(RadMap_2_Val, 1)
            cmds.setAttr(RadMap_3_Pos, 0.99)
            cmds.setAttr(RadMap_3_Val, 1)
            cmds.setAttr(RadMap_4_Pos, 1)
            cmds.setAttr(RadMap_4_Val, 0)
            #With that fix you are good to go.
            #generate tube
            getList=self.tubeGen()
            Tubes=cmds.ls(sl=1)
            Tube=Tubes[0]
            node_radius = node + ".radius"
            tube_LengthDiv=Tubes[0] + ".lengthDivisions"
            tube_WidthDiv=Tubes[0] + ".widthDivisions"
            tube_Width=Tubes[0] + ".width"
            tube_Taper=Tubes[0] + ".taper"
            cmds.expression(s=(node_radius + "=" + ropeWidthControl))
            cmds.expression(s=(node_sweep + "=" + "10" + "*(2*" + reverseControl + "-1)"))
            cmds.expression(s=(node_pointCount + "=" + densityControl))
            cmds.expression(s=(tube_LengthDiv + "=" + lengthDivisionsControl))
            cmds.expression(s=(tube_WidthDiv + "=" + widthDivisionsControl))
            cmds.expression(s=(tube_Width + "=" + widthControl))
            cmds.expression(s=(tube_Taper + "=" + taperControl))
            cmds.parent(getList[0], selectedCurve[i])
            cmds.parent(getList[1], selectedCurve[i])
            cmds.parent(nodeParent[0], selectedCurve[i])
            cmds.hide(nodeParent[0])

        #finally set the default attribute value
        cmds.setAttr(lengthDivisionsControl, 100)
        cmds.setAttr(widthDivisionsControl, 9)
        cmds.setAttr(densityControl, 200)
    cmds.select(selectedCurve,r=1)