import os
import math
from ldmt_function.ldmt_loadUIFile import get_maya_window, load_ui_type
import maya.OpenMayaUI as omui
from ldmt_core import ldmt_cmds as ld
from functools import partial
import maya.cmds as cmds
import maya.mel as mel
from ldmt_ui import *

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
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_randomSelector.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_randomSelector'
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
        self.btn_randomSelect.clicked.connect(self.randomSelect)
        self.slider_selectRatio.setMinimum(0)
        self.slider_selectRatio.setMaximum(100)
        self.slider_selectRatio.setValue(50)
        self.slider_selectRatio.valueChanged.connect(self.sliderRatioChange)
        self.text_selectRatio.editingFinished.connect(self.textRatioChange)
        self.text_selectRatio.setMaxLength(2)
        self.text_selectRatio.setText('50')

    def sliderRatioChange(self):
        self.text_selectRatio.setText(str(self.slider_selectRatio.value()))
    def textRatioChange(self):
        text = self.text_selectRatio.text()
        for i in text:
            if i not in ['0','1','2','3','4','5','6','7','8','9']:
                self.text_selectRatio.setText('0')
                self.slider_selectRatio.setValue('0')
                return
        if len(text)>2:
            self.text_selectRatio.setText(text[:2])
        self.slider_selectRatio.setValue(int(text))
    def randomSelect(self):
        ratio = self.text_selectRatio.text()
        ratio = float(ratio)/100
        sel = cmds.ls(sl=1,fl=1)
        random.shuffle(sel)
        cmds.select(sel[:int(ratio*len(sel))],r=1)

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