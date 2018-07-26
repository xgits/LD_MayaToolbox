'''
Auther: Liu Dian
github: https://github.com/xgits/LD_MayaToolbox
Email: xgits@outlook.com
Website: www.xgits.com
'''
import maya.cmds as cmds
import maya.mel as mel
def ldmt_turboSmooth():
    mods = cmds.getModifiers()
    mel.eval('resetPolySelectConstraint;')
    sel = cmds.ls(sl=1,o=1)
    sel = sel[0]
    cmds.select(sel+'.e[*]',r=1)
    cmds.polySelectConstraint(m=3,t=0x8000,sm=1)
    cmds.sets(n="ldmt_turboSmoothQS")
    currentSel = cmds.ls(sl=1)
    if currentSel != []:
        try:
            cmds.polyCrease(value=1)
        except:
            pass
    cmds.select(sel,r=1)
    cmds.polySmooth(sel,mth=0,sdt=2,ovb=2,ofb=3,ofc=1,ost=1,ocr=1,dv=1,bnr=1,c=0,kb=0,ksb=1,khe=1,kt=0,kmb=0,suv=1,peh=1,sl=1,dpe=1,ps=0.1,ro=1,ch=1)
    cmds.select("ldmt_turboSmoothQS",r=1)
    currentSel = cmds.ls(sl=1)
    if currentSel != []:
        try:
            cmds.polySoftEdge(a=0,ch=1)
            cmds.polyCrease(value=0)
        except:
            pass
        if mods == 4:
            try:
                cmds.polyCrease(value=1)
            except:
                pass
    cmds.polySelectConstraint(m=0,dis=1)
    cmds.select(sel,r=1)
    cmds.delete("ldmt_turboSmoothQS")