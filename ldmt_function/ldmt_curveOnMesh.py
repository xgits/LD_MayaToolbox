import maya.cmds as cmds
import maya.mel as mel

def ldmt_pfxToCurves():
    if cmds.currentCtx() == 'dynWireCtx1':
        new = cmds.ls(sl = True)
        if not new:
            return
        whichNode= cmds.ls(cmds.listRelatives(new, s = True)[0], st = True)[1]
        if whichNode == 'stroke':
            newStroke = new[0]    
            cmds.select(newStroke, r = True)
#            return
            mel.eval('doPaintEffectsToCurve(1);')
            st = cmds.listRelatives(newStroke, s = True)[0]
            c = cmds.listConnections(st, et = True, t = 'nurbsCurve')[0]
            cmds.rebuildCurve(c,ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=10,d=3,tol=0.01)
            cmds.select(cl = True)
            strokeMainCurves = cmds.listRelatives(c, ap= 1)
            strokeCurve = cmds.listRelatives(strokeMainCurves, ap= 1)
            cmds.ungroup(strokeCurve)
            cmds.ungroup(strokeMainCurves)
            cmds.evalDeferred('cmds.delete("'+newStroke+'")')

def ldmt_killPFXJob():
    all = cmds.scriptJob(lj = True)
    for a in all:
        if 'pfxToCurves' in a:
            cmds.scriptJob(kill = int(a.split(':')[0]))
    cmds.select(cl = True)
    cmds.evalDeferred('cmds.setToolTo(\'CreatePolySphereCtx\')')
    cmds.evalDeferred('cmds.setToolTo(\'selectSuperContext\')', lp = True)
    
def startDraw():
    sel = cmds.ls(sl=1,o=1)
    sel = sel[0]
    cmds.select(sel, r = True)

    mel.eval('MakePaintable;')
    vers = int(cmds.about(version = True))
    if not cmds.currentCtx() == 'dynWireCtx1':
        mainPath = mel.eval('getenv "MAYA_LOCATION"')
        if vers > 2016:
            brushLoc = mainPath + '/Examples/Paint_Effects/Pens/ballpointRough.mel'
        else:
            brushLoc =  mainPath + '/brushes/pens/ballpointRough.mel'
        mel.eval('copyBrushToSelected "' + brushLoc + '"')

    cmds.select(cl = True)
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mel.eval('ToggleToolSettings;')

    cmds.scriptJob(event = ['DagObjectCreated', 'ldmt_pfxToCurves()'], compressUndo = True)
    cmds.scriptJob(event =  ['ToolChanged', 'ldmt_killPFXJob()'] , runOnce = True)

if __name__ == "__main__":
    startDraw()