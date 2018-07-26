import maya.cmds as cmds
import maya.mel as mel
 
def getMayaScriptPath():
    mayaScriptPath = os.environ['MAYA_SCRIPT_PATH']
    mayaScriptPath = mayaScriptPath.split(';')
    for eachPath in mayaScriptPath:
        if eachPath.endswith('maya/scripts'):
            mayaScriptPath = eachPath
    return mayaScriptPath

def add2Shelf():
    gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
    title = "LDMT"
    mayaScriptPath = getMayaScriptPath()
    currentShelf =cmds.tabLayout(gShelfTopLevel,h=300,q=1,st=1)
    cmds.setParent(gShelfTopLevel + "|" + currentShelf)

    imagePath = mayaScriptPath+ "/LDMT/ldmt_icon/LDMT_pro.png"
    highlightImagePath = mayaScriptPath+ "/LDMT/ldmt_icon/LDMT_pro_highlight.png"
    cmds.shelfButton(ann="Launch LD MayaToolbox",l=title,image1=imagePath,hi=highlightImagePath,
    command='import maya.cmds as cmds\n\
import maya.mel as mel\n\
PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")\n\
sys.path.append(PATH_MAYA_app_dir+"/scripts/LDMT")\n\
sys.path.append(PATH_MAYA_app_dir+"/scripts/LDMT/ldmt_function")\n\
cmds.evalDeferred("import ldmt_ui")\n\
cmds.evalDeferred("reload(ldmt_ui)")\n\
cmds.evalDeferred("from ldmt_ui import *")\n\
cmds.evalDeferred("show()") ')
