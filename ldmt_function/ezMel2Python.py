# -*- coding: utf-8 -*-
u'''
------------------------------------------------------------
this script translate MEL to Python

Usage:
import ezMel2Python
ezMel2Python.ezMel2Python()

ezMel2Python.ui must be put same folder.

------------------------------------------------------------
'''
import os
import pymel.core as pm
import pymel.tools.mel2py as mel2py
from ldmt_core import ldmt_cmds as ld

def em2pConvMel2Py():
	u'''translate MEL to Python'''
	melCmd = pm.scrollField( 'em2pTextEditMEL', q=1,tx=1 )
		
	pyCmd =  mel2py.mel2pyStr(melCmd,pymelNamespace='pm')
	pyFixed = pyCmd.replace("pymel.all","pymel.core")
	pm.scrollField( 'em2pTextEditPy', e=1,tx=pyFixed )

def ezMel2Python():
	ldmt_ui_path = ld.getPath('LDMT') + '/ldmt_ui'

	try:
		em2pUIFile = ldmt_ui_path + "/ezMel2Python.ui"
	except:
		print u'Error,can\'t load UI.'
		return

	if pm.window('ezMel2PyWin', exists=1) :
		pm.deleteUI( 'ezMel2PyWin' )

	ezMel2PythonWindow = pm.loadUI( uiFile = em2pUIFile )
	pm.showWindow( 'ezMel2PyWin' )
	pm.window('ezMel2PyWin',e=1,tlc=(200,250) )
