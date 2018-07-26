import sys
import os
import xml.etree.ElementTree as xml
from cStringIO import StringIO
from functools import partial
# Qt is a project by Marcus Ottosson ---> https://github.com/mottosso/Qt.py
from ldmt_core.Qt import QtGui, QtWidgets, QtCore

try:
    import pysideuic
    from shiboken import wrapInstance
except ImportError:
    import pyside2uic as pysideuic
    from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui
from ldmt_core import ldmt_cmds as ld
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

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

from ldmt_ribbonTools import *
from ldmt_function import ldmt_toggleUI
reload(ldmt_toggleUI)
ldmt_function_path = ld.getPath('LDMT') + '/ldmt_function'
ldmt_plugin_path = ld.getPath('LDMT') + '/ldmt_plugin'
maya_version = cmds.about(version=1)

def getUiFile():
    LDMT_LOC = ld.getPath('LDMT')
    LDMT_uiFile = LDMT_LOC + "/ldmt_ui/ldmt_main.ui"
    return LDMT_uiFile
    
def loadUiType(uiFile):
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}
        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtWidgets, widget_class)
    return form_class, base_class

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

def maya_api_version():
    return int(cmds.about(api=True))

def maya_version():
    return float(cmds.about(version=1))
    
class FrameLayout(object):
    def __init__(self, titleBar, frame):
        self.titleBar = titleBar 
        self.frame = frame         
        self.collapse = False       
        self.setSignals()           
 
    def setSignals(self):
        self.titleBar.clicked.connect(self.setCollapse)
 
    def setCollapse(self):
        self.collapse = not self.collapse
        self.frame.setHidden(self.collapse)
        if self.collapse:
            self.titleBar.setArrowType(QtCore.Qt.RightArrow)
            self.titleBar.setStyleSheet('\
            QToolButton {\
                border-style: None;\
                background-style:None;\
                padding-left : 6px;\
                padding-bottom : 1px;\
                color:rgb(25,25,25);}\
            QToolButton:hover{\
                border: 1px solid rgb(120,120,120);\
                border-radius: 6px;\
                background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(15, 15, 15, 125), stop:1 rgba(55,55, 55, 55));\
                padding-left : 6px;\
                padding-bottom : 1px;\
                color:rgb(200,200,200);\
                text-decoration: underline!important;}\
            QToolButton:pressed{\
                background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(55, 55, 55, 175), stop:1 rgba(15,15, 15, 125));\
                }\
            ')
        else:
            self.titleBar.setArrowType(QtCore.Qt.DownArrow)
            self.titleBar.setStyleSheet('\
            padding-left : 6px;\
            padding-bottom : 1px;\
            color:rgb(200,200,200);')
            
class LDMT_mainUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
    MAYA2017 = 201700
    def __init__(self, parent=None):
        self.deleteInstances()  # remove any instance of this window before starting
        super(LDMT_mainUI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        """
		compile the .ui file on loadUiType(), a function that uses pysideuic / pyside2uic to compile .ui files
		"""
        uiFile = getUiFile()
        form_class, base_class = loadUiType(uiFile)
        self.ui = form_class()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupBtn()
        self.setupFrameCollapse()
        self.ui.statusbar.showMessage(ld.tag())
        self.installStartBar()
    '''
        Toolbutton Setup
    '''
    def setupFrameCollapse(self):
        self.frameLayout_basicPanels    = FrameLayout(self.ui.toolButton_basicPanels   , self.ui.frame_basicPanels   )
        self.frameLayout_transformTools = FrameLayout(self.ui.toolButton_transformTools, self.ui.frame_transformTools)
        self.frameLayout_selectTools    = FrameLayout(self.ui.toolButton_selectTools   , self.ui.frame_selectTools   )
        self.frameLayout_generateTools  = FrameLayout(self.ui.toolButton_generateTools , self.ui.frame_generateTools )
        self.frameLayout_UVTools        = FrameLayout(self.ui.toolButton_UVTools       , self.ui.frame_UVTools       )
        self.frameLayout_debugTools     = FrameLayout(self.ui.toolButton_debugTools    , self.ui.frame_debugTools    )
        self.frameLayout_commonPanels   = FrameLayout(self.ui.toolButton_commonPanels  , self.ui.frame_commonPanels  )
        self.frameLayout_fileTools      = FrameLayout(self.ui.toolButton_fileTools     , self.ui.frame_fileTools     )
        self.frameLayout_info           = FrameLayout(self.ui.toolButton_info          , self.ui.frame_info          )
        self.frameLayout_textureTools   = FrameLayout(self.ui.toolButton_textureTools  , self.ui.frame_textureTools  )

    def setCollapse(self, toolButtonClass):
            toolButtonClass.collapse = not toolButtonClass.collapse
            toolButtonClass.frame.setHidden(toolButtonClass.collapse)
            if toolButtonClass.collapse:
                toolButtonClass.titleBar.setArrowType(QtCore.Qt.RightArrow)
            else:
                toolButtonClass.titleBar.setArrowType(QtCore.Qt.DownArrow)

    def toggleToolBtnByMsg(self,message):
        buttonName = message.replace(' ','')
        buttonName = 'btn_'+buttonName[0].lower() + buttonName[1:]
        self.toggleToolBtn(buttonName)

    def toggleToolBtn(self,buttonName):
        windowName = 'ldmt_'+buttonName.split('_')[1]
        exec("buttonObj = self.ui.%s"%(buttonName))
        if cmds.window(windowName,ex=1):
            if cmds.window(windowName,q=1,vis=1):
                buttonObj.setStyleSheet('\
                QPushButton{\
                    border:1px solid rgb(30,30,30);\
                    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(80, 80,80, 235), stop:1 rgba(20, 20, 20, 195));\
                    color:rgb(230,230,230);}\
                QPushButton:hover{\
                    border:1px solid rgb(30,30,30);\
                    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(65, 65, 65, 225), stop:1 rgba(10, 10, 10, 195));\
                    color:rgb(230,230,230);}\
                QPushButton:pressed{ \
                    border:1px solid rgb(30,30,30);\
                    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(40, 40, 40, 195), stop:1 rgba(100, 100,100, 235));\
                    color:rgb(230,230,230);}\
                ')
            else:
                buttonObj.setStyleSheet('\
                QPushButton{\
                    border:1px solid rgb(30,30,30);\
                    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(175, 175,175, 235), stop:1 rgba(235, 235, 235, 195));\
                    color:rgb(25,25,25);}\
                QPushButton:hover{\
                    border:1px solid rgb(30,30,30);\
                    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(190, 190, 190, 225), stop:1 rgba(245, 245, 245, 195));\
                    color:rgb(25,25,25);}\
                QPushButton:pressed{ \
                    border:1px solid rgb(30,30,30);\
                    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(215, 215, 215, 195), stop:1 rgba(155, 155,155, 235));\
                    color:rgb(25,25,25);}\
                ')
        else:
            buttonObj.setStyleSheet('\
            QPushButton{\
                border:1px solid rgb(30,30,30);\
                background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(175, 175,175, 235), stop:1 rgba(235, 235, 235, 195));\
                color:rgb(25,25,25);}\
            QPushButton:hover{\
                border:1px solid rgb(30,30,30);\
                background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(190, 190, 190, 225), stop:1 rgba(245, 245, 245, 195));\
                color:rgb(25,25,25);\
            }\
            QPushButton:pressed{ \
                border:1px solid rgb(30,30,30);\
                background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(215, 215, 215, 195), stop:1 rgba(155, 155,155, 235));\
                color:rgb(25,25,25);}\
            ')
    '''
        Button Setup
    '''
    def setupBtn(self):
        #Menu Dev
        self.ui.actionScriptEditor.triggered.connect(self.ldmt_scriptEditor)
        self.ui.actionMelToPy.triggered.connect(self.ldmt_melToPy)
        #Basic Panel
        self.ui.btn_UV.clicked.connect(partial(self.ldmt_function,"UV"))
        self.ui.btn_shader.clicked.connect(partial(self.ldmt_function,"Shader"))
        self.ui.btn_outliner.clicked.connect(partial(self.ldmt_function,"Outliner"))
        #Transform Tools
        self.ui.btn_mirrorTool.clicked.connect(partial(self.ldmt_function,"Mirror Tool"))
        self.ui.btn_resetPivot.clicked.connect(partial(self.ldmt_function,"Reset Pivot"))
        self.ui.btn_flattenTool.clicked.connect(partial(self.ldmt_function,"Flatten Tool"))
        self.ui.btn_deleteHistory.clicked.connect(partial(self.ldmt_function,"Delete History"))
        self.ui.btn_morphToUV.clicked.connect(partial(self.ldmt_function,"Morph To UV"))
        self.ui.btn_turboSmooth.clicked.connect(partial(self.ldmt_function,"Turbo Smooth"))
        self.ui.btn_circularize.clicked.connect(partial(self.ldmt_function,"Circularize"))
        self.ui.btn_rebuildSubdiv.clicked.connect(partial(self.ldmt_function,"Rebuild Subdiv"))
        self.ui.btn_nanomesh.clicked.connect(partial(self.ldmt_function,"Nanomesh"))
        self.ui.btn_insertMesh.clicked.connect(partial(self.ldmt_function,"Insert Mesh"))
        self.ui.btn_instantMeshes.clicked.connect(partial(self.ldmt_function,"Instant Meshes"))
        self.ui.btn_topoBlendshape.clicked.connect(partial(self.ldmt_function,"Topo Blendshape"))
        self.ui.btn_faceTransfer.clicked.connect(partial(self.ldmt_function,"Face Transfer"))
        self.ui.btn_clothTransfer.clicked.connect(partial(self.ldmt_function,"Cloth Transfer"))
        # Select Tools
        self.ui.btn_hardEdges.clicked.connect(partial(self.ldmt_function,"Select Hard Edges"))
        self.ui.btn_UVBorders.clicked.connect(partial(self.ldmt_function,"Select UV Borders"))
        self.ui.btn_randomSelector.clicked.connect(partial(self.ldmt_function,"Random Selector"))
        self.ui.btn_customGrouper.clicked.connect(partial(self.ldmt_function,"Custom Grouper"))
        self.ui.btn_nEdgeSelector.clicked.connect(partial(self.ldmt_function,"N Edge Selector"))
        self.ui.btn_toggleCamSel.clicked.connect(partial(self.ldmt_function,"Toggle Camera Selection"))
        # Generate Tools
        self.ui.btn_spiral.clicked.connect(partial(self.ldmt_function,"Spiral"))
        self.ui.btn_instance.clicked.connect(partial(self.ldmt_function,"Instance"))
        self.ui.btn_ribbon.clicked.connect(partial(self.ldmt_function,"Ribbon"))
        self.ui.btn_tube.clicked.connect(partial(self.ldmt_function,"Tube"))
        self.ui.btn_seams.clicked.connect(partial(self.ldmt_function,"Seams"))
        self.ui.btn_stitches.clicked.connect(partial(self.ldmt_function,"Stitches"))
        self.ui.btn_rope.clicked.connect(partial(self.ldmt_function,"Rope"))
        self.ui.btn_braid.clicked.connect(partial(self.ldmt_function,"Braid"))
        self.ui.btn_edgeToCurve.clicked.connect(partial(self.ldmt_function,"Edge To Curve"))
        self.ui.btn_ribbonTools.clicked.connect(partial(self.ldmt_function,"Ribbon Tools"))
        self.ui.btn_curveOnMesh.clicked.connect(partial(self.ldmt_function,"Curve On Mesh"))
        self.ui.btn_cleanProcedure.clicked.connect(partial(self.ldmt_function,"Clean Procedure"))
        self.ui.btn_findDescription.clicked.connect(partial(self.ldmt_function,"Find Description"))
        self.ui.btn_alignRibbonUV.clicked.connect(partial(self.ldmt_function,"Align Ribbon UV"))
        # UV Tools
        self.ui.btn_UVDeluxe.clicked.connect(partial(self.ldmt_function,"UV Deluxe"))
        self.ui.btn_overlapUVOut.clicked.connect(partial(self.ldmt_function,"Overlap UV Out"))
        self.ui.btn_overlapUVIn.clicked.connect(partial(self.ldmt_function,"Overlap UV In"))
        self.ui.btn_quickUV.clicked.connect(partial(self.ldmt_function,"Quick UV"))
        self.ui.btn_switchUVSet.clicked.connect(partial(self.ldmt_function,"Switch UV Set"))
        # Debug Tools
        self.ui.btn_scene.clicked.connect(partial(self.ldmt_function,"Scene Optimize"))
        self.ui.btn_cleanM.clicked.connect(partial(self.ldmt_function,"Clean Messh"))
        self.ui.btn_normal.clicked.connect(partial(self.ldmt_function,"Facet Normal"))
        self.ui.btn_keepHS.clicked.connect(partial(self.ldmt_function,"Keep Smooth Group"))
        self.ui.btn_rename.clicked.connect(partial(self.ldmt_function,"Rename Tool"))
        self.ui.btn_cleanN.clicked.connect(partial(self.ldmt_function,"Clean Namespace"))
        self.ui.btn_ungroup.clicked.connect(partial(self.ldmt_function,"Ungroup"))
        self.ui.btn_reverse.clicked.connect(partial(self.ldmt_function,"Reverse By View"))
        # Common Panels
        self.ui.btn_plugin.clicked.connect(partial(self.ldmt_function,"Plugin"))
        self.ui.btn_preference.clicked.connect(partial(self.ldmt_function,"Preference"))
        self.ui.btn_hypergraph.clicked.connect(partial(self.ldmt_function,"HyperGraph"))
        self.ui.btn_node.clicked.connect(partial(self.ldmt_function,"Node"))
        self.ui.btn_namespace.clicked.connect(partial(self.ldmt_function,"Namespace"))
        self.ui.btn_hotkey.clicked.connect(partial(self.ldmt_function,"Hotkey"))
        # File
        self.ui.btn_openFolder.clicked.connect(partial(self.ldmt_function,"Open Current Folder"))
        self.ui.btn_quickExport.clicked.connect(partial(self.ldmt_function,"Quick Export"))
        # Info
        self.ui.btn_addToShelf.clicked.connect(partial(self.ldmt_function,"Add Button To Shelf"))
        self.ui.btn_command.clicked.connect(partial(self.ldmt_function,"Search Command"))
        self.ui.btn_helpManual.clicked.connect(partial(self.ldmt_function,"Help Manual"))
        self.ui.btn_links.clicked.connect(partial(self.ldmt_function,"Links"))
        self.ui.btn_update.clicked.connect(partial(self.ldmt_function,"Update"))

    def installStartBar(self):
        allQWidgets = self.findChildren(QWidget)
        for i in allQWidgets:
            i.installEventFilter(self)

    def eventFilter(self, obj, event ):
        '''Connect signals on mouse over''' 
        if event.type() == QEvent.Enter:
            self.ui.oldMessage = ld.tag()
            self.ui.statusbar.showMessage(' '+obj.statusTip(),0) 
        elif event.type() == QEvent.Leave:
            self.ui.statusbar.showMessage(' '+self.ui.oldMessage, 0)
            pass 
            event.accept()
        return False 

    def closeEvent(self,event):
        ld.turnToolBtnOff(self,ldmt_button_name)
        cmds.deleteUI(ldmt_window_name)

    def ldmt_sourceMel(melPath,command):
        if mel.eval('exists "'+command+'"'):
            mel.eval(command)
        else:
            message = 'source "' + melPath + '"'
            mel.eval(message)
            mel.eval(command)        
    #Menu
    def ldmt_scriptEditor(self):
        mel.eval("ScriptEditor;")
    def ldmt_melToPy(self):
        from ldmt_function import ezMel2Python
        ezMel2Python.ezMel2Python()
    def ldmt_function(self,message):
        cmds.undoInfo(ock = 1)
        # Basic Panels
        if message == "UV":
            ldmt_toggleUI.toggleUI('UV')
        elif message == "Shader":
            ldmt_toggleUI.toggleUI('hypershade')
        elif message == "Outliner": 
            ldmt_toggleUI.toggleUI('outliner')
        # Transform Tools
        elif message == "Mirror Tool":
            from ldmt_function import ldmt_mirrorTool
            reload(ldmt_mirrorTool)
            ldmt_mirrorTool.ldmt_show()
        elif message == "Reset Pivot":
            from ldmt_function import ldmt_resetPivot
            ldmt_resetPivot.resetPivot()
        elif message == "Flatten Tool":
            from ldmt_function import ldmt_flattenTool
            reload(ldmt_flattenTool)
            ldmt_flattenTool.ldmt_show()
        elif message == "Delete History":
            from ldmt_function import ldmt_deleteHistory
            reload(ldmt_deleteHistory)
            ldmt_deleteHistory.deleteHistory()
        elif message == "Morph To UV":
            from ldmt_function import ldmt_morphToUV
            ldmt_morphToUV.runMorph2UV()
        elif message == "Turbo Smooth":
            from ldmt_function import ldmt_turboSmooth
            ldmt_turboSmooth.ldmt_turboSmooth()
        elif message == "Circularize":
            if ld.MAYA_version_float <= 2017:
                if mel.eval('exists "CircularizeVtxCmd"'):
                    mel.eval("CircularizeVtxCmd")
                else:
                    pluginFile = ldmt_function_path + '/CircularizeVtxCmd.py'
                    cmds.loadPlugin(pluginFile)
                    mel.eval("CircularizeVtxCmd")
            else:
                cmds.polyCircularize()
        elif message == "Rebuild Subdiv":
            from ldmt_function import ldmt_rebuildSubdiv
            ldmt_rebuildSubdiv.ldmt_rebuildSubdiv()
        elif message == "Nanomesh":
            from ldmt_function import ldmt_nanomesh
            reload(ldmt_nanomesh)
            ldmt_nanomesh.ldmt_show()
        elif message == "Insert Mesh":
            mods = cmds.getModifiers()
            pluginPath = ldmt_function_path + '/duplicateOverSurface.mll'
            if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
                cmds.loadPlugin (pluginPath)
            if mods==0:
                cmds.duplicateOverSurface(cmds.ls(sl=True, long=True)[0])
            elif mods==4:
                cmds.duplicateOverSurface(cmds.ls(sl=True, long=True)[0],rotation=False)
        elif message == "Instant Meshes":
            from ldmt_function import ldmt_instantMeshes
            reload(ldmt_instantMeshes)
            ldmt_instantMeshes.ldmt_show()
        elif message == "Topo Blendshape":
            import geometryWalker.QT.pickWalker_UI as pickWalker_UI
            pickWalker_UI.pickWalkerUI()
        elif message == "Face Transfer":
            import faceTransfer.ui
            faceTransfer.ui.show()
        elif message == "Cloth Transfer":
            from ldmt_function import ldmt_clothTransfer
            reload(ldmt_clothTransfer)
            ldmt_clothTransfer.ldmt_show()

        # Select Tools
        elif message == "Select Hard Edges":
            from ldmt_function import ldmt_hardEdges
            ldmt_hardEdges.selectHardEdges()
        elif message == "Select UV Borders":
            from ldmt_function import ldmt_UVBorders
            ldmt_UVBorders.selectUVEdgeBorders()
        elif message == "Random Selector":
            from ldmt_function import ldmt_randomSelector
            reload(ldmt_randomSelector)
            ldmt_randomSelector.ldmt_show()
        elif message == "Custom Grouper":
            from ldmt_function import ldmt_customGrouper
            reload(ldmt_customGrouper)
            ldmt_customGrouper.ldmt_show()
        elif message == "N Edge Selector":
            from ldmt_function import ldmt_nEdgeSelector
            reload(ldmt_nEdgeSelector)
            ldmt_nEdgeSelector.ldmt_show()
        elif message == "Toggle Camera Selection":
            if self.ui.btn_toggleCamSel.text() == "Turn Cam Sel On":
                cmds.selectPref(useDepth=1)
                self.ui.btn_toggleCamSel.setText("Turn Cam Sel Off")
            else:
                cmds.selectPref(useDepth=0)
                self.ui.btn_toggleCamSel.setText("Turn Cam Sel On")
        # Generate Tools
        elif message == "Spiral":
            from ldmt_function import ldmt_spiralGen
            reload(ldmt_spiralGen)
            ldmt_spiralGen.spiralGen()
        elif message == "Instance":
            from ldmt_function import ldmt_instanceGen
            reload(ldmt_instanceGen)
            ldmt_instanceGen.instanceGen()
        elif message == "Ribbon":
            from ldmt_function import ldmt_ribbonGen
            from ldmt_function import ldmt_fixReverse
            ldmt_ribbonGen.ribbonGen()
            ldmt_fixReverse.fixReverse()
            ld.showChannelBox()

        elif message == "Tube":
            from ldmt_function import ldmt_tubeGen
            from ldmt_function import ldmt_fixReverse
            sel = cmds.ls(sl=1)
            ldmt_tubeGen.tubeGen(sel[0])
            ldmt_fixReverse.fixReverse()
            ld.showChannelBox()

        elif message == "Seams":
            cmds.undoInfo(swf = False)
            maya_version = cmds.about(version=1)
            if maya_version == '2016': pluginPath = ldmt_plugin_path + "/seamsEasy_x64_2016.mll"
            elif maya_version == '2016.5': pluginPath = ldmt_plugin_path + "/seamsEasy_x64_2016.5.mll"
            elif maya_version == '2017': pluginPath = ldmt_plugin_path + "/seamsEasy_x64_2017.mll"
            elif maya_version == '2018': pluginPath = ldmt_plugin_path + "/seamsEasy_x64_2018.mll"
            if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
                cmds.loadPlugin (pluginPath)
            cmds.undoInfo(swf = True)
            mel.eval("seamsEasy")
        elif message == "Stitches":
            cmds.undoInfo(swf = False)
            maya_version = cmds.about(version=1)
            if maya_version == '2016': pluginPath = ldmt_plugin_path + "/seamsEasy_x64_2016.mll"
            elif maya_version == '2016.5': pluginPath = ldmt_plugin_path + "/seamsEasy_x64_2016.5.mll"
            elif maya_version == '2017': pluginPath = ldmt_plugin_path + "/seamsEasy_x64_2017.mll"
            elif maya_version == '2018': pluginPath = ldmt_plugin_path + "/seamsEasy_x64_2018.mll"
            if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
                cmds.loadPlugin (pluginPath)
            cmds.undoInfo(swf = True)
            mel.eval("stitchEasy")
        elif message == "Rope":
            from ldmt_function import ldmt_rope
            reload(ldmt_rope)
            ldmt_rope.ldmt_show()
        elif message == "Braid":
            from ldmt_function import ldmt_braidGen
            ldmt_braidGen.braidGen()
        elif message == "Edge To Curve":
            from ldmt_function import ldmt_edgeToCurve
            ldmt_edgeToCurve.edgeToCurve()
        elif message == "Ribbon Tools":
            LDRibbonToolsUI_show()
        elif message == "Curve On Mesh":
            from ldmt_function import ldmt_curveOnMesh
            ldmt_curveOnMesh.startDraw()
        elif message == "Clean Procedure":
            from ldmt_function import ldmt_cleanProcedure
            ldmt_cleanProcedure.cleanProcedure()
        # UV Tools
        
        # Debug Tools
        elif message == "Reverse By View":
            from ldmt_function import ldmt_fixReverse
            reload(ldmt_fixReverse)
            ldmt_fixReverse.fixReverse()

        # Common Panels
        elif message == "Plugin":
            ldmt_toggleUI.toggleUI('plugin')
        elif message == "Preference":
            ldmt_toggleUI.toggleUI('preference')
        elif message == "HyperGraph":
            ldmt_toggleUI.toggleUI('hypergraph')
            print('hahahah')
        elif message == "Node":
            ldmt_toggleUI.toggleUI('node')
        elif message == "Namespace":
            ldmt_toggleUI.toggleUI('namespace')  
        elif message == "Hotkey":
            ldmt_toggleUI.toggleUI('hotkey')
        # File
        
        # Info
        cmds.undoInfo(cck = 1)
        toolMessage = ["Mirror Tool", "Flatten Tool", "Nanomesh", "Instant Meshes", "Cloth Transfer", "Random Selector","Custom Grouper",\
                        "N Edge Selector","Rope","Ribbon Tools","Check UV Bleed","Scene","Clean Mesh","Rename","Display","Quick Export",\
                        "Texture Render"]
        if message in toolMessage:
            self.toggleToolBtnByMsg(message)

        ld.msg(message)
        
    def dockCloseEventTriggered(self):
        self.deleteInstances()

    # Delete any instances of this class
    def deleteInstances(self):
        def delete2016():
            # Go through main window's children to find any previous instances
            for obj in maya_main_window().children():
                if str(type(
                        obj)) == "<class 'maya.app.general.mayaMixin.MayaQDockWidget'>":  # ""<class 'maya.app.general.mayaMixin.MayaQDockWidget'>":
                    if obj.widget().__class__.__name__ == "LDMT_mainUI":  # Compare object names
                        obj.setParent(None)
                        obj.deleteLater()
        def delete2017():
            for obj in maya_main_window().children():
                if str(type(obj)) == "<class '{}.LDMT_mainUI'>".format(os.path.splitext(
                        os.path.basename(__file__)[0])):  # ""<class 'moduleName.mayaMixin.LDMT_mainUI'>":
                    if obj.__class__.__name__ == "LDMT_mainUI":  # Compare object names
                        obj.setParent(None)
                        obj.deleteLater()
        if maya_api_version() < LDMT_mainUI.MAYA2017:
            delete2016()
        else:
            delete2017()

    def deleteControl(self, control):
        if cmds.workspaceControl(control, q=True, exists=True):
            cmds.workspaceControl(control, e=True, close=True)
            cmds.deleteUI(control, control=True)

    # Show window with docking ability
    def run(self):
        def run2017():
            self.setObjectName("LDMT_mainUI")
            # The deleteInstances() dose not remove the workspace control, and we need to remove it manually
            workspaceControlName = self.objectName() + 'WorkspaceControl'
            self.deleteControl(workspaceControlName)
            # this class is inheriting MayaQWidgetDockableMixin.show(), which will eventually call maya.cmds.workspaceControl.
            # I'm calling it again, since the MayaQWidgetDockableMixin dose not have the option to use the "tabToControl" flag,
            # which was the only way i found i can dock my window next to the channel controls, attributes editor and modelling toolkit.
            self.show(dockable=True, area='left', floating=False)
            cmds.workspaceControl(workspaceControlName, e=True, dtc=["ToolBox",'right'],wp="fixed")
            self.raise_()
            # size can be adjusted, of course
        def run2016():
            self.setObjectName("LDMT_mainUI")
            # on maya < 2017, the MayaQWidgetDockableMixin.show() magiclly docks the window next
            # to the channel controls, attributes editor and modelling toolkit.
            self.show(dockable=True, area='left', floating=False)
            self.raise_()
            # size can be adjusted, of course
            self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        if maya_api_version() < LDMT_mainUI.MAYA2017:
            run2016()
        else:
            run2017()

def show():
    ldmt_globalUI = LDMT_mainUI(parent=maya_main_window())
    ldmt_globalUI.run()
    return ldmt_globalUI

# Bonus
# def changeMayaBackgroundColor():
#     widget.setStyleSheet(
#         'background-color:rgb(0,0,40);'+
#         'color:rgb(216, 138, 143);'
#         )
# omui.MQtUtil.mainWindow()
# ptr = omui.MQtUtil.mainWindow()    
# widget = wrapInstance(long(ptr), QWidget)
# changeMayaBackgroundColor()