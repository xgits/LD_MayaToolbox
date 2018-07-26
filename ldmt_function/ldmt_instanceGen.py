import maya.cmds as cmds
import maya.mel as mel
from ldmt_core import ldmt_cmds as ld
def instanceGen():
    ldmt_plugin_path = ld.getPath('LDMT') + '/ldmt_plugin'
    pluginPath =ldmt_plugin_path + "/instanceAlongCurve.py"
    if cmds.pluginInfo (pluginPath,q=1,l=1) !=1: 
        cmds.loadPlugin (pluginPath)
    sel = cmds.ls(sl=1)
    curve = cmds.filterExpand(sel,sm=9)
    obj = cmds.filterExpand(sel,sm=12)
    cmds.select(curve,r=1)
    cmds.select(obj,add=1)
    mel.eval("instanceAlongCurve")

