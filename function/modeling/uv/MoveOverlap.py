##Liu Dian xgits@outlook.com  www.xgits.com
##This is an open sourced script, you can use it freely.
##Feel free to contact me if you have any question.
##Move flipped/Overlap UV start:20180324 ver:20180324
##Version: Maya 2017 Update3 +
import maya.cmds as cmds
import maya.mel as mel
def returnFlippedUV():
    sel = cmds.ls(sl=True,fl=True)
    mel.eval("selectUVFaceOrientationComponents {} 0 2 1;")
    flippedUV = cmds.polyListComponentConversion(flippedFace,tuv=1)
    cmds.polyEditUV(flippedUV,u=1,v=0)
    return flippedUV
    
def returnOverlapUV():
    sel = cmds.ls(sl=True,fl=True)
    flippedFace = mel.eval("selectUVOverlappingComponents 1 0;")
    overlappedUV = cmds.polyListComponentConversion(flippedFace,tuv=1)
    overlappedUV = cmds.ls(overlappedUV,fl=True)
    cmds.select(sel,r=True)
    return overlappedUV
    
def makedic_shell():
    sel = cmds.ls(sl=True,fl=True)
    shells = cmds.polyEvaluate(sel,usi=1)
    shells = list(set(shells))
    shell_UVbysid = {}
    shell_uavg = {}
    shell_vavg = {}
    shell_umax = {}
    shell_umin = {}
    shell_vmax = {}
    shell_vmin = {}
    shelldic = {}

    for i in range(len(shells)):
        uvs_i = cmds.polyEvaluate(uis=shells[i])
        shell_UVbysid[shells[i]] = cmds.ls(uvs_i,fl=1)
        
        uv_uv = cmds.polyEditUV( uvs_i, query = True )
        uv_u = uv_uv[0::2]
        uv_v = uv_uv[1::2]
        
        uv_uavg = sum(uv_u)/len(uv_u)
        uv_vavg = sum(uv_v)/len(uv_v)
        
        uv_umax = max(uv_u)
        uv_umin = min(uv_u)
        uv_vmax = max(uv_v)
        uv_vmin = min(uv_v)

        shell_uavg[shells[i]] = uv_uavg
        shell_vavg[shells[i]] = uv_vavg
        
        shell_umax[shells[i]] = uv_umax
        shell_umin[shells[i]] = uv_umin
        shell_vmax[shells[i]] = uv_vmax
        shell_vmin[shells[i]] = uv_vmin

    shelldic["UVbysid"] = shell_UVbysid
    shelldic["uavg"] = shell_uavg
    shelldic["vavg"] = shell_vavg
    shelldic["umax"] = shell_umax
    shelldic["umin"] = shell_umin
    shelldic["vmax"] = shell_vmax
    shelldic["vmin"] = shell_vmin
    # print(shelldic)
    return shelldic
    
def makedic_StoF():
    sel = cmds.ls(sl=True,fl=True)
    if(sel!=[]):
        shells = cmds.polyEvaluate(sel,usi=1)
        shells = list(set(shells)) #Now we got shell IDs from selection
        shellToFace = {}

        for i in range(len(shells)):
            uvs_i = cmds.polyEvaluate(uis=shells[i])
            faces_i = cmds.polyListComponentConversion(uvs_i,fuv=1,tf=1) #Don't know if fuv increase performance
            shellToFace[shells[i]] = faces_i 
        return shellToFace
        
    else:
        print("No selection")
        return None

def makedic_shellOverlap():
    shellToFace = {}
    shellToFace = makedic_StoF() #Got shell to face dictionary
    faceList = {}
    shellOverlapped = {}
    for i in shellToFace:
        shellToAdd = [] #Overlap shell list that we need to add as value
        facesFromShell = shellToFace[i]
        for j in shellToFace:
            otherFacesFromShell = shellToFace[j]
            faceList = facesFromShell+otherFacesFromShell
            if(cmds.polyUVOverlap(faceList,oc=1)!=None and i!=j): #I don't need self overlap
                shellToAdd.append(j)
        shellOverlapped[i] = shellToAdd
    return shellOverlapped

def select_overlapUV():
    flippedUVList = returnFlippedUV()
    shelldic = makedic_shell() #function ref
    UVbysid = shelldic["UVbysid"]
    uavg = shelldic["uavg"]
    vavg = shelldic["vavg"]
    umax = shelldic["umax"]
    umin = shelldic["umin"]
    vmax = shelldic["vmax"]
    vmin = shelldic["vmin"]
    uvtomove = []
    shellsid = []

    for id in UVbysid:
        shellsid.append(id)
    # print("shellid")
    # print(shellsid)

    for i in range(len(shellsid)):
        shell = shellsid[i]
        uvs_shell = UVbysid[shell]
        uavg_shell = uavg[shell]
        vavg_shell = vavg[shell]
        umax_shell = umax[shell]
        umin_shell = umin[shell]
        vmax_shell = vmax[shell]
        vmin_shell = vmin[shell]
        for j in range(len(shellsid)-(i+1)):
            othershell = shellsid[i+1+j]
            uvs_othershell = UVbysid[othershell]
            uavg_othershell = uavg[othershell]
            vavg_othershell = vavg[othershell]
            umax_othershell = umax[othershell]
            umin_othershell = umin[othershell]
            vmax_othershell = vmax[othershell]
            vmin_othershell = vmin[othershell]
            
            if abs(uavg_shell - uavg_othershell) > 0.02:
                continue
            elif abs(vavg_shell - vavg_othershell) > 0.02:
                continue
            elif abs(umax_shell - umax_othershell) > 0.02:
                continue
            elif abs(umin_shell - umin_othershell) > 0.02:
                continue
            elif abs(vmax_shell - vmax_othershell) > 0.02:
                continue
            elif abs(vmin_shell - vmin_othershell) > 0.02:
                continue
            else:
                if(set(uvs_othershell).issubset(flippedUVList)):
                    uvtomove += uvs_othershell
                else:
                    uvtomove += uvs_shell
    uvtomove = list(set(uvtomove))
    return uvtomove

def moveUVtoRight():
    sel = cmds.ls(sl=1)
    overlapUV = select_overlapUV()
    cmds.polyEditUV(overlapUV,u=1,v=0)
    
def tryMoveUVtoRight():
    cmds.profiler(sampling=1)
    try:
        moveUVtoRight()
    except:
        print("Select Something First!")
        
    else:
        print("Success")
    cmds.profiler(sampling=0)

#tryMoveUVtoRight()
# if __name__ == "__main__":



# a = makedic_shell()
# print(a["UVbysid"])