import maya.cmds as cmds
import maya.mel as mel
from ldmt_function import ldmt_tubeGen
from ldmt_function import ldmt_fixReverse

def braidGen():
    allSel=cmds.ls(sl=1)
    for eachCurve in allSel:
        cmds.select(eachCurve)
        mel.eval('makeCurvesDynamic 2 { "1", "1", "1", "1", "0"}')
        #First Step nHair - Make Curves Dynamic
        follicle=cmds.listConnections(eachCurve)
        follicleShape=cmds.listRelatives(follicle[0], shapes=1)
        follicleBraid=follicleShape[0] + ".braid"
        follicleSampleDensity=follicleShape[0] + ".sampleDensity"
        cmds.setAttr(follicleBraid, 1)
        # Set Braid to be TRUE
        cmds.setAttr(follicleSampleDensity, 100)
        # Set SampleDensity to be smoother
        cmds.select(eachCurve)
        #print $follicleShape;
        hairSystem=cmds.listConnections(follicleShape[0], type='hairSystem')
        hairSystemShape=cmds.listRelatives(hairSystem[0], type='hairSystem')
        #string $hairSystemShape[] = `ls -type hairSystem`;
        for i in range(0,len(hairSystemShape)):
            if i != 0:
                hairSystemShape.pop(i)
        mainGroup=eachCurve + "_HairSystemGrp"
        #print $hairSystemShape;
        cmds.group(hairSystemShape[0], n=mainGroup)
        NucleusList=cmds.listConnections(hairSystemShape[0], type='nucleus')
        thisNucleus=NucleusList[0]
        cmds.parent(thisNucleus, mainGroup)
        cmds.select(eachCurve)
        hairSystemShapeLastNum=len(hairSystemShape)
        hairSystemShapeClumpCount=hairSystemShape[hairSystemShapeLastNum - 1] + ".hairsPerClump"
        hairSystemShapeClumpWidth=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidth"
        hairSystemShapeClumpTaper=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[1].clumpWidthScale_FloatValue"
        hairSystemShapeClumpFlatness=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpFlatness[0].clumpFlatness_FloatValue"
        hairSystemShapeClumpCount=hairSystemShape[hairSystemShapeLastNum - 1] + ".hairsPerClump"
        ClumpWidthScale_pos1=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[0].clumpWidthScale_Position"
        ClumpWidthScale_val1=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[0].clumpWidthScale_FloatValue"
        ClumpWidthScale_pos2=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[1].clumpWidthScale_Position"
        ClumpWidthScale_val2=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[1].clumpWidthScale_FloatValue"
        ClumpWidthScale_pos3=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[2].clumpWidthScale_Position"
        ClumpWidthScale_val3=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[2].clumpWidthScale_FloatValue"
        ClumpWidthScale_pos4=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[3].clumpWidthScale_Position"
        ClumpWidthScale_val4=hairSystemShape[hairSystemShapeLastNum - 1] + ".clumpWidthScale[3].clumpWidthScale_FloatValue"
        cmds.setAttr(ClumpWidthScale_pos1, 0)
        cmds.setAttr(ClumpWidthScale_val1, 0)
        cmds.setAttr(ClumpWidthScale_pos2, 0.001)
        cmds.setAttr(ClumpWidthScale_val2, 1)
        cmds.setAttr(ClumpWidthScale_pos3, 0.999)
        cmds.setAttr(ClumpWidthScale_val3, 1)
        cmds.setAttr(ClumpWidthScale_pos4, 0.999)
        cmds.setAttr(ClumpWidthScale_val4, 0)
        cmds.setAttr(hairSystemShapeClumpCount, 3)
        cmds.setAttr(hairSystemShapeClumpWidth, 3)
        mel.eval("AssignBrushToHairSystem;")
        pfxHair=cmds.listConnections(hairSystemShape[hairSystemShapeLastNum - 1])
        pfxHair_Size=len(pfxHair)
        pfxHairLast=pfxHair[pfxHair_Size - 1]
        cmds.parent(pfxHairLast, mainGroup)
        cmds.select(pfxHairLast)
        # select last one
        mel.eval("doPaintEffectsToCurve(1);") 
        pfxHairStringCount=len(pfxHairLast)
        pfxHairLastNum=pfxHairLast[7:pfxHairStringCount]
        pfxHairShapeCurves="pfxHairShape" + pfxHairLastNum + "Curves"
        cmds.parent(pfxHairShapeCurves, mainGroup)
        follicleConnectedCurve=cmds.listConnections(follicleShape[0], type='nurbsCurve')
        for originCurve in follicleConnectedCurve:
            objects=cmds.ls(originCurve, l=1)
            parentList = []
            parentList=objects[0].split("|")
            cmds.parent(parentList[1], mainGroup)
            
        cmds.select(pfxHairShapeCurves)
        getList = ldmt_tubeGen.tubeGen(eachCurve)
        Tubes=cmds.ls(sl=1)
        cmds.select(eachCurve)
        Tube0_LengthDiv=Tubes[0] + ".lengthDivisions"
        Tube1_LengthDiv=Tubes[1] + ".lengthDivisions"
        Tube2_LengthDiv=Tubes[2] + ".lengthDivisions"
        Tube0_WidthDiv=Tubes[0] + ".widthDivisions"
        Tube1_WidthDiv=Tubes[1] + ".widthDivisions"
        Tube2_WidthDiv=Tubes[2] + ".widthDivisions"
        Tube0_Width=Tubes[0] + ".width"
        Tube1_Width=Tubes[1] + ".width"
        Tube2_Width=Tubes[2] + ".width"
        Tube0_Taper=Tubes[0] + ".taper"
        Tube1_Taper=Tubes[1] + ".taper"
        Tube2_Taper=Tubes[2] + ".taper"
        lengthDivisionsControl=eachCurve + ".lengthDivisions"
        widthDivisionsControl=eachCurve + ".widthDivisions"
        braidWidthControl=eachCurve + ".braidWidth"
        braidTaperControl=eachCurve + ".braidTaper"
        flatnessControl=eachCurve + ".flatness"
        perbraidWidthControl=eachCurve + ".perbraidWidth"
        perBraidTaperControl=eachCurve + ".perbraidtaper"
        if cmds.attributeQuery("braidWidth", node = eachCurve, ex=1):
            cmds.deleteAttr(lengthDivisionsControl)
            cmds.deleteAttr(widthDivisionsControl)
            cmds.deleteAttr(braidWidthControl)
            cmds.deleteAttr(braidTaperControl)
            cmds.deleteAttr(flatnessControl)
            cmds.deleteAttr(perbraidWidthControl)
            cmds.deleteAttr(perBraidTaperControl)
        cmds.addAttr(eachCurve, min=0, ln="braidWidth", h=0, k=1, at='double', dv=1)
        cmds.addAttr(eachCurve, min=0, ln="braidTaper", h=0, k=1, at='double', dv=1)
        cmds.addAttr(eachCurve, ln="flatness", h=0, k=1, at='double', max=1, dv=0)
        cmds.addAttr(eachCurve, min=0, ln="lengthDivisions", h=0, k=1, at='long', dv=100)
        cmds.addAttr(eachCurve, min=0, ln="widthDivisions", h=0, k=1, at='long', dv=7)
        cmds.addAttr(eachCurve, min=0, ln="perbraidWidth", h=0, k=1, at='double', dv=0.5)
        cmds.addAttr(eachCurve, min=0, ln="perbraidtaper", h=0, k=1, at='double', dv=1)
        cmds.expression(s=(hairSystemShapeClumpWidth + "=" + braidWidthControl))
        cmds.expression(s=(hairSystemShapeClumpTaper + "=" + braidTaperControl))
        cmds.expression(s=(hairSystemShapeClumpFlatness + "=" + flatnessControl))
        cmds.expression(s=(Tube0_LengthDiv + "=" + lengthDivisionsControl))
        cmds.expression(s=(Tube1_LengthDiv + "=" + lengthDivisionsControl))
        cmds.expression(s=(Tube2_LengthDiv + "=" + lengthDivisionsControl))
        cmds.expression(s=(Tube0_WidthDiv + "=" + widthDivisionsControl))
        cmds.expression(s=(Tube1_WidthDiv + "=" + widthDivisionsControl))
        cmds.expression(s=(Tube2_WidthDiv + "=" + widthDivisionsControl))
        cmds.expression(s=(Tube0_Width + "=" + perbraidWidthControl))
        cmds.expression(s=(Tube1_Width + "=" + perbraidWidthControl))
        cmds.expression(s=(Tube2_Width + "=" + perbraidWidthControl))
        cmds.expression(s=(Tube0_Taper + "=" + perBraidTaperControl))
        cmds.expression(s=(Tube1_Taper + "=" + perBraidTaperControl))
        cmds.expression(s=(Tube2_Taper + "=" + perBraidTaperControl))
        cmds.hide(mainGroup)
        cmds.parent(eachCurve,w=1,r=1)
        cmds.parent(mainGroup, eachCurve)
        cmds.parent(getList[0], eachCurve)
        cmds.parent(getList[1], eachCurve)
        cmds.select(Tubes)
        ldmt_fixReverse.fixReverse()
    cmds.select(allSel)
    for i in allSel:
        cmds.rename(i ,'Braid_#')