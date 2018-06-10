import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2
PM_startTime = cmds.timerX()
PM_timeAdder = 0
MAYA_version = cmds.about(v=1)
MAYA_version_float = float(MAYA_version.split(' ')[0])

## Plugins ##
def ifExists(command):
    if not mel.eval('exists "'+command+'"'):
        return 0
    else:
        return 1
## Tranforms ##
def freeze(sel):
    cmds.makeIdentity(sel,apply=True, t=1, r=1, s=1, n=0)
    
## Select ##
def ls( index="all", type = "transform" ):
    # if index is str and not indicating index, then we think this is a type and return all index
    if index != "all" and index != 0:
        type = index
    
    # specify each type
    if type == "transform":
        sel = cmds.ls( sl=1, type = type )
    elif type in ["poly","polygon","polymesh","mesh","obj"]:
        sel = cmds.ls (sl=1, type ="transform")
        sel = cmds.filterExpand(sel,sm=12)
    elif type in ["c","cr","curve","nurbsCurve"]:
        sel = cmds.ls (sl=1, type ="transform")
        sel = cmds.filterExpand(sel,sm=9)
        
    # specify index
    if index == "all" or isinstance(index,(str)):
        if sel == None:
            msg("Nothing Selected")
            return None
        return sel
       
    elif isinstance(index,(int)):
        if sel == None:
            msg("Nothing Selected")
            return None
        return sel[index]

## Warning ##
def msg(msg="Heads Up!"):
    global PM_startTime
    global PM_timeAdder
    PM_offset = 0
    PM_time = cmds.timerX(startTime = PM_startTime)
    PM_startTime = cmds.timerX()
    if PM_time<1.5:
        PM_offset = 10+20*(PM_timeAdder)
        PM_timeAdder = PM_timeAdder+1 
    else:
        PM_offset = 10
        PM_timeAdder = 0 
    if MAYA_version_float >= 2014:
        cmds.inViewMessage(
        amg = "<span style=\"color:#ffffff\">"+ msg +"</span>",
        fade = 1, fit = 150, fst = 800, fot = 150, fof = PM_offset, bkc = 0x2288ff, 
        pos = "topCenter", fontSize = 10, a = 0, ta = 0.68)
    