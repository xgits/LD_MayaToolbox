import maya.cmds as cmds
def cleanProcedure():
    cmds.undoInfo(ock=1)
    sel = cmds.ls(sl=1)
    selRelatives = cmds.listRelatives(sel)
    if selRelatives[0].startswith('instanceAlongCurveLocator'):
        selectedLocator = []
        selectedLocator=cmds.ls(sl=1)
        tempGroupName = ""
        tempGroupName=str(cmds.group(em=1, n='InstanceMesh'))
        selectedMesh = []
        selectedMeshDuplicatedShape = []
        selectedThings = []
        cmds.select(selectedLocator)
        selectedThings=cmds.listRelatives(c=1)
        selectedMesh=cmds.filterExpand(sm=12)
        cmds.select(selectedMesh)
        selectedMeshDuplicatedShape=cmds.listRelatives(c=1)
        eachOverride=selectedMeshDuplicatedShape[0] + ".overrideEnabled"
        cmds.setAttr(eachOverride, 1)
        selectedMeshDuplicated=cmds.duplicate()
        cmds.parent(selectedMeshDuplicated, tempGroupName)
        cmds.ungroup(tempGroupName)
        cmds.delete(selectedLocator)
        cmds.select(selectedMeshDuplicated)
        cmds.polyUnite(centerPivot=1, ch=1, mergeUVSets=1)
        separatedMesh = []
        separatedMesh=cmds.polySeparate(ch=1)
        cmds.CenterPivot()
        separatedMeshGroup=cmds.listRelatives(separatedMesh, p=1)
        cmds.select(separatedMeshGroup)
        cmds.select(selectedMeshDuplicated, add=1)
        cmds.ungroup()
        cmds.DeleteHistory()
        resultAll = cmds.ls(sl=1,o=1)
        result = cmds.filterExpand(resultAll,sm=12)
        toDelete = list(set(resultAll).difference(set(result)))
        cmds.delete(toDelete)

    else:
        try:
            selectedForClean=cmds.ls(sl=1)
            cmds.polyCube(sz=1, sy=1, sx=1, d=1, cuv=4, h=1, ch=1, w=1, ax=(0, 1, 0))
            temp_polyCube=cmds.ls(sl=1)
            cmds.select(selectedForClean)
            cmds.select(temp_polyCube, add=1)
            cmds.CombinePolygons()
            temp_BeforeSeparate=cmds.ls(sl=1)
            cmds.SeparatePolygon()
            temp_AfterSeparate=cmds.ls(sl=1)
            cmds.delete(temp_AfterSeparate[- 1])
            cmds.DeleteHistory()
            temp_father=cmds.listRelatives(temp_AfterSeparate[0], p=1)
            cmds.select(temp_BeforeSeparate)
            cmds.ungroup()
            cmds.delete(selectedForClean)
            cmds.CombinePolygons()
            cmds.DeleteHistory()
        except:
            pass
    cmds.undoInfo(cck=1)