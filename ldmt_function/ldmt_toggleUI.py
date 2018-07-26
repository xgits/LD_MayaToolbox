# Liu Dian 
# xgits@outlook.com
# www.xgits.com
import maya.cmds as cmds
import maya.mel as mel
def toggleUI(uiName):
    if uiName == 'UV':
        toggleUV()
    elif uiName == "hypershade":
        toggleHyperShade()
    elif uiName == "outliner":
        toggleOutliner()
    elif uiName == "plugin":
        togglePlugin()
    elif uiName == "preference":
        togglePreference()
    elif uiName == "hypergraph":
        toggleHyperGraph()
    elif uiName == "node":
        toggleNodeEditor()
    elif uiName == "namespace":
        toggleNamespace()
    elif uiName == "hotkey":
        toggleHotkey()

def toggleUV():
    if cmds.window('polyTexturePlacementPanel1Window',ex=1):
        cmds.deleteUI('polyTexturePlacementPanel1Window')
        mel.eval('toggleUVToolkit;')
    else:
        mel.eval('texturePanelShow;')
        uvEditorPanel = cmds.getPanel( sty='polyTexturePlacementPanel')
        uvEditorWindow = uvEditorPanel[0] + 'Window'
        cmds.workspaceControl("UVToolkitDockControl",e=1,dockToControl=[uvEditorWindow,'right'])
    
def toggleHyperShade():
    if cmds.window('hyperShadePanel1Window',ex=1):
        cmds.deleteUI('hyperShadePanel1Window')
    else:
        cmds.scriptedPanel("hyperShadePanel1",e=1,to=1)

def toggleOutliner():
    try:
        if cmds.workspaceControl("Outliner",q=1,vis=1):
            cmds.workspaceControl("Outliner",e=1,vis=0)
        else:
            cmds.workspaceControl("Outliner",e=1,vis=1)
    except:
        if cmds.window("Outliner",ex=1):
            cmds.deleteUI("Outliner")
        else:
            mel.eval("OutlinerWindow;")

def togglePlugin():
    if cmds.window('pluginManagerWindow',ex=1):
        cmds.deleteUI('pluginManagerWindow')
    else:
        mel.eval('PluginManager;')

def togglePreference():
    if cmds.window('PreferencesWindow',ex=1):
        cmds.deleteUI('PreferencesWindow')
    else:
        mel.eval('PreferencesWindow;')

def toggleHyperGraph():
    if cmds.window('hyperGraphPanel1Window',ex=1):
        cmds.deleteUI('hyperGraphPanel1Window')
    else:
        cmds.scriptedPanel("hyperGraphPanel1",e=1,to=1)

def toggleNodeEditor():
    if cmds.window('nodeEditorPanel1Window',ex=1):
        cmds.deleteUI('nodeEditorPanel1Window')
    else:
        cmds.scriptedPanel("nodeEditorPanel1",e=1,to=1)

def toggleHotkey():
    if cmds.window('HotkeyEditor',ex=1):
        cmds.deleteUI('HotkeyEditor')
    else:
        mel.eval('HotkeyPreferencesWindow;')
        
def toggleNamespace():
    if cmds.window('namespaceEditor',ex=1):
        cmds.deleteUI('namespaceEditor')
    else:
        mel.eval('NamespaceEditor;')