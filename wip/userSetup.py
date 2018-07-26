#LDMT#LDMT beta
#Dont't Edit Anythin Within #LDMT (Including #LDMT)

import maya.cmds as cmds
import sys

MAYA_SCRIPT_PATH = os.environ['MAYA_SCRIPT_PATH']
MAYA_SCRIPT_PATH = MAYA_SCRIPT_PATH.split(';')

for eachPath in MAYA_SCRIPT_PATH:
    if eachPath.endswith('maya/scripts'):
        MAYA_SCRIPT_PATH = eachPath

LDMTPATH = MAYA_SCRIPT_PATH + '/' + 'LDMT' 

sys.path.insert(0,LDMTPATH)
sys.path.insert(0,LDMTPATH+'/ldmt_function')
import ldmt_ui
reload(ldmt_ui)
ldmt_ui.show()

#LDMT