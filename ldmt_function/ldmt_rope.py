import os
import math
from ldmt_function.ldmt_loadUIFile import get_maya_window, load_ui_type
import maya.OpenMayaUI as omui
from ldmt_core import ldmt_cmds as ld
from functools import partial
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

import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import random
import ast

LDMTPATH = ld.getPath('LDMT')
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_rope.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_rope'
ldmt_button_name = 'btn_'+ldmt_window_name.split('_')[1]

'''
#UI
'''
class ldmt_cls(ldmt_list_form, ldmt_list_base):
    def __init__(self, parent = get_maya_window()):
        super(ldmt_cls, self).__init__(parent)
        self.window_name = ldmt_window_name
        self.setupUi(self)
        self.move(QCursor.pos() + QPoint(20,20))
        # update status bar so it's not only show in help line window.
        self.setupBtn()
        self.text_strandsCount.setText('2')
        self.statusbar.showMessage(ld.tag())
        self.installStartBar()
        
    def setupBtn(self):
        self.btn_generate.clicked.connect(self.generate)
        
    def generate(self):
        cmds.undoInfo(ock = 1)
        try:
            count = int(self.text_strandsCount.text())
        except:
            ld.msg("Input count is not valid!")
        if self.btn_normalRope.isChecked():
            self.generateNormalRope(count)
        else:
            self.generateHelixRope(count)
        cmds.undoInfo(cck = 1)

    def spiralGen(self):
        from ldmt_function import ldmt_spiralGen
        ldmt_spiralGen.spiralGen()
        
    def tubeGen(self):
        from ldmt_function import ldmt_tubeGen
        from ldmt_function import ldmt_fixReverse
        sel = cmds.ls(sl=1)
        returnList = ldmt_tubeGen.tubeGen(sel[0])
        return returnList

    def generateNormalRope(self,count):
        from ldmt_function import ldmt_fixReverse
        ldmt_plugin_path = ld.getPath('LDMT') + '/ldmt_plugin'
        pluginPath = ldmt_plugin_path + "/curve2spiral.py"
        if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
            cmds.loadPlugin (pluginPath)
        selectedCurve=cmds.ls(sl=1)
        selectedCurve=cmds.filterExpand(selectedCurve,sm=9)
        for i in range(len(selectedCurve)):
            ropeWidthControl       = selectedCurve[i] + ".ropeWidth"
            densityControl         = selectedCurve[i] + ".ropeDensity"
            lengthDivisionsControl = selectedCurve[i] + ".lengthDivisions"
            widthDivisionsControl  = selectedCurve[i] + ".widthDivisions"
            widthControl           = selectedCurve[i] + ".width"
            taperControl           = selectedCurve[i] + ".taper"
            reverseControl         = selectedCurve[i] + ".reverse"
            # if used delete attributes
            if cmds.attributeQuery("ropeWidth", node = selectedCurve[i],ex=1):
                try:
                    cmds.deleteAttr(ropeWidthControl)
                    cmds.deleteAttr(densityControl)
                    cmds.deleteAttr(lengthDivisionsControl)
                    cmds.deleteAttr(widthDivisionsControl)
                    cmds.deleteAttr(widthControl)
                    cmds.deleteAttr(taperControl)
                    cmds.deleteAttr(reverseControl)
                except:
                    pass
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
                tubes=cmds.ls(sl=1)
                tube=tubes[0]
                node_radius = node + ".radius"
                tube_LengthDiv= tube + ".lengthDivisions"
                tube_WidthDiv= tube + ".widthDivisions"
                tube_Width= tube + ".width"
                tube_Taper= tube + ".taper"
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
        ldmt_fixReverse.fixReverse()

        #rename
        for i in selectedCurve:
            cmds.rename(i ,'NormalRope_'+str(count)+'Strand_#')


    def generateHelixRope(self,count):
        from ldmt_function import ldmt_fixReverse
        pluginPath ="curveWarp"
        if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
            cmds.loadPlugin (pluginPath)
        ropeAngle=float(360 / count)
        selectedCurve = cmds.ls(sl=1)
        curve_count = len(selectedCurve)
        for i in range(curve_count):
            ropeWidthControl       = selectedCurve[i] + ".ropeWidth"
            densityControl         = selectedCurve[i] + ".ropeDensity"
            lengthDivisionsControl = selectedCurve[i] + ".lengthDivisions"
            widthDivisionsControl  = selectedCurve[i] + ".widthDivisions"
            widthControl           = selectedCurve[i] + ".width"
            taperControl           = selectedCurve[i] + ".taper"
            reverseControl         = selectedCurve[i] + ".reverse"
            # if used delete attributes
            if cmds.attributeQuery("ropeWidth", node = selectedCurve[i],ex=1):
                try:
                    cmds.deleteAttr(ropeWidthControl)
                    cmds.deleteAttr(densityControl)
                    cmds.deleteAttr(lengthDivisionsControl)
                    cmds.deleteAttr(widthDivisionsControl)
                    cmds.deleteAttr(widthControl)
                    cmds.deleteAttr(reverseControl)
                    cmds.deleteAttr(taperControl)
                except:
                    pass
            # get main curve shape
            shapes=cmds.listRelatives(selectedCurve[i], children=1)
            shape=shapes[0]
            # set main curve attirubtes
            cmds.addAttr(selectedCurve[i], ln="ropeWidth", h=0, k=1, at='double', dv=0.8)
            cmds.addAttr(selectedCurve[i], min=0, ln="ropeDensity", h=0, k=1, at='double', dv=10)
            cmds.addAttr(selectedCurve[i], min=3, ln="lengthDivisions", h=0, k=1, at='long', dv=20)
            cmds.addAttr(selectedCurve[i], min=3, ln="widthDivisions", h=0, k=1, at='long', dv=18)
            cmds.addAttr(selectedCurve[i], min=0.01, ln="width", h=0, k=1, at='double', dv=4)
            cmds.addAttr(selectedCurve[i], min=0, max=1, ln="reverse", h=0, k=1, at='long', dv=0)
            
            curve0 = selectedCurve[i]
            arclength = float(cmds.arclen(curve0))
            for i_count in range(count):
                rotationAngle=float(i_count * ropeAngle)
                helix = cmds.polyHelix(cuv=3, c=10, ch=1, d=1, h=arclength, rcp=0, sco=50, r=0.4, w=2, sc=1, ax=(0, 1, 0), sa=8)
                helix0 = helix[0]
                helix1 = helix[1]
                cmds.select(curve0, add=1)
                curvewrapname=str(cmds.createCurveWarp())
                curvewraprotation=curvewrapname + ".rotation"
                helixheight= helix1 + ".height"
                cmds.setAttr(helixheight, lock=1)
                cmds.setAttr(curvewraprotation, rotationAngle)

                helixWidth = helix1 + '.width'
                helixCoils = helix1 + '.coils'
                helixRadius = helix1 + '.radius'
                helixSubdivAxis = helix1 + '.subdivisionsAxis'
                helixSubdivCoil = helix1 + '.subdivisionsCoil'
                helixReverse = curvewrapname + '.flipAxis'

                cmds.expression(s=(helixRadius+ "=" + ropeWidthControl))
                cmds.expression(s=(helixReverse + "=" + reverseControl))
                cmds.expression(s=(helixCoils + "=" + densityControl))
                cmds.expression(s=(helixSubdivCoil + "=" + lengthDivisionsControl))
                cmds.expression(s=(helixSubdivAxis + "=" + widthDivisionsControl))
                cmds.expression(s=(helixWidth + "=" + widthControl))

                cmds.parent(helix0, selectedCurve[i])

        cmds.select(selectedCurve,r=1)
        ldmt_fixReverse.fixReverse()
        #rename
        for i in selectedCurve:
            cmds.rename(i ,'HelixRope_'+str(count)+'Strand_#')
    def installStartBar(self):
        allQWidgets = self.findChildren(QWidget)
        for i in allQWidgets:
            i.installEventFilter(self)

    def eventFilter(self, obj, event ):
        '''Connect signals on mouse over''' 
        if event.type() == QEvent.Enter:
            self.oldMessage = ld.tag()
            self.statusbar.showMessage(' '+obj.statusTip(),0) 
        elif event.type() == QEvent.Leave:
            self.statusbar.showMessage(' '+self.oldMessage, 0)
            pass 
            event.accept()
        return False 

    def closeEvent(self,event):
        ld.turnToolBtnOff(self,ldmt_button_name)
        cmds.deleteUI(ldmt_window_name)

def ldmt_show():
    if cmds.window(ldmt_window_name,ex=1):
        if cmds.window(ldmt_window_name,q=1,vis=1):
            cmds.window(ldmt_window_name,e=1,vis=0)
        else:
            cmds.window(ldmt_window_name,e=1,vis=1)
    else:
        ui = ldmt_cls()
        ui.show()


if __name__ == '__main__':
    ldmt_show()