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
    
LDMTPATH = ld.getPath('LDMT')
ldmt_flattenTool_uifile = LDMTPATH + '/ldmt_ui/ldmt_flattenTool.ui'
ldmt_flattenTool_list_form, ldmt_flattenTool_list_base = load_ui_type(ldmt_flattenTool_uifile)
ldmt_window_name = 'ldmt_flattenTool'
ldmt_button_name = 'btn_'+ldmt_window_name.split('_')[1]

'''
#UI
'''
class ldmt_cls(ldmt_flattenTool_list_form, ldmt_flattenTool_list_base):
    def __init__(self, parent = get_maya_window()):
        super(ldmt_cls, self).__init__(parent)
        self.window_name = 'ldmt_flattenTool'
        self.setupUi(self)
        self.move(QCursor.pos() + QPoint(20,20))
        # update status bar so it's not only show in help line window.
        self.setupBtn()
        self.statusBar_flattenTool.showMessage(ld.tag())
        self.installStartBar()
        
    def setupBtn(self):
        self.btn_x.clicked.connect(partial(self.ldmt_flatten,'x'))
        self.btn_y.clicked.connect(partial(self.ldmt_flatten,'y'))
        self.btn_z.clicked.connect(partial(self.ldmt_flatten,'z'))
        self.btn_average.clicked.connect(partial(self.ldmt_flatten,'average'))

    def ldmt_flatten(self,direction):
        cmds.undoInfo(ock = 1)
        cmds.setToolTo( 'Move' )
        cmds.manipMoveContext('Move',e=1,mode=10)
        pivotPositionArray = cmds.manipMoveContext('Move',q=1,p=1 )
        pivotPosition = (pivotPositionArray[0],pivotPositionArray[1],pivotPositionArray[2])
        orientAxesArray = cmds.manipMoveContext('Move',q=1,oa=1 )
        orientAxes = (math.degrees(orientAxesArray[0]),math.degrees(orientAxesArray[1]),math.degrees(orientAxesArray[2]))
        cmds.manipMoveContext('Move',e=1,mode=2)

        if direction == 'x':
            cmds.scale(1e-05,1,1,ws=1,r=1,p=pivotPosition)
        elif direction == 'y':
            cmds.scale(1,1e-05,1,ws=1,r=1,p=pivotPosition)
        elif direction == 'z':
            cmds.scale(1,1,1e-05,ws=1,r=1,p=pivotPosition)
        elif direction == 'average':
            cmds.scale(1e-05,1,1,oa=orientAxes,r=1,p=pivotPosition)
            cmds.manipMoveContext('Move',e=1,mode=10)
        cmds.undoInfo(cck = True)

    def installStartBar(self):
        allQWidgets = self.findChildren(QWidget)
        for i in allQWidgets:
            i.installEventFilter(self)

    def eventFilter(self, obj, event ):
        '''Connect signals on mouse over''' 
        if event.type() == QEvent.Enter:
            self.oldMessage = ld.tag()
            self.statusBar_flattenTool.showMessage(' '+obj.statusTip(),0) 
        elif event.type() == QEvent.Leave:
            self.statusBar_flattenTool.showMessage(' '+self.oldMessage, 0)
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



    