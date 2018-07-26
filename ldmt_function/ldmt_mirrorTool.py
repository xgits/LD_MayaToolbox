import os
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
    
LDMTPATH = ld.getPath('LDMT')
ldmt_mirrorTool_uifile = LDMTPATH + '/ldmt_ui/ldmt_mirrorTool.ui'
ldmt_mirrorTool_list_form, ldmt_mirrorTool_list_base = load_ui_type(ldmt_mirrorTool_uifile)
ldmt_window_name = 'ldmt_mirrorTool'
ldmt_button_name = 'btn_'+ldmt_window_name.split('_')[1]

'''
#UI
'''
class ldmt_cls(ldmt_mirrorTool_list_form, ldmt_mirrorTool_list_base):
    def __init__(self, parent = get_maya_window()):
        super(ldmt_cls, self).__init__(parent)
        self.window_name = 'ldmt_mirrorTool'
        self.setupUi(self)
        self.move(QCursor.pos() + QPoint(20,20))
        # update status bar so it's not only show in help line window.
        self.setupBtn()
        self.setupBtnStyle()
        self.statusBar_mirrorTool.showMessage(ld.tag())
        self.installStartBar()
        
    def setupBtnStyle(self):
        self.checkBox_reverse.setVisible(0)
        
    def setupBtn(self):
        self.btn_mirror.clicked.connect(self.ldmt_mirror)
        self.checkBox_local.stateChanged.connect(self.setReverse)
        
    def setReverse(self):
        if self.checkBox_local.checkState():
            self.checkBox_reverse.setVisible(1)
        else:
            self.checkBox_reverse.setVisible(0)

    def ldmt_mirror(self):
        cmds.undoInfo(ock = 1)
        # exec mirror function
        mirrored = cmds.polyMirrorFace(n="polyMirrorFace#")
        # prepare all attribute name
        mirrored_axis = mirrored[0]+".axis"
        mirrored_mirrorAxis = mirrored[0]+".mirrorAxis"
        mirrored_axisDirection = mirrored[0]+".axisDirection"
        mirrored_mergeThreshold = mirrored[0]+".mergeThreshold"
        mirrored_cutMesh = mirrored[0]+".cutMesh"
        # get current value
        if self.radioButton_x.isChecked():
            targetAxis = 0
        elif self.radioButton_y.isChecked():
            targetAxis = 1
        elif self.radioButton_z.isChecked():
            targetAxis = 2
        if self.checkBox_weld.isChecked():
            ifCutmesh = 0
        else:
            ifCutmesh = 1
        if self.checkBox_reverse.isChecked():
            ifReverse = 0
        else:
            ifReverse = 1
        if self.checkBox_local.isChecked():
            mirrorAxis = 0
        else:
            mirrorAxis = 2
        cmds.setAttr(mirrored_axis, targetAxis)
        cmds.setAttr(mirrored_cutMesh, ifCutmesh)
        cmds.setAttr(mirrored_mirrorAxis, mirrorAxis)
        cmds.setAttr(mirrored_axisDirection, ifReverse)
        cmds.setAttr(mirrored_mergeThreshold, 0.2)
        cmds.undoInfo(cck = True)

    def installStartBar(self):
        allQWidgets = self.findChildren(QWidget)
        for i in allQWidgets:
            i.installEventFilter(self)

    def eventFilter(self, obj, event ):
        '''Connect signals on mouse over''' 
        if event.type() == QEvent.Enter:
            self.oldMessage = ld.tag()
            self.statusBar_mirrorTool.showMessage(' '+obj.statusTip(),0) 
        elif event.type() == QEvent.Leave:
            self.statusBar_mirrorTool.showMessage(' '+self.oldMessage, 0)
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



    