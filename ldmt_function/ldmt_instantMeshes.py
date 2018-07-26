import os
import math
import tempfile
from ldmt_function.ldmt_loadUIFile import get_maya_window, load_ui_type
import maya.OpenMayaUI as omui
import subprocess
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
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_instantMeshes.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_instantMeshes'
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
        self.btn_sendToExe.clicked.connect(self.sendToExe)
        self.btn_remesh.clicked.connect(self.remesh)
        self.text_targetCount.setPlainText("50%")
    def sendToExe(self):
        sel=cmds.ls(sl=1,o=1)
        if sel == []:
            InstantMeshPath = LDMTPATH + "/ldmt_exe/instantMesh.exe"
            subprocess.Popen(InstantMeshPath,False)
        else:
            self.instantMeshes_sendToExe()

    def remesh(self):
        targetCount = self.text_targetCount.toPlainText()
        try:
            if targetCount.endswith('%'):
                sel = cmds.ls(sl=1,o=1)
                sel = sel[0]
                currentFaceCount = int(cmds.polyEvaluate(sel, f=True))
                targetCount = 2*int(currentFaceCount*float(targetCount[:-1])/100)
            else:
                targetCount = int(targetCount)
        except:
            ld.msg('Please input a number or ratio!')
            return 
        self.instantMeshes_remesh(targetCount)

    def instantMeshes_sendToExe(self,face_count=None):
        inst_mesh_path = LDMTPATH + "/ldmt_exe/instantMesh.exe"
        if not os.path.exists(inst_mesh_path):
            cmds.warning('Instant Mesh path not found!')
            return
        # Get current selection
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            print 'Processing Instant Mesh...'
            # Create temp file for OBJ export
            temp = tempfile.NamedTemporaryFile(prefix='instantMesh_', suffix='.obj', delete=False)
            temp_path = temp.name
            # Save the currently selected object as an OBJ
            cmds.file(temp_path, force=True, exportSelected=True, type="OBJ")
            # run instamesh command on the OBJ
            print temp_path
            print "Instant Mesh start"
            some_command = inst_mesh_path + " " + temp_path
            p = subprocess.Popen(some_command, False)
            temp.close()
        else:
            cmds.warning('No objects selected...')

    def instantMeshes_remesh(self,face_count=None):
        inst_mesh_path = LDMTPATH + "/ldmt_exe/instantMesh.exe"
        if not os.path.exists(inst_mesh_path):
            cmds.warning('Instant Mesh path not found!')
            return
        # Get current selection
        sel_obj = cmds.ls(sl=True)
        if sel_obj:
            print 'Processing Instant Mesh...'
            # if no polycount set just double the amount of the source object
            if not face_count:
                face_count = int(cmds.polyEvaluate(sel_obj, f=True))
                face_count *= 2
            face_count /= 2
            # Create temp file for OBJ export
            temp = tempfile.NamedTemporaryFile(prefix='instantMesh_', suffix='.obj', delete=False)
            temp_path = temp.name
            # Save the currently selected object as an OBJ
            cmds.file(temp_path, force=True, exportSelected=True, type="OBJ")
            # run instamesh command on the OBJ
            print temp_path
            print "Instant Mesh start"
            some_command = inst_mesh_path + " " + temp_path + " -o " + temp_path + " -f " + str(face_count) + " -D" + " -b"
            p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
            p.communicate()
            p.wait()
            print "Instant Mesh end"
            print some_command
            # import back the temp OBJ file
            returnedNodes = cmds.file(temp_path,
                                    i=True,
                                    type="OBJ",
                                    rnn=True,
                                    ignoreVersion=True,
                                    options="mo=0",
                                    loadReferenceDepth="all")
            # delete the temp file
            temp.close()
            # Select the imported nodes
            if returnedNodes:
                cmds.select(returnedNodes, r=True)
            print 'Instant Mesh done...'
        else:
            cmds.warning('No objects selected...')

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