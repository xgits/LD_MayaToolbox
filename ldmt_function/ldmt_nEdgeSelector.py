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
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_nEdgeSelector.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_nEdgeSelector'
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
        self.statusbar.showMessage(ld.tag())
        self.installStartBar()
        
    def setupBtn(self):
        self.btn_selectByEdgeCount.clicked.connect(self.selectByEdgeCount)
        self.btn_selectByPattern.clicked.connect(self.selectByPattern)
        self.btn_selectOneByOne.clicked.connect(self.selectOneByOne)
        self.text_nCount.setText('2')
    def selectOneByOne(self):
        cmds.undoInfo(ock = 1)
        from ldmt_function import patternSelection
        patternSelection.patternSelection()
        cmds.undoInfo(cck = 1)
    def selectByEdgeCount(self):
        cmds.undoInfo(ock = 1)
        count = self.text_nCount.text()
        if self.btn_edgeLoop.isChecked():
            selectType = 'edgeLoopOrBorder'
        else:
            selectType = 'edgeRing'
        try:
            count = int(count)
            mel.eval("polySelectEdgesEveryN " + selectType + " " +str(count))
        except:
            ld.msg("Count should be an integer!")
        cmds.undoInfo(cck = 1)
    def getEdgeIdIndex(self,edgeId,edgeIds):
        for i in range(len(edgeIds)):
            if edgeId == edgeIds[i]:
                return i
        return -1
    def getEdgeIdFromSelectionString(self,sel):
        tokens = sel.split('[')
        if len(tokens) != 2:
            return -1
        else:
            return int(tokens[1][:-1])
    def selectByPattern(self):
        cmds.undoInfo(ock = 1)
        selectedObject = cmds.ls(sl=1,o=1)
        initialEdgeSelection = cmds.ls(sl=1,fl=1)
        numEdges = len(initialEdgeSelection)
        if numEdges == 0 or numEdges>2:
            return
        firstEdge = initialEdgeSelection[0]
        firstEdgeId = self.getEdgeIdFromSelectionString(firstEdge)
        if numEdges == 1:
            cmds.polySelect(selectedObject[0], edgeLoop = firstEdgeId)
            return
        secondEdge = initialEdgeSelection[1]
        secondEdgeId = self.getEdgeIdFromSelectionString(secondEdge)
        edgeLoopIds = cmds.polySelect(selectedObject[0], edgeLoop = firstEdgeId, noSelection=1)
        firstEdgeIndex = self.getEdgeIdIndex(firstEdgeId, edgeLoopIds)
        if firstEdgeIndex == -1:
            return
        secondEdgeIndex = self.getEdgeIdIndex(secondEdgeId, edgeLoopIds)
        if secondEdgeIndex == -1:
            edgeLoopIds = cmds.polySelect(selectedObject[0], edgeLoop = firstEdgeId, noSelection=1)
            firstEdgeIndex = self.getEdgeIdIndex(firstEdgeId, edgeLoopIds)
            if firstEdgeIndex == -1:
                return
            secondEdgeIndex = self.getEdgeIdIndex(secondEdgeId, edgeLoopIds)
            if secondEdgeIndex == -1:
                return
        numEdgesInLoop = len(edgeLoopIds)
        isFullLoop = edgeLoopIds[0] == edgeLoopIds[numEdgesInLoop-1]
        edgesToSkip = abs(secondEdgeIndex - firstEdgeIndex)
        if isFullLoop and edgesToSkip > (numEdgesInLoop - edgesToSkip -1):
            edgesToSkip = numEdgesInLoop - edgesToSkip - 1
        for i in range(firstEdgeIndex,numEdgesInLoop,edgesToSkip):
            cmds.select(selectedObject[0]+'.e['+str(edgeLoopIds[i])+']', add=1)
        for i in range(0,firstEdgeIndex - edgesToSkip,edgesToSkip):
            cmds.select(selectedObject[0]+'.e['+str(edgeLoopIds[i])+']', add=1)
        cmds.undoInfo(cck = 1)
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