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
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_clothTransfer.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_clothTransfer'
ldmt_button_name = 'btn_'+ldmt_window_name.split('_')[1]

'''
#Functions
'''

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
        self.statusbar.showMessage(ld.tag())
        self.installStartBar()
        
    def setupBtn(self):
        self.btn_setCloth.clicked.connect(self.setCloth)
        self.btn_setOrigin.clicked.connect(self.setOrigin)
        self.btn_setTarget.clicked.connect(self.setTarget)
        self.btn_selectCloth.clicked.connect(self.selectCloth)
        self.btn_selectOrigin.clicked.connect(self.selectOrigin)
        self.btn_selectTarget.clicked.connect(self.selectTarget)

        self.btn_transfer.clicked.connect(self.transfer)

    def setCloth(self):
        sel = cmds.ls(sl=1,o=1)
        sel = sel[0]
        if sel != []:
            self.btn_selectCloth.setText(str(sel))
        else:
            self.btn_selectCloth.setText('...')
    def setOrigin(self):
        sel = cmds.ls(sl=1,o=1)
        sel = sel[0]
        if sel != []:
            self.btn_selectOrigin.setText(str(sel))
        else:
            self.btn_selectOrigin.setText('...')
    def setTarget(self):
        sel = cmds.ls(sl=1,o=1)
        sel = sel[0]
        if sel != []:
            self.btn_selectTarget.setText(str(sel))
        else:
            self.btn_selectTarget.setText('...')
    def selectSetObjects(self,sel):
        if sel != '...':
            cmds.select(sel,r=1)
        else:
            ld.msg('Nothing selected')
    def selectCloth(self):
        sel = self.btn_selectCloth.text()
        self.selectSetObjects(sel)
    def selectOrigin(self):
        sel = self.btn_selectOrigin.text()
        self.selectSetObjects(sel)
    def selectTarget(self):
        sel = self.btn_selectTarget.text()
        self.selectSetObjects(sel)
    def transfer(self):
        cloth = self.btn_selectCloth.text()
        origin = self.btn_selectOrigin.text()
        target = self.btn_selectTarget.text()
        cmds.makeIdentity(target,apply=True, t=1, r=1, s=1, n=0)
        cmds.select(cloth,r=1)
        cmds.select(origin,add=1)
        mel.eval('DeleteHistory;')
        mel.eval('CreateWrap;')
        blendObjs = [target,origin]
        blendName = cmds.blendShape(blendObjs,o='world',n='clothTransfer#')
        cmds.blendShape(blendName,e=1,w=(0,1))

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