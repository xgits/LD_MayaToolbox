import maya.cmds as cmds
import maya.mel as mel
import os

def fastExport(exportType):

    fullpath = cmds.file(query=1 ,location=1)

    if fullpath == 'unknown':
        mayaPath = mel.eval('getenv MAYA_LOCATION')
        exportPath = mayaPath+'/bin/'
    else:
        filename = cmds.file(q=1,sn=1,shn=1)
        exportPath = fullpath[:-len(filename)]
    # subprocess.Popen('explorer '+ filepath +'', shell=True)
    sel = cmds.ls(sl=1,o=1)
    exportFolder = exportPath+"models/"
    if not os.path.exists(exportFolder):
        os.mkdir(exportFolder)
    exportName = exportFolder+sel[0]

    if exportType == 'OBJ':
        if cmds.pluginInfo("objExport",q=1,l=1) !=1: 
            mds.loadPlugin("objExport",qt=1)
        cmds.file(exportName, force=True, options='groups=1;ptgroups=1;materials=1;smoothing=1;normal s=1', type='OBJexport', pr=True, es=True)

    elif exportType == 'FBX':
        if cmds.pluginInfo("fbxmaya",q=1,l=1) !=1: 
            mds.loadPlugin("fbxmaya",qt=1)
        fbxExportName = exportName+".fbx"

        mel.eval('FBXExportScaleFactor 1;')
        mel.eval('FBXExportInAscii -v 1;')
        mel.eval('FBXExportSmoothingGroups -v 1;')
        mel.eval('FBXExportSmoothMesh -v 1;')
        mel.eval('FBXExportTriangulate -v 0;')
        mel.eval('FBXExportUpAxis y;')
        
        mel.eval('FBXExport -f "'+ fbxExportName +'" -s;')
        
    elif exportType == 'UE4':
        if cmds.pluginInfo("fbxmaya",q=1,l=1) !=1: 
            mds.loadPlugin("fbxmaya",qt=1)
        fbxExportName = exportName+".fbx"
        
        mel.eval('FBXExportScaleFactor 1;')
        mel.eval('FBXExportInAscii -v 1;')
        mel.eval('FBXExportSmoothingGroups -v 1;')
        mel.eval('FBXExportSmoothMesh -v 1;')
        mel.eval('FBXExportTriangulate -v 1;')
        mel.eval('FBXExportUpAxis y;')
        
        mel.eval('FBXExport -f "'+ fbxExportName +'" -s;')

    mel.eval('system("load '+ exportFolder +'");')

