import maya.cmds as cmds
def cleanupPlugin():
    pluginNames = cmds.pluginInfo(query=1,listPlugins=1)
    for pluginName in pluginNames:
        cmds.pluginInfo(pluginName,e=1,autoload=0) 
    cmds.pluginInfo("fbxmaya",e=1,autoload=1)
    cmds.pluginInfo("modelingToolkit",e=1,autoload=1)
    cmds.pluginInfo("objExport",e=1,autoload=1)
    cmds.pluginInfo("wire",e=1,autoload=1)
    cmds.loadPlugin("fbxmaya",qt=1)
    cmds.loadPlugin("modelingToolkit",qt=1)
    cmds.loadPlugin("objExport",qt=1)