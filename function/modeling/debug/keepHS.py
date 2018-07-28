"""
Author: Buliarca Cristian (buliarca@yahoo.com)
Copyright (C) 2013 Buliarca Cristian
http://buliarca.blog124.fc2.com/

Version: 1.0.1

Function:
	this script takes the selected objects and transforms the locked normals
	into Hard or Soft edges.
	Usually when the user import an object in format fbx, from other 3d package 
	maya bring that object with locked normals not with hard and soft edges.

	To install it you need to copy the script : "lockNormals_toHS.py"
	 in maya user scripts directory:
		"c:\Users\_your user name_\Documents\maya\2012-x64\scripts\"

	and use these python command to run it:

import lockNormals_toHS as lockNormals_toHS
reload(lockNormals_toHS)

	If you want to have it on your shelf just create a shelf button with the above comments.

	Use and/or modify at your own risk.

Update:
	Simplified the second step, now the script is 2 times faster
	
"""

import maya.cmds as cmds
import math

class mbVector() :
	"""provides 3D vector functionality simmilar to Maya"""
	x, y, z = 0.0, 0.0, 0.0
		
	def __init__( self, *initValues ) :
		if len( initValues ) == 1 :
			self.x = initValues[ 0 ][ 0 ]
			self.y = initValues[ 0 ][ 1 ]
			self.z = initValues[ 0 ][ 2 ]
		else :
			self.x = initValues[ 0 ]
			self.y = initValues[ 1 ]
			self.z = initValues[ 2 ]

	def __add__( self, other )	:
		return mbVector( [ self.x + other.x, self.y + other.y, self.z + other.z ] )

	def __sub__( self, other )	:
		return mbVector( [ self.x - other.x, self.y - other.y, self.z - other.z ] )
		
	def __mul__( self, scalar ) :
		return mbVector( [ self.x * scalar, self.y * scalar, self.z * scalar ] )
	
	def mag( self ) :
		return math.sqrt( self.x*self.x + self.y*self.y + self.z*self.z )
	

	def __repr__( self ) :
		return ( "<< " + str( math.floor( self.x * 100.0 + 0.49) / 100.0 ) + ", " + str( math.floor( self.y * 100.0 + 0.49 ) / 100.0 ) + ", " + str( math.floor( self.z * 100.0 + 0.49 ) / 100.0 ) + " >>" )
	

def progress(step1):
	if(cmds.window(MBScriptWin, q=True, ex = True) ):
		cmds.progressBar(progressControl, edit=True, progress=step1+1)

def setMaxVal(val):
	if(cmds.window(MBScriptWin, q=True, ex = True) ):
		if val ==0:
			val = 1
		cmds.progressBar(progressControl, edit=True, maxValue=val)

def delProgWin():
	if(cmds.window(MBScriptWin, q=True, ex = True) ):
		cmds.deleteUI( MBScriptWin, window=True )

def changeMessageTo(newText):
	if(cmds.window(MBScriptWin, q=True, ex = True) ):
		cmds.text(mbText, edit=True, label = newText)

def remove_values_from_list(the_list, val):
    for ii in range(the_list.count(val)):
        the_list.remove(val)

def compareVFNormal(vert):
	obj = vert.split(".")
	nrVtx = obj[1].split("[")
	nrVtx = nrVtx[1].strip("]")
	edg = []
	vfInfo = cmds.polyInfo( vert, vf=True )
	vfList = []
	vfIList = vfInfo[0].split(' ')
	emptyListIdx = []
	ee = 0
	remove_values_from_list(vfIList, "")
	remove_values_from_list(vfIList, "\n")
	vfIList.pop(0)
	vfIList.pop(0)
	for i in range(len(vfIList)):
		fInf = vfIList[i].strip()
		vfList.append(obj[0]+".vtxFace["+nrVtx+"]["+fInf+"]")
	vfN = cmds.polyNormalPerVertex(vfList[-1],query=True, xyz=True )
	vfOldV = mbVector(vfN[0],vfN[1],vfN[2])
	for j in range(len(vfList)):
		vfN1 = cmds.polyNormalPerVertex(vfList[j], query=True, xyz=True )
		vfNewV = mbVector(vfN1[0],vfN1[1],vfN1[2])
		compV = vfOldV - vfNewV
		if compV.mag() != 0:
			hEdge = cmds.polyListComponentConversion(vfList[j], te= True)
			edg.append(hEdge[0])
		vfOldV = vfNewV
	return edg

def mbJoin(list1, list2):
	for a in list2:
		list1.append(a)
	return list1

def SGtoHS():
	try:
		sel = cmds.ls(sl=True, fl=True)
		for obj in sel:
			changeMessageTo('  Step 1 of 2 for: ' + str(obj))
			nrVtx = cmds.polyEvaluate(obj, v=True)
			setMaxVal(nrVtx)
			hardEdg = []
			h = 0
			for i in range(nrVtx):
				currVert = obj+".vtx["+str(i)+"]"
				cmpV = compareVFNormal(currVert)
				hardEdg = mbJoin(hardEdg,cmpV)
				progress(i)
			
			cmds.polyNormalPerVertex (obj, ufn = True)
			cmds.polySoftEdge (obj, a=180)
			setMaxVal(len(hardEdg))
			progress(0)
			changeMessageTo('  Step 2 of 2 for: ' + str(obj) )
			k=0
			if len(hardEdg) != 0:
				cmds.select(hardEdg, r=True)
				cmds.polySoftEdge (a=0)
			
		cmds.select(sel, r=True)
		delProgWin()
	except :
		sel = []
		if len(sel) == 0:
			changeMessageTo('You need to have at least one object selected')
try:
	if(cmds.window(MBScriptWin, q=True, ex=True) ):
		delProgWin()
except :
	pass
MBScriptWin = cmds.window(title="Converting locked normals to Soft\Hard Edges")
cmds.columnLayout(adjustableColumn=True)
mbText = cmds.text( label='  Step 1 of 2  ', align='center' )
progressControl = cmds.progressBar(maxValue=10, width=400, isInterruptable = True)
cmds.showWindow( MBScriptWin )
SGtoHS()