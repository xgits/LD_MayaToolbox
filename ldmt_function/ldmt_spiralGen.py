import maya.cmds as cmds
import maya.mel as mel
from ldmt_core import ldmt_cmds as ld
def spiralGen():
    ldmt_plugin_path = ld.getPath('LDMT') + '/ldmt_plugin'
    pluginPath = ldmt_plugin_path + "/curve2spiral.py"
    if cmds.pluginInfo("curve2spiral",q=1,l=1) != 1:
        cmds.loadPlugin(pluginPath)
    sel = cmds.ls(sl=1)
    sel = cmds.filterExpand(sel,sm=9)
    if len(sel)>0:
        for i in sel:
            shapes = cmds.listRelatives(i,children=1)
            shape = shapes[0]
            node = cmds.createNode("curveSpiral")
            cmds.connectAttr(shape+".worldSpace",node+'.ic')
            outputNode = cmds.createNode("nurbsCurve")
            cmds.connectAttr(node+'.oc',outputNode+'.create')
            cmds.select([outputNode,node],r=1)
    else:
        ld.msg("No Curve Selected!")

