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
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_customGrouper.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_customGrouper'
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
        self.btn_depthGroupR.clicked.connect(self.depthGroupR)
        self.btn_depthGroupA.clicked.connect(self.depthGroupA)
        self.btn_randomGroup.clicked.connect(self.randomGroup)
        self.text_groupCount.setText('5')
    def getGroupCount(self):
        groupCount = self.text_groupCount.text()
        try:
            if int(groupCount)>=1:
                return int(groupCount)
        except:
            ld.msg('Please input a integer!')
            return 0
    def depthGroupR(self):
        cmds.undoInfo(ock = 1)
        sel = cmds.ls(sl=1,fl=1)
        groupCount = self.getGroupCount()
        groups = []
        start = 0
        currentCount = len(sel)
        stop = int(currentCount/groupCount)
        if groupCount == 0:
            return
        else: 
            sel = self.shuffleByDepth(sel)
            group_objs = []
            currentGroupCount = groupCount
            for i in range(groupCount):
                group_objs = sel[start:stop]
                tempGroup = cmds.group(group_objs,n='randomGroup#')
                groups.append(tempGroup)
                currentCount = currentCount-(stop-start)
                start = stop
                currentGroupCount = currentGroupCount-1
                if currentGroupCount == 0:
                    break
                else:
                    stop = stop + int(currentCount/currentGroupCount)

        mainGroup = cmds.group(groups,n='randomMainGroup#')
        childGroups = cmds.listRelatives(mainGroup)
            
        for level1 in range(len(childGroups)):
            children = cmds.listRelatives(childGroups[level1])
            for level2 in range(len(childGroups)):
                jumpHardness = abs(level1-level2)
                randomBar = 0.5**(jumpHardness+1)
                if jumpHardness == 0:
                    continue
                else:
                    for child in children:
                        if random.random() < randomBar:
                            cmds.parent(child,childGroups[level2])
        cmds.select(mainGroup,r=1)
        cmds.undoInfo(cck = 1)

    def depthGroupA(self):
        cmds.undoInfo(ock = 1)
        sel = cmds.ls(sl=1,fl=1)
        groupCount = self.getGroupCount()
        groups = []
        start = 0
        currentCount = len(sel)
        stop = int(currentCount/groupCount)
        if groupCount == 0:
            return
        else:
            sel = self.shuffleByDepth(sel)
            group_objs = []
            currentGroupCount = groupCount
            for i in range(groupCount):
                group_objs = sel[start:stop]
                tempGroup = cmds.group(group_objs,n='randomGroup#')
                groups.append(tempGroup)
                currentCount = currentCount-(stop-start)
                start = stop
                currentGroupCount = currentGroupCount-1
                if currentGroupCount == 0:
                    break
                else:
                    stop = stop + int(currentCount/currentGroupCount)
        mainGroup = cmds.group(groups,n='randomMainGroup#')
        cmds.undoInfo(cck = 1)
    def randomGroup(self):
        cmds.undoInfo(ock = 1)
        sel = cmds.ls(sl=1,fl=1)
        groupCount = self.getGroupCount()
        groups = []
        start = 0
        currentCount = len(sel)
        stop = int(currentCount/groupCount)
        if groupCount == 0:
            return
        else:
            random.shuffle(sel)
            group_objs = []
            currentGroupCount = groupCount
            for i in range(groupCount):
                group_objs = sel[start:stop]
                tempGroup = cmds.group(group_objs,n='randomGroup#')
                groups.append(tempGroup)
                currentCount = currentCount-(stop-start)
                start = stop
                currentGroupCount = currentGroupCount-1
                if currentGroupCount == 0:
                    break
                else:
                    stop = stop + int(currentCount/currentGroupCount)   
        mainGroup = cmds.group(groups,n='randomMainGroup#')
        cmds.undoInfo(cck = 1)

    def shuffleByDepth(self, sel):
        sel_depth = {}
        for i in sel:
            bb = cmds.polyEvaluate(i,b=1)
            sel_depth[i] = bb[2][1]

        sel_depth_sorted = sorted(sel_depth.iteritems(), key=lambda d:d[1])
        newSel = []
        for i in sel_depth_sorted:
            newSel.append(i[0])
        return newSel

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