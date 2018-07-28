import maya.cmds as cmds
import maya.mel as mel
def openFolder():
    fullpath = cmds.file(query=1 ,location=1)
    filename = cmds.file(q=1,sn=1,shn=1)
    filepath = fullpath[:-len(filename)]
    if fullpath =='unknown':
        mayaPath = mel.eval('getenv MAYA_LOCATION')
        exportPath = mayaPath+'/bin/'
    else:
        exportPath = filepath
    mel.eval('system("load '+ exportPath +'");')


