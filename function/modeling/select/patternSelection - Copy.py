# Pattern Selection for Maya
# (c) Emil Lindfors 2016-2017
# gumroad.com/emill
# hi@emill.fi
# Polycount: Limeforce


# INSTALLATION:
# Full instructions on Gumroad & Polycount
#
# 1) Copy this file (patternSelection.py) somewhere in MAYA_SCRIPT_PATH
# (e.g. C:/Users/cooluser1234/Documents/maya/2017/prefs/scripts)
#
# 2) Make a hotkey (maybe Ctrl+UpArrow) for the Python command (without quotes)
# "import patternSelection; patternSelection.patternSelection()"
# [optional] Make another hotkey
# "import patternSelection; patternSelection.patternSelectionRepeat()"
#
# 3) Restart Maya

# ROADMAP:
#   - suppress Script Editor output
#	- pattern loop/ring selection


import pymel.core as pm

def patternSelection():

	with pm.UndoChunk():

		#pm.scriptEditorInfo(suppressInfo=True)

		selOrderTrackingEnabled = pm.selectPref(q=1, trackSelectionOrder=1)
		if not selOrderTrackingEnabled:
			#pm.confirmDialog( title='Warning', message='For pattern selection to work you need to enable selection order tracking [Windows > Settings/Preferences > Preferences > Selection > Track selection order]', button=['OK'])
			pm.selectPref(trackSelectionOrder=1)
			pm.mel.eval("selectPref -trackSelectionOrder true")
			return


		sel = pm.ls(orderedSelection=1,fl=1)

		if len(sel) <= 1:
			return

		# get name of mesh object containing selected components
		mesh = pm.ls(sel[0].name().split(".")[0])[0]


		##########
		# VERTEX #
		##########

		if sel[0].__class__.__name__ == "MeshVertex" and sel[1].__class__.__name__ == "MeshVertex":

			print "vepe"

			vertFirst = sel[-2].indices()[0]
			vertLast = sel[-1].indices()[0]

			# detect if two last selected vertices are next to each other
			nextToEachother = False
			pm.select( mesh+".vtx["+str(vertFirst)+"]",r=1)
			pm.select( mesh+".vtx["+str(vertLast)+"]",add=1)
			pm.mel.eval("ConvertSelectionToContainedEdges;")

			if len(pm.ls(sl=1)) == 1:
				nextToEachother = True

			# restore selection order stack
			pm.mel.eval("ConvertSelectionToVertices;") # avoid getting stuck in edge/multi-component mode
			pm.select(sel,r=1)
			pm.select(sel[-1],d=1)
			pm.select(sel[-2],d=1)
			pm.select(sel[-2],add=1)
			pm.select(sel[-1],add=1)

			if nextToEachother:
				selectNextVertex("next")
				return

			# detect if two last selected vertices are on same edge loop
			pm.select( mesh+".vtx["+str(vertFirst)+"]",r=1)
			pm.select( mesh+".vtx["+str(vertLast)+"]",add=1)

			# converting two verts on the same loop to and edge loop
			# results in selecting all verts between them (why?)
			pm.mel.eval("SelectEdgeLoopSp;")

			path = pm.ls(sl=1,fl=1)

			if ( path ): # on same loop

				# get edge loop, needed for inversion later
				pm.mel.eval("ConvertSelectionToContainedEdges;")
				edgePath = pm.ls(sl=1,fl=1)

				# SelectEdgeRingSp is sometimes unreliable with multiple consecutive
				# edges selected so we use just one edge to find the current loop
				pm.select(edgePath[0],r=1)

				pm.mel.eval("SelectEdgeLoopSp;")
				loop = pm.ls(sl=1)

			# restore selection order stack
			pm.select(sel,r=1)
			pm.select(sel[-1],d=1)
			pm.select(sel[-2],d=1)
			pm.select(sel[-2],add=1)
			pm.select(sel[-1],add=1)

			if ( path ): # on same loop
				selectNextVertex("pattern", mesh, len(edgePath)-1, loop)


		########
		# EDGE #
		########

		if sel[0].__class__.__name__ == "MeshEdge" and sel[1].__class__.__name__ == "MeshEdge":
			edgeFirst = sel[-2].indices()[0]
			edgeLast = sel[-1].indices()[0]

			ring = pm.polySelect( mesh.name(), q=1, edgeRingPath=[edgeFirst,edgeLast] )
			if ( ring ):
				if ( len(ring) == 2 ):
					selectNextEdge("ring")

				if ( len(ring) > 2 ):
					selectNextEdge("ringPattern", mesh, len(ring)-2)

			loop = pm.polySelect( mesh.name(), q=1, edgeLoopPath=[edgeFirst,edgeLast] )
			if ( loop ):
				if (len(loop) == 2 ):
					selectNextEdge("loop")

				if ( len(loop) > 2 ):
					selectNextEdge("loopPattern", mesh, len(loop)-2)


		########
		# FACE #
		########

		if sel[0].__class__.__name__ == "MeshFace" and sel[1].__class__.__name__ == "MeshFace":
			faceFirst = sel[-2].indices()[0]
			faceLast = sel[-1].indices()[0]

			path = pm.polySelect( mesh.name(), q=1, shortestFacePath=[faceFirst,faceLast] )

			if (path):

				if len(path) == 2:
					selectNextFace("next")

				if len(path) > 2:
					pm.select( mesh+".f["+str(faceFirst)+"]",r=1)
					pm.select( mesh+".f["+str(faceLast)+"]",add=1)

					pm.mel.eval("SelectEdgeLoopSp;")
					facePath = pm.ls(sl=1,fl=1)

					if (facePath):
						# face path isnt sorted
						pm.mel.eval("ConvertSelectionToContainedEdges;")
						pm.select(pm.ls(sl=1,fl=1)[0],r=1)
						pm.mel.eval("SelectEdgeRingSp;")
						pm.mel.eval("ConvertSelectionToVertices;") # TODO REM buggy command was: pm.mel.eval("GrowPolygonSelectionRegion;")
						pm.mel.eval("ConvertSelectionToContainedFaces;")
						loop = pm.ls(sl=1)
						print loop
						print "-------------------"

					# restore selection order stack
					pm.select(sel,r=1)
					pm.select(sel[-1],d=1)
					pm.select(sel[-2],d=1)
					pm.select(sel[-2],add=1)
					pm.select(sel[-1],add=1)

					#print len(facePath)

					if (facePath):
						selectNextFace("pattern", mesh, len(facePath)-2, loop)




def patternSelectionRepeat():

	pm.mel.eval("cmdFileOutput -closeAll;")

	print "repe"

	sel = pm.ls(orderedSelection=1,fl=1)

	nSelectedOld = len(sel)

	patternSelection()

	sel = pm.ls(orderedSelection=1,fl=1)
	nSelectedNew = len(sel)

	while ( nSelectedNew > nSelectedOld ):

		nSelectedOld = nSelectedNew

		patternSelection()

		sel = pm.ls(orderedSelection=1,fl=1)
		nSelectedNew = len(sel)



# END OF USER-FACING COMMANDS







def selectNextVertex(mode, mesh="", nVerticesInBetween=-1, loop=""):

	orig = pm.ls(orderedSelection=1,fl=1)

	if mode == "next":
		# find loop inversion
		pm.select(orig[-2],r=1)
		pm.select(orig[-1],add=1)
		pm.mel.eval("SelectEdgeLoopSp;")
		pm.mel.eval("InvertSelection")
		loopInverted = pm.ls(sl=1)

		pm.select(orig[-1],r=1)
		pm.mel.eval("GrowPolygonSelectionRegion;")


	elif mode == "pattern":

		# checked already that verts are on same loop (in patternSelectNext() )

		pm.select(loop,r=1)

		pm.mel.eval("PolySelectConvert 3;") # edges to vertices
		pm.mel.eval("InvertSelection")
		loopInverted = pm.ls(sl=1)

		tmpVerts = [orig[-1]]
		pm.select(orig[-1],r=1)
		for i in range(0,nVerticesInBetween+1):
			pm.mel.eval("GrowPolygonSelectionRegion;")
			pm.select(loopInverted,d=1)
			if i <= nVerticesInBetween:
		 		pm.select(tmpVerts,d=1)
		 		tmpVerts += pm.ls(orderedSelection=1,fl=1)



	pm.select(loopInverted,d=1)

	# a little dance to ensure that two newest selected edges are always last in the selection order
	pm.select(orig,d=1)
	new = pm.ls(orderedSelection=1,fl=1)
	pm.select(orig,add=1)
	pm.select(new,d=1)
	pm.select(orig[-1],d=1)
	pm.select(orig[-1],add=1)
	pm.select(new,add=1)




def selectNextEdge(mode, mesh="", nEdgesInBetween=-1):

	orig = pm.ls(orderedSelection=1,fl=1)

	# SelectEdgeRingSp is sometimes unreliable with multiple consecutive edges selected
	# luckily we always use the last selected edge to find the current loop/ring
	pm.select(orig[-1],r=1)
	if mode[0:4] == "ring":
		pm.mel.eval("SelectEdgeRingSp;")
	elif mode[0:4] == "loop":
		pm.mel.eval("SelectEdgeLoopSp;")
	pm.mel.eval("InvertSelection")
	ringOrLoopInverted = pm.ls(sl=1)

	pm.select(orig[-1],r=1)



	# convert to faces, edge perimeter, grow etc etc depending on mode
	if mode == "ring":
		pm.mel.eval( "ConvertSelectionToEdgePerimeter" )

	elif mode == "loop":
		pm.mel.eval( "ConvertSelectionToFaces;ConvertSelectionToEdges;GrowPolygonSelectionRegion;" )

	elif mode == "ringPattern":
		tmpEdges = pm.ls(orderedSelection=1,fl=1)
		for i in range(0,nEdgesInBetween+1):
			pm.mel.eval( "ConvertSelectionToEdgePerimeter;" )
			pm.select(ringOrLoopInverted,d=1)
			if i <= nEdgesInBetween:
				pm.select(tmpEdges,d=1)
				tmpEdges += pm.ls(orderedSelection=1,fl=1)

	elif mode == "loopPattern":
		tmpEdges = pm.ls(orderedSelection=1,fl=1)
		for i in range(0,nEdgesInBetween+1):
			pm.mel.eval( "ConvertSelectionToFaces;ConvertSelectionToEdges;GrowPolygonSelectionRegion;" )
			pm.select(ringOrLoopInverted,d=1)
			if i <= nEdgesInBetween:
				pm.select(tmpEdges,d=1)
				tmpEdges += pm.ls(orderedSelection=1,fl=1)


	pm.select(ringOrLoopInverted,d=1)

	# a little dance to ensure that two newest selected edges are always last in the selection order
	pm.select(orig,d=1)
	new = pm.ls(orderedSelection=1,fl=1)
	pm.select(orig,add=1)
	pm.select(new,d=1)
	pm.select(orig[-1],d=1)
	pm.select(orig[-1],add=1)
	pm.select(new,add=1)



def selectNextFace(mode, mesh="", nFacesInBetween=-1, loop=""):

	orig = pm.ls(orderedSelection=1,fl=1)

	if mode == "next":
		pm.select(orig[-2],r=1)
		pm.select(orig[-1],add=1)
		pm.mel.eval("SelectEdgeLoopSp;")
		pm.mel.eval("InvertSelection;")
		loopInverted = pm.ls(sl=1)

		pm.select(orig[-1],r=1)
		pm.mel.eval("GrowPolygonSelectionRegion;")


	if mode == "pattern":
		pm.select(loop,r=1)
		pm.mel.eval("InvertSelection;")
		loopInverted = pm.ls(sl=1)

		# restore stack
		pm.select(orig,r=1)
		pm.select(orig[-1],d=1)
		pm.select(orig[-2],d=1)
		pm.select(orig[-2],add=1)
		pm.select(orig[-1],add=1)

		pm.select(orig[-1],r=1)
		tmpFaces = pm.ls(orderedSelection=1,fl=1)
		for i in range(0,nFacesInBetween+1):
			pm.mel.eval( "GrowPolygonSelectionRegion;" )
			pm.select(loopInverted,d=1)
			if i <= nFacesInBetween:
				pm.select(tmpFaces,d=1)
				tmpFaces += pm.ls(orderedSelection=1,fl=1)

	pm.select(loopInverted,d=1)

	# fix selection order
	pm.select(orig,d=1)
	new = pm.ls(orderedSelection=1,fl=1)
	pm.select(orig,add=1)
	pm.select(new,d=1)
	pm.select(orig[-1],d=1)
	pm.select(orig[-1],add=1)
	pm.select(new,add=1)

